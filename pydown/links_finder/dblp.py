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
import requests

from bs4 import BeautifulSoup
import re

def dblp_doi_page_filter(url):
    #http://dx.doi.org/10.1109/SP.2015.9
    """
    This function is used to filter doi_page links
    Input is: value (url)
    Output is: True (match result), False(not match)
    """
    if 'http://dx.doi.org' in url:
        return True
    return False


def doi_page_file_filter(url):
    #
    return False


class dblp():
    def __init__(self,url="http://dblp.uni-trier.de/db/conf/sp/sp2016.html",year=2016):
        self.year = year
        if year >= 10 and year <= 17 and '16' in url :
            self.url = url.replace("16",str(year))
        else:
            raise ValueError
        self.doipages = set()
        self.foundfilelinks = set()

    def savelinkstofile(self,filename=None):
        if filename is None:
            filename = "dblp20" + str(self.year) + ".txt"
        lf = LinkFile(filename)
        lf.saveto(self.foundfilelinks)

    def extractpages(self):
        try:
            con = urllib2.urlopen(self.url,timeout=10)
            p = LinkParser(self.url,filterfunc= dblp_doi_page_filter)
            p.feed(con.read())
            self.doipages = p.getlinks()
            self.savelinkstofile("saveddoipages.txt")
            return self.doipages
        except Exception,e:
            sys.stderr.write("Error in extractfilelinks: " + str(e))

    def extractfilelinks(self):
        if len(self.doipages) == 0:
            self.extractpages()
        for i in self.doipages:
            try:
                print "PAGE: " + str(i)


                r = requests.get(i,allow_redirects=True)
                #tmp = urllib2.urlopen(i,timeout=10)
                print r.url
                tmp = urllib2.urlopen(r.url,timeout=10)
                soup = BeautifulSoup(tmp)
                for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
                    print link.get('href')
                break

                t = LinkParser(r.url,filetypes=[".pdf"])
                t.feed(r.text)
                for i in t.getlinks():
                    self.foundfilelinks.add(i)
                    print "\tfile: ",i
                print "\n"
                tmp.close()
            except Exception,e:
                sys.stderr.write("Error in extractfilelinks: " + str(e))
            break
        self.savelinkstofile()

    def find(self):
        print "Extract information from: " + self.url
        if len(self.foundfilelinks) == 0:
            self.extractfilelinks()
        return self.foundfilelinks



if __name__ == "__main__":
    u = dblp(year= 13)
    links = u.extractpages()
    flinks = u.extractfilelinks()
    print flinks
