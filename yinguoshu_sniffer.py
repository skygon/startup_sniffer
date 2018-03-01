#coding=utf-8
import urllib  
import urllib2
import json
from worker import Worker
from utils import company_queue

class YGSSniffer(object):
    def __init__(self):
        self.start_page = 1
        self.per_page_count = 10
        self.thread_load = 10 # each thread fetch 10 pages
        self.idate = urllib2.quote("2018") # 2018%3B2017
        self.area = "%E6%B5%99%E6%B1%9F"
        # all areas templare url, with idate configurable
        self.template_url = "https://www.innotree.cn/inno/search/ajax/getAllSearchResult?query=&tagquery=&st=%s&ps=%s&areaName=&rounds=&show=0&idate=%s&edate=&cSEdate=-1&cSRound=-1&cSFdate=1&cSInum=-1&iSNInum=1&iSInum=-1&iSEnum=-1&iSEdate=-1&fchain="
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        #self.values = {'name' : 'who','password':'123456'}  
        #self.data = urllib.urlencode(values)  
        self.headers = { 'User-Agent' : self.user_agent }  
        self.prepare_information_schema()

    def prepare_information_schema(self):
        self.prepare_company_info_schema()
        self.prepare_inst_info_schema()
    
    def prepare_company_info_schema(self):
        self.company_metadata = []
        self.company_metadata.append("alias")
        self.company_metadata.append("idate")
        self.company_metadata.append("round")
        self.company_metadata.append("amount")
        self.company_metadata.append("address")
        self.company_metadata.append("edate")  
        self.company_metadata.append("name")
        self.company_metadata.append("insts")
        self.company_metadata.append("mainClassify")
        self.company_metadata.append("mainChain")
        self.company_metadata.append("tags")
    
    def prepare_inst_info_schema(self):
        self.inst_metadata = []
        self.inst_metadata.append("instName")

    def prepareUrl(self, template_url, page_index, page_count, date_str):
        try:
            url = template_url %(page_index, page_count, date_str)
            return url
        except Exception, e:
            print "prepare url error: ", e


    def fetchAllPages(self):
        try:
            url = self.prepareUrl(self.template_url, 1, self.per_page_count, self.idate)
            req = urllib2.Request(url, "", self.headers)
            response = urllib2.urlopen(req)
            if (response.getcode() != 200):
                raise Exception("HTTP request failed, url: ", url)
            
            res = response.read()
            data = json.loads(res)
            count = data['data']['company']['count']
            
            thread_count = count / self.per_page_count / self.thread_load
            threads = []
            start_page = 0
            for i in range(thread_count):
                start_page = i * self.per_page_count + 1
                t = Worker(self.template_url, start_page, self.per_page_count, self.idate, self.thread_load, company_queue)
                threads.append(t)
            
            # left few pages, use another thread to fetch
            start_page = start_page + self.per_page_count
            t = Worker(self.template_url, start_page, self.per_page_count, self.idate, self.thread_load,company_queue)
            threads.append(t)
            
            for t in threads:
                if t.isAlive():
                    t.join()

            # start to process
            total_items = 0
            while(company_queue.empty() is False):
                company_queue.get()
                total_items = total_items + 1
            
            print "Total items ",  total_items
        except Exception, e:
            print "fetch all pages failed: ", e


if __name__ == "__main__":
    ygs = YGSSniffer()
    ygs.fetchAllPages()