import util
from link import Item
from bs4 import BeautifulSoup

class MySoup():
	def __init__(self,url):
		self._data = None
		self._url = url
		self._soup = None
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
		pass

	def getresults(self):
		self.analyze()
		#return self._soup.find_all('a')
		return self.results



class DBLPSoup(MySoup):
	def analyze(self):
		self._soup = BeautifulSoup(self._data)
		index = 0
		for section in self._soup.find_all("h2"):
			sectitle = section.text
			print sectitle
		for span in self._soup.find_all("span"):
			print '\t span = ',span



class MoSTSoup(MySoup):
	# def __init__(self,url):
	# 	MySoup.__init__(self,url)

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
