# This module defines the tools for downloading specified websits

import os
import json
from .downloader import MyFilesDownloader
from .links_finder.finder import NewFileFinder, NewLinkParser
from .links_finder.filter import *


def say_hello():
    print "hello world"

def opentraining_executor():
    """
    specially for downloading slides from opentraning
    """
    classurl = "http://opensecuritytraining.info/Training.html"
    ffinder = NewFileFinder(filt_opentrain, classurl)
    links = list(ffinder.find())
    print links
    with open("/home/huang/Desktop/opentrain/alllinks.txt", 'w') as fp:
        print "saving all links to file"
        for i in links:
            fp.write(i)
            fp.write("\n")

    outputfiles=dict()
    for url in links:
        # make dir
        dirname = url.split("/")[-1][:-5]
        try:
            os.mkdir(os.path.join("/home/huang/Desktop/opentrain/",dirname))
        except Exception,e:
            print str(e)
        # download file to
        #http://opensecuritytraining.info/AndroidForensics_files/AndroidForensics_all_materials_office_1.zip
        subffinder = NewFileFinder(filt_opentrain_file, url)
        links = list(subffinder.find())
        downer = MyFilesDownloader(links, dirname)
        #downer.startDownloadingFiles()
        outputfiles[url]=links
    
    with open("result.json", "w") as fp:
        json.dump(outputfiles, fp)

def download_opentrain_from_json(jsonfile="result.json"):
    with open(jsonfile, "r") as data:
        outputfiles = json.load(data)
    for url in outputfiles.keys():
        if len(outputfiles[url]) == 0:
            continue
        else:
            dirname = url.split("/")[-1][:-5]
            dirname = os.path.join("/home/huang/Desktop/opentrain/",dirname)
            try:
                os.mkdir(dirname)
            except Exception,e:
                print str(e)
            links = outputfiles[url]
            downer = MyFilesDownloader(links, dirname)
            downer.startDownloadingFiles()


def dump_linkdic_as_json(data, outputfile="result.json"):
    """
    Dumps the data dict (url => []) to json file
    """
    with open(outputfile, "w") as fp:
        json.dump(data, fp)


def load_linkdic_from_json(jsonfile):
    with open(jsonfile, "r") as data:
        outputfiles = json.load(data)
    return outputfiles


def make_dirname(srcdir, url):
    """
    Make dir name from srcdir and url
    srcdir:
        the base directory
    url:
        the download url
    """
    if os.path.exists(srcdir):
        srcdir = os.path.abspath(srcdir)
    else:
        srcdir = os.path.abspath('.')
    dirname = url.split("/")[-1][:-5]
    dirname = os.path.join(srcdir,dirname)
    try:
        os.mkdir(dirname)
    except Exception,e:
        print str(e)
    return dirname

def download_linkdic(outputfiles, outputdir):
    """
    Download all the links in outputfiles
    """
    for url in outputfiles.keys():
        if len(outputfiles[url]) == 0:
            continue
        else:
            dirname = make_dirname(outputdir, url)
            links = outputfiles[url]
            downer = MyFilesDownloader(links, dirname)
            downer.startDownloadingFiles()




        