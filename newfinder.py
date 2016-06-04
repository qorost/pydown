#The finder module helps to find various links

from HTMLParser import HTMLParser
from urlparse import urljoin
from urlparse import urlsplit
from bs4 import BeautifulSoup
from downloader import Downloader
import os


import sys
import urllib2

import util

class Item(object):
	def __init__(self,url,filename = '',description=''):
		self._url = url
		self._filename = filename
		self._descp = description

	def __str__(self):
		return "Filename: " + self._filename + "\tUrl: " + self._url + "\tDescription: " + self._descp

	def url():
	    doc = "The url property."
	    def fget(self):
	        return self._url
	    def fset(self, value):
	        self._url = value
	    def fdel(self):
	        del self._url
	    return locals()
	url = property(**url())

	def filename():
	    doc = "The filename property."
	    def fget(self):
	        return self._filename
	    def fset(self, value):
	        self._filename = value
	    def fdel(self):
	        del self._filename
	    return locals()
	filename = property(**filename())

	def descp():
	    doc = "The descp property."
	    def fget(self):
	        return self._descp
	    def fset(self, value):
	        self._descp = value
	    def fdel(self):
	        del self._descp
	    return locals()
	descp = property(**descp())

class MoSTSoup():
	def __init__(self,url):
		self._data = None
		self._url = url
		self.results = set()

	def url():
		doc = "The url property"
		def fget(self):
			return self._url
		def fset(self,value):
			self._url = value
		def fdel(self):
			del self._url
		return locals()
	url = property(**url())

	def soup():
		doc = "The soup property"
		def fget(self):
			return self._soup
		return locals()
	soup = property(**soup())

	def data():
		doc = "The doc data"
		def fget(self):
			return self._data
		def fset(self,value):
			self._data = value
		def fdel(self):
			del self._data
		return locals()
	data = property(**data())

	def feed(self,data):
		self._data = data

	def analyze(self):
		self._soup = BeautifulSoup(self._data)
		index = 0
		for td in self._soup.find_all('td'):
			paras = td.find_all('p')
			# print "td index : ",index
			index += 1
			if paras != []:
				if '2016' in self._url:
					#Keynote
					title = paras[0].b.text + paras[0].a.text
					value = paras[0].a['href']
					url = util.get_url(self._url,value)
					filename = title + urlsplit(value)[-1]
					descp = paras[1].b.text + paras[1].text
					paras = paras[1:]
				tindex = 0
				for p in paras:
					# print "\ttindex: ",tindex
					tindex += 1
					title = p.b.text
					hrefs = p.find_all('a')
					for h in hrefs:
						value = h['href']

						url = util.get_url(self._url,value)
						filename = title + util.name_file(url)
						filename = h.text + util.regulate_filename(filename)
						descp = ''
						self.results.add(Item(url,filename,descp))
						# print "\t\tfilename: ", filename

	def getresults(self):
		self.analyze()
		#return self._soup.find_all('a')
		return self.results


class MoSTParser(HTMLParser):
	def __init__(self,url):
		HTMLParser.__init__(self)
		self._url = url
		self.results = set()

	def url():
		doc = "The url property"
		def fget(self):
			return self._url
		def fset(self,value):
			self._url = value
		def fdel(self):
			del self._url
		return locals()
	url = property(**url())

	def handle_starttag(self,tag,attrs):
		pass
	def handle_data(self,data):
		pass

	def getresults(self):
		return self.results



class LinkParser(HTMLParser):
	def __init__(self,filetypes,url=None):
		HTMLParser.__init__(self)
		self.filetypes = filetypes
		self._url = url
		self.foundfiles = set()
		self.results = set()

	def url():
	    doc = "The url property."
	    def fget(self):
	        return self._url
	    def fset(self, value):
	        self._url = value
	    def fdel(self):
	        del self._url
	    return locals()
	url = property(**url())


	def handle_starttag(self,tag,attrs):
		if tag == 'a':
			for name,value in attrs:
				if name == 'href':
					for ftype in self.filetypes:
						if value.endswith(ftype):
							url = util.get_url(self._url,value)
							if url not in self.foundfiles:
							    self.foundfiles.add(url)
							    self.results.add(Item(url,util.name_file(url)))

	def getresults(self):
		return self.results

class Finder():
	def __init__(self,url,myparser=None):
		self.url = url
		self.con = None
		self.parser = myparser
		try:
			self.con = urllib2.urlopen(self.url,timeout=10)
		except:
			sys.stderr.write("Fail to open url\n")
			#print("Fail to open url " + self.url,file=sys.stderr)
			raise ValueError

	def find(self):
		if self.con is None or self.parser is None:
			print "Invalid Data Inputs(find)"
			return None
		if issubclass(self.parser.__class__,HTMLParser):
			self.parser.url = self.url
			self.parser.feed(self.con.read())
			return self.parser.getresults()
		elif issubclass(self.parser.__class__,BeautifulSoup):
			return self.parser.getresults()
		else:
			self.parser.feed(self.con.read())
			return self.parser.getresults()


if __name__ == "__main__":
	t = ["pdf","jpg"]
	url = "http://csiflabs.cs.ucdavis.edu/~ssdavis/60/"
	p = LinkParser(t,url)
	finder = Finder(url,p)
	results =  finder.find()
	# for i in results:
	# 	print i

	url = "http://www.ieee-security.org/TC/SPW2015/MoST/"
	p = MoSTParser(url)
	finder = Finder(url,p)
	resuls = finder.find()

	soup = MoSTSoup(url)
	finder = Finder(url,soup)
	results =  finder.find()
	dirname = './files/'
	for i in results:
		#print i
		url = i.url
		filename = os.path.join(dirname,i.filename)
		xdown = Downloader(url,filename)
		xdown.run()


#New Version design

'''
1.functions to tell if the tag/attrs
def mytifiles_filter(filetypes,tags,attrs):


class LinkFinder(HTMLParser)
    def __init__(url,filter)


class FileFinder()
    def __init__(filetypes,url)
    def make_filter(filetypes)
    def find()
'''
