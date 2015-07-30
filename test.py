__author__ = 'liuqiang'



import chardet,urllib2

from TextExtractor import TextExtractor
import requests


te = TextExtractor()

#r = requests.get('http://www.163.com')
f = urllib2.urlopen('http://www.bbc.com/')

a = f.read()
#ec = chardet.detect(a)

c = a.decode('utf-8')


#print f.read()

print te.extract(c)
#print r.text



