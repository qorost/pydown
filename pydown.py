#this file is the command line interface

from finder import FileFinder
from downloader import MyFilesDownloader 

import argparse

pdf = ["pdf"]
adobe = pdf + [".ps"]
office = ["ppt","pptx","doc","docx"]
media = ["mp4","bittorrent","mp3"]
document = pdf + office 

if __name__ == '__main__':
	#
    #parser = argparse.ArgumentParser('PyDown, find and download documents in a webpage')
    #group = parser.add_mutually_exclusive_group()
    parser = argparse.ArgumentParser()
    parser.add_argument("-d",action="store_true",help="Enable Downloading files")
    parser.add_argument("-o","--output",type=str,help="Output directory")
    parser.add_argument("-f","--filter",type=str,help="File type filter")
    parser.add_argument("url",type=str,help="The Webpage")
    args = parser.parse_args()


    filetypes = pdf
    print args.filter, args.d, args.url

    if args.url is None:
        print "url not found"



    if args.filter is None:
        filetypes = pdf
    else:
        if args.filter == "all":
            filetypes = document + media
        elif args.filter == "office":
            filetypes = office
        elif args.filter == "document":
            filetypes = document
        elif args.filter == "media":
            filetypes = media

	ffinder = FileFinder(filetypes,args.url)
	links = list(ffinder.find())
    if args.d:
        if args.output is not None:
            dirname = args.output
        else:
            dirname = os.path.abspath('.')
    	downer = MyFilesDownloader(links,dirname)
        downer.startDownloadingFiles()
    else:
        print "Found Links:\n",links

    '''

	url = "http://csiflabs.cs.ucdavis.edu/~ssdavis/60/"
	filetypes = [".pdf"]
	dirname = "/Volumes/Transcend/DAVISWork/Classes/ecs60/materials"

	ffinder = FileFinder(filetypes,url)
	links = list(ffinder.find())

	downer = MyFilesDownloader(links,dirname)
	downer.startDownloadingFiles()
    '''
