__author__ = 'vin@misday.com'

import os, sys, urllib, codecs
from datetime import *

reload(sys)
sys.setdefaultencoding('utf8')

def get_timestamp():
	return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class Fetch:
	def __init__(self):
		self.use_proxy = False;
	
	def set_proxy(self, server, usr='', passwd=''):
		self.use_proxy = True;
		self.proxy_config = "http://%s:%s@%s" % (usr, passwd, server)
		print 'using proxy: %s' % (self.proxy_config)

	def get(self, url):
		print '<%s GET %s>' % (get_timestamp(), url)

		try:
			if self.use_proxy:
				wp = urllib.urlopen(url, proxies={'http' : self.proxy_config})
			else:
				wp = urllib.urlopen(url)
			response = wp.read();
		except:
			print 'failed...'
			response = ''

		return response
		
	def wget(self, url, filename):
		print '<%s DOWNLOAD %s>' % (get_timestamp(), url)
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

class Spider():
	todo = []
	vist = []
	callbacks = {}
	
	def __init__(self, name='Spider'):
		print name
		self.fetch = Fetch()
		
	def set_proxy(self, server, usr='', passwd=''):
		self.fetch.set_proxy(server, usr, passwd)

	def start(self):
		while len(self.todo) > 0:
			url = self.todo.pop(0)
			self.vist.append(url)
			
			response = self.fetch.get(url)
			self.dispatch(url, response)
				
	def dispatch(self, url, response):
		for u in self.callbacks.keys():
			if url.startswith(u): # TODO: replace with regular expression
				self.callbacks[u](url, response)

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
		self.fetch.wget(url, filename)

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
