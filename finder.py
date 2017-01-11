#The finder module helps to find various links

from HTMLParser import HTMLParser
from urlparse import urljoin


import sys
import urllib2



def get_url(url,value):
	if value.startswith("http"):
		return value
	else:
		return urljoin(url,value)
		#assemble the a value url
		#return url+value


class LinkParser(HTMLParser):
	def __init__(self,url,filetypes=[],filterfunc=None):
		HTMLParser.__init__(self)
		self.filetypes = filetypes
		self.url = url
		self.foundfiles = set()
		self.filterfunc = filterfunc

	def handle_starttag(self,tag,attrs):
		if tag == 'a':
			for name,value in attrs:
				if name == 'href':
					if self.filterfunc:
						if self.filterfunc(value):
							url = get_url(self.url,value)
							self.foundfiles.add(url)
							return

					for ftype in self.filetypes:
						print name,value, type(value)
						if value.endswith(ftype):
							url = get_url(self.url,value)
							self.foundfiles.add(url)
	def getlinks(self):
		return self.foundfiles

	def printlinks(self):
		for link in self.foundfiles:
			print link

class FileFinder():
	def __init__(self,url,filetypes=[]):
		self.filetypes = filetypes
		self.url = url
		self.con = None
		try:
			self.con = urllib2.urlopen(self.url,timeout=10)
		except:
			sys.stderr.write("Fail to open url\n")
			#print("Fail to open url " + self.url,file=sys.stderr)
			raise ValueError


	def find(self):
		if self.con is not None:
			p = LinkParser(self.url,self.filetypes)
			p.feed(self.con.read())
			return p.getlinks()

if __name__ == "__main__":
	t = ["pdf","jpg"]
	url = "http://csiflabs.cs.ucdavis.edu/~ssdavis/60/"
	finder = FileFinder(url,filetypes=t)
	print finder.find()


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
