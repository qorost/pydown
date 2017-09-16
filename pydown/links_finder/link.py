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
