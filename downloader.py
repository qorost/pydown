import urllib 
import urllib2 
#import requests
import os.path

import thread
import threading



class Downloader():
    def __init__(self,url,filename):
      self.url = url
      self.filename = filename

    def run(self) :
        msg= self.url
        i = 0
        url = self.url
        file_name = self.filename
        print 'Downloading file from url:%s\n ' %url
        # if file_name is None:
        #     file_name = url.split('/')[-1]
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
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status

        f.close()


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
                for url in self.downurls :
                    if url.find('/') >= 0:
                        filename = url.split('/')[-1]
                    else :
                        filename ="test.pdf"
                    filename =os.path.join(self.dir, filename)
                    filedownloader = Downloader(url, filename)
                    filedownloader.run()


def TestDownload():
    xdown = Downloader("http://www.crackmes.de/users/jockcranley/t0ad_k3yg3n/download",'k3yg3n.exe')
    xdown.run()


if __name__ == '__main__':
    TestDownload()

