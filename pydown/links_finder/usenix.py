#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 huang <huang@huang-desktop>
#
# Distributed under terms of the MIT license.

"""

"""

from finder import LinkParser
from downloader import *


import urllib2
import sys


def usenix_presentation_filter(url):
    if 'presentation' in url:
        return True
    return False

class USENIX():
    def __init__(self,year=2016):
        self.year = year
        if year >= 10 and year <= 17:
            self.url =  "https://www.usenix.org/conference/usenixsecurity16/technical-sessions".replace("16",str(year))
        else:
            raise ValueError
        self.presentationpages = set()
        self.foundfilelinks = set()

    def savelinkstofile(self,filename=None):
        if filename is None:
            filename = "usenix20" + str(self.year) + ".txt"
        lf = LinkFile(filename)
        lf.saveto(self.foundfilelinks)

    def extractpages(self):
        try:
            con = urllib2.urlopen(self.url,timeout=10)
            p = LinkParser(self.url,filterfunc=usenix_presentation_filter)
            p.feed(con.read())
            self.presentationpages = p.getlinks()

        except Exception,e:
            sys.stderr.write("Error in extractfilelinks: " + str(e))

    def extractfilelinks(self):
        if len(self.presentationpages) == 0:
            self.extractpages()
        for i in self.presentationpages:
            try:
                print "PAGE: " + str(i)
                tmp = urllib2.urlopen(i,timeout=10)
                t = LinkParser(i,filetypes=[".pdf"])
                t.feed(tmp.read())
                for i in t.getlinks():
                    self.foundfilelinks.add(i)
                    print "\tfile: ",i
                print "\n"
                tmp.close()
            except Exception,e:
                sys.stderr.write("Error in extractfilelinks: " + str(e))
        self.savelinkstofile()

    def find(self):
        print "Extract information from: " + self.url
        if len(self.foundfilelinks) == 0:
            self.extractfilelinks()
        return self.foundfilelinks



if __name__ == "__main__":
    u = USENIX(13)
    links = u.find()
    print links
    exit()
