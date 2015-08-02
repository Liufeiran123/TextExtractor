__author__ = 'liuqiang'

import re


def charsetdet(html):
    fa = re.findall("(<meta.*?)(charset\\s*?=\\s*?['\"]?)(.*?)('|\">)",html,flags = re.I|re.S)
    if len(fa) != 0:
        if fa[0][2] == 'GB2312' or fa[0][2] == 'gb2312' or fa[0][2] == 'GBK' or fa[0][2] == 'gbk':
            return 'GB18030'
        return fa[0][2]
    else:
        return None






