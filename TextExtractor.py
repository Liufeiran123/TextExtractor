__author__ = 'liuqiang'
#coding=utf-8

import re
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

class TextExtractor(object):
    def __init__(self):
        self.lines = []
        self.blockWidth = 3
        self.threshold = -1
        self.start = -1
        self.end = -1
        self.indexDistribution = []
        self.flag = False

    def langdetect(self,line):
        return detect(line)

    #def trim(self,line):


    #def length(self,line):


    def extract(self,_html):
        return self.parse(_html,False)

    def parse(self,_html,_flag):
        self.flag = _flag
        self.html = self.preProcess(_html)

        #print self.html

        return self.getText()

    def preProcess(self,source):
        source = re.sub('<!DOCTYPE.*?>','',source,flags=re.I | re.S)
        source = re.sub('<!--.*?-->','',source,flags=re.I | re.S)
        source = re.sub('<script.*?>.*?</script>','',source,flags=re.I | re.S)
        source = re.sub('<style.*?>.*?</style>','',source,flags=re.I | re.S)
        source = re.sub('&.{2,7};|&#.{3,4};','',source)
        source = re.sub('<[sS][pP][aA][nN].*?>','',source)
        source = re.sub('</[sS][pP][aA][nN]>','',source)
        #source = re.sub("<[^>'\"]*['\"].*['\"].*?>",'',source)
        source = re.sub('<.*?>','',source,flags=re.S)
        source = re.sub('\r\n','\n',source)
        return source

    def getText(self):
        self.lines = self.html.split('\n')
        empty = 0
        text = ''

        if(len(self.lines) < self.blockWidth):
            return ""

        for i in range(len(self.lines) - self.blockWidth):
            if len(self.lines[i]) == 0:
                empty+=1
            wordsNum = 0
            for j in range(self.blockWidth):
                temp = re.sub('\\s+','',self.lines[i+j])
                if len(temp) != 0:
                    lang = ''
                    try:
                        lang = detect(self.lines[i+j])
                    except LangDetectException, e:
                        continue
                    #添加支持的语言
                    if lang == 'zh-cn':
                        self.lines[i+j] = re.sub('\\s+','',self.lines[i+j])
                        wordsNum += len(self.lines[i+j])
                    elif lang == 'en':
                        self.lines[i+j] = self.lines[i+j].strip(' ')
                        wordsNum += len(self.lines[i+j].split(' '))
            self.indexDistribution.append(wordsNum)

        _sum = sum(self.indexDistribution)

        self.threshold = min(100,(_sum/len(self.indexDistribution)) << (empty/(len(self.lines)-empty)>>1))
        self.threshold = max(50, self.threshold)

        start = -1
        end = -1

        boolstart = False
        boolend = False

        firstMatch = True

        for i in range(len(self.indexDistribution)):
            if firstMatch and (not boolstart):
                if (self.indexDistribution[i] > (self.threshold/2) ) and (not boolstart):
                    if (self.indexDistribution[i+1] != 0) or (self.indexDistribution[i+2] != 0):
                        firstMatch = False
                        boolstart = True
                        start = i
                        continue
            if (self.indexDistribution[i] > self.threshold) and (not boolstart):
                if (self.indexDistribution[i+1] != 0) or (self.indexDistribution[i+2] != 0) or (self.indexDistribution[i+3] != 0):
                    boolstart = True
                    start = i
                    continue
            if boolstart:
                if (self.indexDistribution[i] == 0) or self.indexDistribution[i+1] == 0:
                    end = i
                    boolend = True
            if boolend:
                buffer = ''
                for j in range(end - start + 1):
                    if len(self.lines[start + j]) < 4:
                        continue
                    buffer += self.lines[start + j]
                if 'Copyright' in buffer or u'版权所有' in buffer:
                    continue
                text += buffer
                boolend = boolstart = False

        if start > end:
            buffer =''
            for i in range(len(self.lines)-start):
                if len(self.lines[start+i]) < 4:
                    continue
                buffer+=self.lines[start+i]
            if ('Copyrght' not in buffer) or (u'版权所有' not in buffer):
                text+=buffer

        return text






















