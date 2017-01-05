import sys
import urllib
import urllib2
#import requests
import os.path

import thread
import threading

import argparse


def print_progress(iteration,total,prefix='Progress: ',suffix='Complete',decimals = 2, barlen = 100):
    """
        http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
    """
    filledlen = int(round(barlen*iteration)/float(total))
    percents = round(100.00*(iteration/float(total)),decimals)
    bar = '#' * filledlen + '-' * (barlen - filledlen)
    try:
        sys.stdout.write("%s [%s] %s%s %s\r" % (prefix,bar,percents,'%',suffix))
        sys.stdout.flush()
    except Exception,e:
        print str(e)
        print prefix,bar,percents,suffix
        print type(percents),type(bar)
    if iteration == total:
        print("\n")


class LinkFile():
    def __init__(self,filename="links.txt"):
        self.filename = filename

    def saveto(self,links):
        try:
            fp = open(self.filename,"w")
            for i in links:
                fp.write(i)
                fp.write("\n")
            fp.close()
        except Exception,e:
            sys.stderr.write("Error in Writing: " + str(e))

    def extractfrom(self,filename=None):
        links = set()
        if filename is not None:
            tmp = filename
        else:
            tmp = self.filename
        try:
            fp = open(tmp,"r")
            texts = fp.read().splitlines()
            for i in texts:
                links.add(i)
            fp.close()
            return links
        except Exception,e:
            sys.stderr.write("Error while reading: " + str(e))



class Downloader():
    def __init__(self,url,filename,overite=False):
      self.url = url
      self.filename = filename

    def run(self,overite=False) :
        msg= self.url
        i = 0
        url = self.url
        file_name = self.filename
        if os.path.exists(os.path.abspath(file_name)) and overite == False:
            print "File Already Existed, skip downloading..."
            return 1
        try:
            u = urllib2.urlopen(url)
            f = open(file_name, 'wb')
            meta = u.info()
            file_size = int(meta.getheaders("Content-Length")[0])
            print "Downloading: %s Bytes: %s" % (file_name, file_size)


            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break
                file_size_dl += len(buffer)
                f.write(buffer)
                print_progress(file_size_dl,file_size)
                #status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                #status = status + chr(8)*(len(status)+1)
                #print status

            f.close()
            return 0
        except Exception,e:
            print 'Exceptiion in %s',url,': ',str(e)
            return -1


class MyDownLoadThread(threading.Thread) :
    def __init__(self,url, filename = None):
        threading.Thread.__init__(self)
        self.fileurl = url
        if filename is not None:
            self.filename = filename
        else:
            if url.find('/') >= 0:
                self.filename = url.split('/')[-1]
            else :
                self.filename ='test.pdf'

    def run(self) :
        msg= 'Thread downloading %s started!\n From url: %s' %(self.filename,self.fileurl)
        try :
            urllib.urlretrieve(self.fileurl, self.filename,None)
            msg= 'File %s downloaded!' %  self.filename
        except:
            msg= 'failed to download'


class MyFilesDownloader():
    def __init__(self, urls, dir='.'):
        self.downurls = urls
        self.threads = []
        self.dir = dir

    def startDownloadingFiles(self, multiThreading = False):
        if multiThreading == True :
            msg= 'In MULTITHREAD mode \nStart Downloading file into directory %s...' % self.dir

            if self.downurls is not None:
                for url in self.downurls :
                    if url.find('/') >= 0:
                        filename = url.split('/')[-1]
                    else :
                        filename ="test.pdf"
                    filename =os.path.join(self.dir, filename)
                    t = MyDownLoadThread(url, filename)
                    self.threads.append(t)
                    t.start()
        else :
            msg= 'In NORMAL mode \nStart Downloading file into directory %s...' % self.dir
            if self.downurls is not None:
                i = 1
                failures = 0
                skipped = 0
                success = 0
                num = len(self.downurls)
                for url in self.downurls :
                    if url.find('/') >= 0:
                        filename = url.split('/')[-1]
                    else :
                        filename ="test.pdf"
                    print "(%d/%d) URL: %s" %(i,num,url)
                    filename =os.path.join(self.dir, filename)
                    filedownloader = Downloader(url, filename)
                    result = filedownloader.run()
                    i += 1
                    if result == 1:
                        skipped += 1
                    elif result == 0:
                        success += 1
                    else:
                        failures += 1
            print "\nDownloading finished, (Suc:%d,Fails:%d,Skipped,%d,Total:%d)" %(success,failures,skipped,num)


def TestDownload():
    filename = "5MB5MB.zip"
    url = "http://download.thinkbroadband.com/5MB.zip"
    xdown = Downloader(url,filename)
    xdown.run()


if __name__ == '__main__':
    #TestDownload()
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input",type=str,help="input file")
    parser.add_argument("-o","--output",type=str,help="Output directory")
    #parser.add_argument("url",type=str,help="The Webpage")
    args = parser.parse_args()

    if args.output is not None:
        dirname = args.output
    else:
        dirname = os.path.abspath('.')

    if args.input is not None:
        links = LinkFile().extractfrom(args.input)
        downer = MyFilesDownloader(links,dirname)
        downer.startDownloadingFiles()






        #
