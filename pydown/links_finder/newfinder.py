#The finder module helps to find various links
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
from urlparse import urljoin
from urlparse import urlsplit
import os
import sys
import urllib2

import util
from link import Item
from confsouper import MoSTSoup,DBLPSoup
from downloader import Downloader



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
	#print results,len(results)," found!"
	dirname = './files/'
	for i in results:
		#print i
		url = i.url
		filename = os.path.join(dirname,i.filename)
		#xdown = Downloader(url,filename)
		#xdown.run()

	url = "http://dblp.uni-trier.de/db/conf/sp/sp2015.html"
	p = DBLPSoup(url)
	finder = Finder(url,p)
	results = finder.find()

	for i in results:
		print i


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
