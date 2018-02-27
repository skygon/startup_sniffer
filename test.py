#coding=utf-8
import urllib  
import urllib2
import gzip  
import StringIO 


"""
https://www.innotree.cn/inno/search/ajax/getAllSearchResult?query=&tagquery=&st=1&ps=10&areaName=%E6%B5%99%E6%B1%9F&rounds=&show=0&idate=2018%3B2017&edate=&cSEdate=-1&cSRound=-1&cSFdate=1&cSInum=-1&iSNInum=1&iSInum=-1&iSEnum=-1&iSEdate=-1&fchain=
"""

prov = u"浙江"
scope = 126 #company service
page = 1
prov = prov.encode('utf-8')
prov = urllib2.quote(prov)
url = "https://www.itjuzi.com/investevents?scope=%s&page=%s" %(prov,scope, page)

url = urllib2.unquote(url)
print url


user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
values = {'name' : 'who','password':'123456'}  
headers = { 'User-Agent' : user_agent }  
data = urllib.urlencode(values)  
req = urllib2.Request(url, "", headers)  
response = urllib2.urlopen(req) 
print "HTTP return code: ", response.getcode()
info = response.info()
print info
yread = response.read()

# response.read return gzip. Need special handle for this
ydata = StringIO.StringIO(yread)  
ygz = gzip.GzipFile(fileobj = ydata)  
yread = ygz.read()  
ygz.close()  
ystr = yread.decode('utf8', 'ignore').encode('GB2312')  
print ystr