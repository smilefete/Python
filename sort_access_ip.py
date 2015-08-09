#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
查看access.log中的ip，并排序
log的格式为：ip开头，之后有一个空格，然后是其他内容
'''
import sys,platform

def sort_address(src,dest):
	fin=None
	fout=None
	try:
		fin=open(src)
		fout=open(dest,'ab')
	except IOError:
		print 'src file not exist!'
		return
	dic={}
	count=1
	for line in fin:
		print count
		count+=1
		pos=line.index(' ')
		index=line[:pos]
		if dic.has_key(index):
			dic[index]+=1
		else:
			dic[index]=1
	dic_sorted=sorted(dic.items(),key=lambda d:d[1],reverse=True)
	for key,value in dic_sorted:
		fout.write(str(value)+' '+key+'\n')
	fin.close()
	fout.close()

if __name__ == '__main__':
	src=''
	dest=''
	os=platform.system()
	if os=='Linux':
		src='/data/logs/access.log'
		dest='/data/logs/access-sort.txt'
	elif os=='Windows':
		src=r'D:\tmp.log'
		dest=r'D:\tmp-sort.txt'
	print '-----------------begin sort-------------------'
	sort_address(src,dest)
	print '-----------------end sort-------------------'