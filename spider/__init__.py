__author__ = 'vin@misday.com'

import os, sys, urllib, codecs, traceback, platform
from datetime import *
from pyvin.core import Processor

reload(sys)
sys.setdefaultencoding('utf8')

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

    def get(self, url):
        print '<%s GET %s>' % (get_timestamp(), url)

        try:
            wp = urllib.urlopen(url, proxies=self.proxy)
            response = wp.read();
        except:
            print 'failed...'
            traceback.print_exc()
            response = ''

        return response

    def retrieveFile(self, url, filename):
        print '<%s RETRIEVE %s --> %s>' % (get_timestamp(), url, filename)
        if os.path.exists(filename):
            print 'exist...'
            return
        try:
            urllib.URLopener(self.proxy).retrieve(url, filename)
        except:
            print 'failed...'
            traceback.print_exc()

    def wget(self, url, filename):
        print '<%s DOWNLOAD %s --> %s>' % (get_timestamp(), url, filename)
        sysstr = platform.system()
        if sysstr == 'Linux':
            try:
                cmd = "wget %s -O %s" % (url, filename)
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
                print 'failed...'
                traceback.print_exc()
        elif sysstr == 'Windows':
            print 'not support'
        else:
            print 'not support'

    def copyall(self, src, dst):
        sysstr = platform.system()
        if sysstr == 'Linux':
            os.system('cp -a %s/* %s/' % (src, dst))
        elif sysstr == 'Windows':
            os.system('xcopy /s/e/a/q/y %s\\* %s\\' % (src, dst))

class Spider(Processor):
    todo = []
    vist = []
    callbacks = {}

    def __init__(self, name='Spider'):
        Processor.__init__(self)
        self.bind(Processor.EVT_START, self.onStart)
        self.bind(Processor.EVT_LOOP, self.onLoop)
        self.bind(Processor.EVT_STOP, self.onStop)

        self.name = name
        self.fetch = Fetch()

    def onStart(self, event):
        print '[%s] starting...' % self.name
        return True

    def onLoop(self, event):
        if len(self.todo) > 0:
            url = self.todo.pop(0)

            response = self.fetch.get(url)
            self._dispatch(url, response)

            self.vist.append(url)
            return True
        else:
            return False

    def onStop(self, event):
        print '[%s] stopping...' % self.name
        return True

    def _dispatch(self, url, response):
        for u in self.callbacks.keys():
            if url.startswith(u): # TODO: replace with regular expression
                self.callbacks[u](url, response)

    def set_proxy(self, server, usr='', passwd=''):
        self.fetch.set_proxy(server, usr, passwd)

    def add_urls(self, urls):
        if len(urls) > 0:
            for url in urls:
                if url not in self.todo and url not in self.vist:
                    self.todo.append(url)

    def add_callbacks(self, callbacks={}):
        # print type(callbacks)
        for u in callbacks.keys():
            self.callbacks[u] = callbacks[u]

    # for content
    def clear_node(self, soup, node, att={}):
        tags = soup.findAll(node, attrs=att)
        if tags:
            # print '%s %d' % (node, len(tags))
            for tag in tags:
                tag.extract()

    def download(self, url, filename):
        Persist.ensurePath(filename)
        self.fetch.retrieveFile(url, filename)

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
