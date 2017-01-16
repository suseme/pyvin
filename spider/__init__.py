__author__ = 'vin@misday.com'

import os, sys, urllib, urllib2, codecs, traceback, platform, re, threading
from datetime import *
from pyvin.core import Processor
import bs4

reload(sys)
sys.setdefaultencoding('utf8')

sysstr = platform.system()

def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class Fetch:
    def __init__(self):
        self.use_proxy = False;
        self.proxy = None

    def set_proxy(self, server, usr='', passwd=''):
        self.use_proxy = True;
        self.proxy_config = "http://%s:%s@%s" % (usr, passwd, server)
        self.proxy = {'http' : self.proxy_config}
        print 'using proxy: %s' % (self.proxy_config)

    def get2(self, url):
        print '<%s GET2 %s>... ' % (get_timestamp(), url),
        try:
            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36')
            reader= urllib2.urlopen(request)
            response = reader.read()
            print 'OK'
        except:
            print 'failed'
            traceback.print_exc()
            response = ''
        return response

    def get(self, url):
        print '<%s GET %s>... ' % (get_timestamp(), url),
        try:
            wp = urllib.urlopen(url, proxies=self.proxy)
            response = wp.read()
            print 'OK'
        except:
            print 'failed'
            traceback.print_exc()
            response = ''
        return response

    def retrieveFile(self, url, filename):
        print '<%s RETRIEVE %s --> %s>... ' % (get_timestamp(), url, filename),
        if os.path.exists(filename):
            print 'exist'
            return
        try:
            urllib.URLopener(self.proxy).retrieve(url, filename)
            print 'OK'
        except:
            print 'failed'
            traceback.print_exc()

    def wget(self, url, filename):
        print '<%s DOWNLOAD %s --> %s>... ' % (get_timestamp(), url, filename)
        if sysstr == 'Linux':
            try:
                cmd = "wget %s -O %s -nv" % (url, filename)
                # retry 10 times, timeout 120s
                args = '-c -T 120 -t 10'
                # quiet
                # args = '%s -q' % args
                # --no-clobber
                args = '%s -nc' % args
                # proxy
                if self.use_proxy:
                    args = '%s -e \"http_proxy=%s\"' % (args, self.proxy_config)
                cmd = '%s %s' % (cmd, args)
                # multi-thread
                # cmd = '%s &' % cmd
                os.system(cmd)
            except:
                print 'failed'
                traceback.print_exc()
        elif sysstr == 'Windows':
            print 'not support'
        else:
            print 'not support'

    def copyall(self, src, dst):
        if sysstr == 'Linux':
            os.system('cp -a %s/* %s/' % (src, dst))
        elif sysstr == 'Windows':
            os.system('xcopy /s/e/a/q/y %s\\* %s\\' % (src, dst))

