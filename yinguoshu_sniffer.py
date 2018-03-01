#coding=utf-8
import urllib  
import urllib2
import json

class YGSSniffer(object):
    def __init__(self):
        self.start_page = 1
        self.per_page_count = 10
        self.idate = urllib2.quote("2018;2017") # 2018%3B2017
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

    def fetchOnePage(self, page_id):
        try:
            pass
        except Exception, e:
            print "fetch one page failed: ", e

    def fetchAllPages(self):
        try:
            url = self.prepareUrl(self.template_url, 1, self.per_page_count, self.idate)
            req = urllib2.Request(url, "", self.headers)
            response = urllib2.urlopen(req)
            if (response.getcode() != 200):
                raise Exception("HTTP request failed, url: ", url)
            
            res = response.read()
            data = json.loads(res)
            company_info = data['data']['company']['infos']
            str = json.dumps(company_info[0], ensure_ascii=False)
            print str
        except Exception, e:
            print "fetch all pages failed: ", e


if __name__ == "__main__":
    ygs = YGSSniffer()
    ygs.fetchAllPages()