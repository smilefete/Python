#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
	pic 复制    Cgo8PFTUV_mAUW_wAACHtpnf68w574.png
'''
import shutil
import hashlib

fo=open(r'lg-wh-logo-name.txt')
count=0
m = hashlib.md5()
for line in fo:
    count+=1
    print count
    line=line.strip()
    if line=='':
        continue
    pos=line.index('.')
    end=line[pos:]
    src=r'D:\lg-logo\4\\'+line
    #m.update(line)
    dest=r'D:\lg-logo\lg-wh\\'+line
    #dest=r'D:\lg-logo\lg-wh\\'+m.hexdigest()+end
    try:
        shutil.copy(src,dest)
    except IOError:
        continue
fo.close()
