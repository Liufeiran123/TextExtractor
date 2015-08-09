__author__ = 'liuqiang'



import chardet,urllib2

from TextExtractor import TextExtractor
from Charsetdet import charsetdet




te = TextExtractor()

f = urllib2.urlopen('http://www.bbc.com/news/world-asia-china-33728654')
#f = urllib2.urlopen('http://www.sxdaily.com.cn/n/2015/0731/c142-5720819-4.html')

html = f.read()

#print a
#ec = chardet.detect(a)

code = charsetdet(html)

if code == None:
    code = chardet.detect(html)

c = html.decode(code)

print te.extract(c)



