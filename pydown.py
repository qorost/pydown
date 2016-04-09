#this file is the command line interface

from finder import FileFinder
from downloader import MyFilesDownloader 

if __name__ == '__main__':
	#check for input

	#

	url = "http://csiflabs.cs.ucdavis.edu/~ssdavis/60/"
	filetypes = [".pdf"]
	
	dirname = "/Volumes/Transcend/DAVISWork/Classes/ecs60/materials"

	ffinder = FileFinder(filetypes,url)
	links = list(ffinder.find())

	downer = MyFilesDownloader(links,dirname)
	downer.startDownloadingFiles()