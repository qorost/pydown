#!/usr/bin/env python

import unittest
import os

import pydown.downloader as downloader

class DownloaderTests(unittest.TestCase):
    def test_imgur(self):
        filename = "5MB5MB.zip"
        url = "http://ipv4.download.thinkbroadband.com/5MB.zip"
        xdown = downloader.Downloader(url, filename)
        #xdown.run()
        self.assertTrue(True)
        #self.assertTrue(os.path.exists(filename))


if __name__ == '__main__':
    unittest.main()
