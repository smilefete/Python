#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
整理地址，多余的删除，按照公司id排序，对应同一公司的所有地址，按照地址长度降序排序
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
		index=int(line[0:pos])
		content=line[pos+1:].strip()
		if dic.has_key(index):
			list=dic[index]
			if not content in list:
				list.append(content)
			dic[index]=list
		else:
			dic[index]=[content]
	dic_sorted=sorted(dic.items(),key=lambda d:d[0])
	for key,value in dic_sorted:
		value.sort(key=lambda x:len(x))
		value.reverse()
		content=''
		for item in value:
			content+='#'
			content+=item
		fout.write(str(key)+' '+content+'\n')
	fin.close()
	fout.close()

if __name__ == '__main__':
	src=''
	dest=''
	os=platform.system()
	if os=='Linux':
		src='/home/hwz/address.txt'
		dest='/home/hwz/dest.txt'
	elif os=='Windows':
		src=r'F:\code\spider\address.txt'
		dest=r'F:\code\spider\dest.txt'
	print '-----------------begin sort-------------------'
	sort_address(src,dest)
	print '-----------------end sort-------------------'