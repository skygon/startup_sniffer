#coding=utf-8
import urllib  
import urllib2
import json

class YGSSniffer(object):
    def __init__(self):
        self.start_page = 1
        self.per_page_count = 20
        self.idate = urllib2.quote("2018;2017") # 2018%3B2017
        self.prepared_url = "https://www.innotree.cn/inno/search/ajax/getAllSearchResult?query=&tagquery=&st=%s&ps=%s&areaName=%E6%B5%99%E6%B1%9F&rounds=&show=0&idate=%s&edate=&cSEdate=-1&cSRound=-1&cSFdate=1&cSInum=-1&iSNInum=1&iSInum=-1&iSEnum=-1&iSEdate=-1&fchain="
        self.url = self.prepareUrl(self.prepared_url)


    def prepareUrl(self, url):
        try:
            self.url = url %(self.start_page, self.per_page_count, self.idate)
        except Exception, e:
            print "prepare url error: ", e
