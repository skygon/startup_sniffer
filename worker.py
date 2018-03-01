#coding=utf-8
import threading
import urllib2
import json

class Worker(threading.Thread):
    def __init__(self, template_url, start_page, per_page_count, idate, total_pages, msg_queue):
        super(Worker, self).__init__()
        self.template_url = template_url
        self.start_page = start_page
        self.per_page_count = per_page_count
        self.idate = idate
        self.total_pages = total_pages
        self.queue = msg_queue
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        #self.values = {'name' : 'who','password':'123456'}  
        #self.data = urllib.urlencode(values)  
        self.headers = { 'User-Agent' : self.user_agent } 
        self.start() 

    def run(self):
        count = 0
        while count < self.total_pages:
            try:
                url = self.template_url %(self.start_page, self.per_page_count, self.idate)
                req = urllib2.Request(url, "", self.headers)
                response = urllib2.urlopen(req)
                if (response.getcode() != 200):
                    raise Exception("HTTP request failed, url: ", url)
                
                res = response.read()
                data = json.loads(res)
                if (data['data']['company']['count'] == 0):
                    break

                self.queue.put(data['data']['company']['infos'])
                self.start_page = self.start_page + 1
                count = count + 1
            except Exception, e:
                print "Worker error: ", e
        print "Finish work"