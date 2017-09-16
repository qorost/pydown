# The finder module helps to find various links

from HTMLParser import HTMLParser
from urlparse import urljoin


import sys
import urllib2


def get_url(url, value):
    """
    get url from the value of the href tag
    """
    if value.startswith("http"):
        return value
    else:
        return urljoin(url, value)


class LinkParser(HTMLParser):
    """
    Pass the url page
    """

    def __init__(self, ifiletypes, iurl):
        HTMLParser.__init__(self)
        self.filetypes = ifiletypes
        self.url = iurl
        self.foundfiles = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    for ftype in self.filetypes:
                        if value.endswith(ftype):
                            url = get_url(self.url, value)
                            self.foundfiles.add(url)

    def getlinks(self):
        return self.foundfiles


class FileFinder():
    def __init__(self, ifiletypes, iurl):
        self.filetypes = ifiletypes
        self.url = iurl
        self.con = None
        try:
            self.con = urllib2.urlopen(self.url, timeout=10)
        except:
            sys.stderr.write("Fail to open url\n")
            # print("Fail to open url " + self.url,file=sys.stderr)
            raise ValueError

    def find(self):
        if self.con is not None:
            p = LinkParser(self.filetypes, self.url)
            p.feed(self.con.read())
            return p.getlinks()


class NewLinkParser(HTMLParser):
    """
    Pass the url page
    """

    def __init__(self, ffilter, iurl):
        HTMLParser.__init__(self)
        self.filter = ffilter
        self.url = iurl
        self.foundfiles = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    value = get_url(self.url, value)
                    if self.filter(value):
                        self.foundfiles.add(value)

    def getlinks(self):
        return self.foundfiles


class NewFileFinder():
    def __init__(self, ffilter, iurl):
        self.filter = ffilter
        self.url = iurl
        self.con = None
        try:
            self.con = urllib2.urlopen(self.url, timeout=10)
        except:
            sys.stderr.write("Fail to open url\n")
            # print("Fail to open url " + self.url,file=sys.stderr)
            raise ValueError

    def find(self):
        if self.con is not None:
            p = NewLinkParser(self.filter, self.url)
            p.feed(self.con.read())
            return p.getlinks()


if __name__ == "__main__":
    t = ["pdf", "jpg"]
    url = "http://csiflabs.cs.ucdavis.edu/~ssdavis/60/"
    finder = FileFinder(t, url)
    print finder.find()


# New Version design

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