class Spider(Processor):
    todo = []
    vist = []
    callbacks = {}

    def __init__(self, name='Spider'):
        Processor.__init__(self, interval=1)
        self.bind(Processor.EVT_START, self.onStart)
        self.bind(Processor.EVT_LOOP, self.onLoop)
        self.bind(Processor.EVT_STOP, self.onStop)

        self.name = name
        self.fetch = Fetch()

        # will run how many thread, default is 1.
        self.thread_count_max = 2
        self.thread_count = 0

        self.lock = threading.Lock()

    def set_max_thread(self, count):
        self.thread_count_max = count

    def set_proxy(self, server, usr='', passwd=''):
        '''set proxy'''
        self.fetch.set_proxy(server, usr, passwd)

    def onStart(self, event):
        print '[%s] starting...' % self.name
        return True

    def onLoop(self, event):
        count = self.url_count()
        if count > 0:
            # print 'url_count %d' % count
            if self.thread_count < self.thread_count_max: # there is
                url = self.pop_url()
                if url:
                    # print url
                    t = threading.Thread(target=self.processing, args=(url,))
                    t.start()
                    self.thead_count_increase()
            else:
                pass
            return True
        elif self.thread_count > 0: # waiting running thread
            return True
        else:
            return False

    def onStop(self, event):
        print '[%s] stopping...' % self.name
        return True

    def processing(self, args):
        # print args
        url = args

        response = self.fetch.get(url)
        self._dispatch(url, response)

        self.release_url(url)
        self.thread_count_decrease()

    def _dispatch(self, url, response):
        '''dispatch fetched content to callbacks'''
        for u in self.callbacks.keys():
            if re.match(u, url, flags=0): #url.startswith(u): # TODO: replace with regular expression
                self.callbacks[u](url, response)

    def thead_count_increase(self):
        self.lock.acquire()
        self.thread_count += 1
        self.lock.release()

    def thread_count_decrease(self):
        self.lock.acquire()
        self.thread_count -= 1
        self.lock.release()

    def add_urls(self, urls):
        '''add url to queue'''
        self.lock.acquire()
        if len(urls) > 0:
            for url in urls:
                if url not in self.todo and url not in self.vist:
                    self.todo.append(url)
        self.lock.release()

    def pop_url(self):
        self.lock.acquire()
        if len(self.todo) > 0:
            url = self.todo.pop(0)
        else:
            url = None
        self.lock.release()
        return url

    def release_url(self, url):
        self.lock.acquire()
        self.vist.append(url)
        self.lock.release()

    def url_count(self):
        self.lock.acquire()
        count = len(self.todo)
        self.lock.release()
        return count

    def add_callbacks(self, callbacks={}):
        '''add callbacks for urls fetched'''
        # print type(callbacks)
        for u in callbacks.keys():
            self.callbacks[u] = callbacks[u]

    ###################################################################################################################

    # for content
    def clear_node(self, soup, node, att={}):
        tags = soup.findAll(node, attrs=att)
        if tags:
            # print '%s %d' % (node, len(tags))
            for tag in tags:
                tag.extract()

    def download(self, url, filename):
        Persist.ensurePath(filename)
        if sysstr == 'Linux':
            self.fetch.wget(url, filename)
        elif sysstr == 'Windows':
            self.fetch.retrieveFile(url, filename)
        else:
            print 'not download %s' % url

class Persist():
    def __init__(self, filename, charset='utf-8'):
        Persist.ensurePath(filename)
        print '<%s Store \'%s\'>' % (get_timestamp(), filename)
        self.fp = fp = codecs.open(filename, 'w+', charset)

    def start_html(self):
        self.fp.write('<html xmlns="http://www.w3.org/1999/xhtml">\n')
        self.fp.write('<head>\n')
        self.fp.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
        self.fp.write('<body>\n')

    def set_title(self, title):
        self.fp.write('<h1>\n')
        self.fp.write(title)
        self.fp.write('</h1>\n')

    def set_info(self, clazz):
        self.fp.write('<p>\n')
        self.fp.write(clazz)
        self.fp.write('</p>\n')

    def stop_html(self):
        self.fp.write('</body></html>')

    def store(self, data):
        self.fp.write(data)

    def store_soup(self, soup, charset='utf-8'):
        content = str(soup.prettify())
        if len(charset):
            content = content.decode(charset)
        self.fp.write(content)

    def close(self):
        self.fp.close()

    @staticmethod
    def ensurePath(path):
        path = os.path.split(path)[0]
        if not os.path.exists(path):
            os.makedirs(path)

class SpiderStub:
    starts = []
    callbacks = {}

class SpiderSoup:
    @staticmethod
    def clearNode(soup, node, att={}):
        tags = soup.findAll(node, attrs=att)
        if tags:
            # print '%s %d' % (node, len(tags))
            for tag in tags:
                tag.extract()

    @staticmethod
    def clearAttr(soup, attrs, tag, att={}):
        tags = soup.findAll(tag, attrs=att)
        if tags:
            # print '%s %d' % (node, len(tags))
            for tag in tags:
                for attr in attrs:
                    del(tag[attr])

    @staticmethod
    def clearComments(soup):
        for child in soup.children:
            if isinstance(child, bs4.Comment):
                child.extract()

    @staticmethod
    def insertCss(soup, url):
        tag = soup.new_tag("link", href=url)
        tag['rel'] = 'stylesheet'
        tag['type'] = 'text/css'
        soup.head.append(tag)

    @staticmethod
    def insertScript(soup, url):
        tag = soup.new_tag("script")
        tag['src'] = url
        soup.head.append(tag)

def main():
    pass

if __name__ == '__main__':
    main()
