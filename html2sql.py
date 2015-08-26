#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
html 2 sql
'''

__author__ = 'smilefete'

import os
import sys
import MySQLdb
import urllib2
from bs4 import BeautifulSoup

#
'''
str = ’0123456789′
print str[0:3] #截取第一位到第三位的字符
print str[:] #截取字符串的全部字符
print str[6:] #截取第七个字符到结尾
print str[:-3] #截取从头开始到倒数第三个字符之前
print str[2] #截取第三个字符
print str[-1] #截取倒数第一个字符
print str[::-1] #创造一个与原字符串顺序相反的字符串
print str[-3:-1] #截取倒数第三位与倒数第一位之前的字符
print str[-3:] #截取倒数第三位到结尾
print str[:-5:-3] #逆序截取，具体啥意思没搞明白？
'''
def get_lg_company_info(html):
    soup=BeautifulSoup(html)
    #print soup.prettify().encode("GB18030");
    #logo=soup.find_all(id='logoShow')
    logo_url= soup.find('div',class_='top_info_wrap').img['src']
    pos = logo_url[::-1].index('/')
    logo_name=logo_url[-pos:]
    if logo_name=='logo_default.png':
    	logo_url=''
    	logo_name=''
    name_tag=soup.find('h1',class_='ellipsis').a
    short_name=name_tag.string.strip()
    full_name=name_tag['title']
    link=''
    try:
        link=name_tag['href']
    except KeyError:
        print 'KeyError'
    short_description=soup.find('div',class_='company_word clear').string.strip()
    full_description=soup.find('div',class_='company_intro_text').get_text().strip()
    tag_list=soup.find_all('li',class_='con_ul_li')
    tag=''
    for item in tag_list:
        tag+='#'
        tag+=item.string.strip()
    some_list=soup.find('ul',class_='info_list_with_icon').find_all('span')
    field=some_list[0].string
    financing_stage=some_list[1].string
    scale=some_list[2].string
    city=some_list[3].string
    founders_list=soup.find_all('li',class_='item_has  manager_list_now ')
    #print founders_list
    founders=''
    for item in founders_list:
        founders+='#'
        for line in item.stripped_strings:
            founders+='$'
            founders+=line
    #print founders
    news=''
    jobs=soup.find('div',class_='company_navs_wrap').ul.get_text().strip()[-2]
    #print jobs
    #info['url_id']
    info={}
    info['logo_name']=str(logo_name).decode('utf8')
    info['logo_url']=str(logo_url).decode('utf8')
    info['short_name']=str(short_name).decode('utf8')
    info['full_name']=str(full_name).decode('utf8')
    info['short_description']=str(short_description).decode('utf8')
    info['full_description']=str(full_description).decode('utf8')
    info['tag']=str(tag).decode('utf8')
    info['city']=str(city).decode('utf8')
    info['field']=str(field).decode('utf8')
    info['scale']=str(scale).decode('utf8')
    info['link']=str(link).decode('utf8')
    info['financing_stage']=str(financing_stage).decode('utf8')
    info['founders']=str(founders).decode('utf8')
    info['news']=str(news).decode('utf8')
    info['jobs']=str(jobs).decode('utf8')
    return info

def getJobInfo(html,space):
    soup=BeautifulSoup(html)
    company_url_id=''
    try:
        company_url=soup.find('dl',class_='job_company').dt.a['href']
        company_url_reverse=company_url[::-1]
        pos1=company_url_reverse.index('/')
        pos2=company_url_reverse.index('.')
        company_url_id=company_url[-pos1:-pos2-1]
    except AttributeError:
        #print 'company_url_id:AttributeError'
        company_url_id='0'
    publisher=''
    try:
        publisher=soup.find('span',class_='name').get_text()+'#'+soup.find('span',class_='pos').get_text()
    except AttributeError:
        pass
        #print 'publisher:AttributeError'
    job_name=soup.find('dt',class_='clearfix join_tc_icon').h1['title']
    hire_department=soup.find('dt',class_='clearfix join_tc_icon').div.get_text()
    some_list=soup.find('dd',class_='job_request').stripped_strings
    salary=''
    tag=''
    attraction=''
    publish_date=''
    count=0
    for line in some_list:
        if count==0:
            salary=line
        elif count<5:
            tag+='#'
            tag+=line
        elif count==5:
            attraction=line[7:]
        else:
            publish_date=line[5:]
        count+=1
    if len(publish_date)==10:
        pass
    elif len(publish_date)==5:
        publish_data='2015-06-05'
    elif len(publish_date)==7:
        publish_date='2015-06-07'
    else:
        pass
    description=soup.find('dd',class_='job_bt').get_text().strip()[4:].strip().replace(space,'')
    address=''
    try:
        address=soup.find('dl',class_='job_company').dd.div.get_text().strip()
    except AttributeError:
        pass
        #print 'address:AttributeError'
    available=0
    try:
        soup.find('a',class_='btn fr btn_sended').get_text()
    except AttributeError:
        available=1
    info={}
    info['available']=str(available).decode('utf8')
    info['company_url_id']=str(company_url_id).decode('utf8')
    info['publish_date']=str(publish_date).decode('utf8')
    info['publisher']=str(publisher).decode('utf8')
    info['job_name']=str(job_name).decode('utf8')
    info['hire_department']=str(hire_department).decode('utf8')
    info['address']=str(address).decode('utf8')
    info['salary']=str(salary).decode('utf8')
    info['tag']=str(tag).decode('utf8')
    info['attraction']=str(attraction).decode('utf8')
    info['description']=str(description).decode('utf8')
    return info
    

def test():
    fo_space=open(r'D:\code\spider\lg\space.html')
    html_doc=fo_space.read()
    space=BeautifulSoup(html_doc).div.get_text()
    fo_space.close()
    fo=open(r'D:\code\spider\lg\1.html')
    html_doc=fo.read()
    info=getJobInfo(html_doc,space)
    fo.close()
    print '----------------test  begin------------------'
    print '-------available\n'+info['available']+'\n'
    print '-------company_url_id\n'+info['company_url_id'].encode('GB18030')+'\n'
    print '-------publish_date\n'+info['publish_date'].encode('GB18030')+'\n'
    print '-------publisher\n'+info['publisher'].encode('GB18030')+'\n'
    print '-------job_name\n'+info['job_name'].encode('GB18030')+'\n'
    print '-------hire_department\n'+info['hire_department'].encode('GB18030')+'\n'
    print '-------address\n'+info['address'].encode("GB18030")+'\n'
    print '-------salary\n'+info['salary'].encode('GB18030')+'\n'
    print '-------tag\n'+info['tag'].encode('GB18030')+'\n'
    print '-------attraction\n'+info['attraction'].encode('GB18030')+'\n'
    print '-------description\n'+info['description'].encode('GB18030')+'\n'
    print '----------------test  end------------------'

def jobHtml2sql():
    fo=open(r'D:\code\spider\lg\space.html')
    html_doc=fo.read()
    space=BeautifulSoup(html_doc).div.get_text()
    fo.close()
    try:
        conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='mapc',port=3306,charset="utf8")
        cur=conn.cursor()
        address=open(r'D:\code\spider\lg\address4.txt','ab')
        info={}
        file_name=''
        for id in range(600000,753161):
            print id
            if id<700000:
                file_name=r'D:\code\spider\lg\job\60\\'+str(id)+'.html'
            else:
                file_name=r'D:\code\spider\lg\job\70\\'+str(id)+'.html'
            fo=None
            try:
                fo=open(file_name)
            except IOError:
                #print 'file not exist'
                continue
            if fo:
                html_doc=fo.read()
                info=getJobInfo(html_doc,space)
                fo.close()

            if info['address']!='':
                address.write(info['company_url_id']+' '+info['address']+'\n')

            info['url_id']=id

            cur.execute("insert into mapc_job_lg \
                (url_id,company_url_id,available,publish_date,publisher,job_name,hire_department,\
                    salary,address,tag,attraction,description) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",\
                (info['url_id'],\
                    info['company_url_id'],\
                    info['available'],\
                    info['publish_date'],\
                    info['publisher'],\
                    info['job_name'],\
                    info['hire_department'],\
                    info['salary'],\
                    info['address'],\
                    info['tag'],\
                    info['attraction'],\
                    info['description']\
                ))
        address.close()
        cur.close()
        conn.close()
    
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def lg_company_html_2_sql():
    try:
        conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='mapc',port=3306,charset="utf8")
        cur=conn.cursor()
        address=open(r'D:\code\spider\lg\address.txt','ab')
        info={}
        for id in range(60000,80000):
            print 'begin'+str(id)
            file_name=r'D:\code\spider\lg\c\\'+str(id)+'.html'
            try:
                file_size=os.path.getsize(file_name)
            except WindowsError:
                print 'file not exist'
                #not_exist.write(str(id)+'\n')
                continue
            if file_size<10000:
                continue
            fo=open(file_name)
            html_doc=fo.read()
            fo.close()
            info=get_lg_company_info(html_doc)

            if info['logo_url']!='':
                flogo.write(info['logo_url']+'\n')

            info['url_id']=id

            cur.execute("insert into mapc_company_lg \
                (url_id,jobs,logo_name,logo_url,short_name,full_name,short_description,city,\
                    field,scale,link,financing_stage,tag,founders,news,full_description) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",\
                (info['url_id'],\
                    info['jobs'],\
                    info['logo_name'],\
                    info['logo_url'],\
                    info['short_name'],\
                    info['full_name'],\
                    info['short_description'],\
                    info['city'],\
                    info['field'],\
                    info['scale'],\
                    info['link'],\
                    info['financing_stage'],\
                    info['tag'],\
                    info['founders'],\
                    info['news'],\
                    info['full_description']\
                ))

            #print "ID of last record is ", int(cur.lastrowid) #最后插入行的主键ID  
            #print "ID of inserted record is ", int(conn.insert_id()) #最新插入行的主键ID，conn.insert_id()一定要在conn.commit()之前，否则会返回0  
        address.close()

        cur.close()
        conn.close()
    
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


def get_itjuzi_company_info(html):
    soup=BeautifulSoup(html)
    company_url_id=''
    financing_needs_tag=soup.find_all(id='company-fund-status')
    financing_needs=''
    financing_stage=''
    if len(financing_needs_tag)==1:
        financing_stage=financing_needs_tag[0].get_text().strip()
    elif len(financing_needs_tag)==2:
        financing_needs=financing_needs_tag[0].get_text().strip()
        financing_stage=financing_needs_tag[1].get_text().strip()
    logo_url_tag=soup.find('div',class_='archive-logo pull-left')
    logo_url=''
    logo_name=''
    if logo_url_tag:
        logo_url=logo_url_tag.img['src'].strip()
        logo_url_reverse=logo_url[::-1]
        pos=logo_url_reverse.index('/')
        logo_name=logo_url[-pos:]
    name_tag=soup.find('div',class_='public-info pull-left')
    short_name=name_tag.find(id='com_id_value').get_text().strip()
    full_name=name_tag.find('p',class_='dark').get_text().strip()
    link=name_tag.find('b').get_text().strip()
    info_tag=soup.find('ul',class_='detail-info').find_all('li')
    founding_time=''
    area=''
    status=''
    stage=''
    sector=''
    sub_sector=''
    tag=''
    short_description=''
    for item in info_tag:
        item_str=item.get_text().strip()
        pos=item_str.index(':')
        name=item_str[:pos]
        content=item_str[pos+1:].strip()
        #print name,content
        if name=='时间':
            founding_time=content
        elif name=='地点':
            area=content
        elif name=='状态':
            status=content
        elif name=='阶段':
            stage=content
        elif name=='行业':
            sector=content.replace(',','#').replace(' ','')
        elif name=='子行业':
            sub_sector=content.replace(',','#').replace(' ','')
        elif name=='TAG':
            tag=content.replace(',','#').replace(' ','')
        elif name=='简介':
            short_description=content
    news_tag=soup.find(id='company-new-list')
    news=''
    if news_tag:
        news_tag=news_tag.find_all('li')
        news_tag.pop()
        for item in news_tag:
            time=item.find('b',class_='company-new-list-news-tit pull-left').get_text().strip().replace(' ','')
            title=item.find('a',class_='pull-left').get_text().strip()
            news_link=item.find('a',class_='pull-left')['href']
            tag_tag=item.find_all('a',class_='btn btn-gray')
            news_item_tag=''
            for i in tag_tag:
                news_item_tag+='@'
                news_item_tag+=i.get_text().strip()
            news+='$'
            news+='#'+time+'#'+title+'#'+news_link+'#'+news_item_tag
    founders_tag=soup.find(id='company-member-list-tbl')
    founders=''
    if founders_tag:
        founders_tag=founders_tag.find_all('tr')
        for item in founders_tag:
            item=item.find_all('td')
            item_name=item[1].get_text().strip()
            item_position=item[2].get_text().strip()
            item_weibo_tag=item[3].a
            item_weibo_link=''
            if item_weibo_tag:
                item_weibo_link=item_weibo_tag['href']
            founders+='$'
            founders+='#'+item_name+'#'+item_position
            if item_weibo_link!='':
                founders+='#'+item_weibo_link
    milestones_tag=soup.find(id='company-mile')
    milestones=''
    if milestones_tag:
        if milestones_tag.parent.h2.get_text().strip()[-3:]=='里程碑':
            milestones_tag=milestones_tag.find_all('li')
            for item in milestones_tag:
                item_time=item.b.get_text().strip()
                item_title=item.p.get_text().strip()
                milestones+='$'
                milestones+='#'+item_time+'#'+item_title
    investments_tag=soup.find_all('div',class_='company-fund-item')
    investments=''
    if investments_tag:
        for item in investments_tag:
            item_turn=item.h3.b.get_text().strip()
            item_time=item.h3.get_text().strip()
            item_time=item_time[item_time.index(' ')+1:].strip()
            item_num=item.p.a.get_text().strip()
            item_investor_tag=item.find_all('p')[1].find_all('a')
            item_investor=''
            for i in item_investor_tag:
                item_investor+='@'+i.get_text().strip()
            investments+='$'
            investments+='#'+item_turn+'#'+item_time+'#'+item_num+'#'+item_investor
    info={}
    info['financing_needs']=str(financing_needs).decode('utf8')
    info['logo_name']=str(logo_name).decode('utf8')
    info['logo_url']=str(logo_url).decode('utf8')
    info['short_name']=str(short_name).decode('utf8')
    info['full_name']=str(full_name).decode('utf8')
    info['link']=str(link).decode('utf8')
    info['founding_time']=str(founding_time).decode('utf8')
    info['area']=str(area).decode('utf8')
    info['status']=str(status).decode('utf8')
    info['stage']=str(stage).decode('utf8')
    info['sector']=str(sector).decode('utf8')
    info['sub_sector']=str(sub_sector).decode('utf8')
    info['financing_stage']=str(financing_stage).decode('utf8')
    info['tag']=str(tag).decode('utf8')
    info['short_description']=str(short_description).decode('utf8')
    info['founders']=str(founders).decode('utf8')
    info['milestones']=str(milestones).decode('utf8')
    info['news']=str(news).decode('utf8')
    info['investments']=str(investments).decode('utf8')
    return info


def itjuzi_company_html_2_sql():
    try:
        conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='test',port=3306,charset="utf8")
        cur=conn.cursor()
        itjuzi_logo_url=open(r'E:\itjuzi_logo_url.txt','ab')
        #itjuzi_logo_url=open('/home/hwz/spider/itjuzi_logo_url.txt','ab')
        info={}
        file_name=''
        for id in range(10000,22634):
            print id
            file_name=r'E:\itjuzi\\'+str(id)+'.html'
            #file_name='/home/hwz/spider/itjuzi/'+str(id)+'.html'
            fo=None
            try:
                fo=open(file_name)
            except IOError:
                print 'file not exist'
                continue
            if fo:
                html_doc=fo.read()
                info=get_itjuzi_company_info(html_doc)
                fo.close()

            info['url_id']=id
            if info['logo_url']!='':
                itjuzi_logo_url.write(str(id)+' '+info['logo_url']+'\n')

            cur.execute("insert into mapc_company_itjuzi \
                (url_id,financing_needs,logo_name,logo_url,short_name,full_name,\
                    link,founding_time,area,status,stage,sector,sub_sector,financing_stage,\
                    tag,short_description,founders,milestones,news,investments) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",\
                (info['url_id'],\
                    info['financing_needs'],\
                    info['logo_name'],\
                    info['logo_url'],\
                    info['short_name'],\
                    info['full_name'],\
                    info['link'],\
                    info['founding_time'],\
                    info['area'],\
                    info['status'],\
                    info['stage'],\
                    info['sector'],\
                    info['sub_sector'],\
                    info['financing_stage'],\
                    info['tag'],\
                    info['short_description'],\
                    info['founders'],\
                    info['milestones'],\
                    info['news'],\
                    info['investments']\
                ))
        itjuzi_logo_url.close()
        cur.close()
        conn.close()
    
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def test_itjuzi_company():
    fo=open(r'E:\itjuzi\3.html')
    html_doc=fo.read()
    info=get_itjuzi_company_info(html_doc)
    fo.close()
    print '----------------test  begin------------------'
    for key,value in info.items():
            print '-------'+key+'---'+str(len(value))+'\n'+value.encode('GB18030')+'\n'
    print '----------------test  end------------------'

if __name__=='__main__':
    reload(sys)
    sys.setdefaultencoding( "utf-8" )
    test_itjuzi_company()
