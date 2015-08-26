#encoding=utf-8
'''
基于BaseHTTPServer的http server实现，包括get，post方法，get参数接收，post参数接收。
'''
import os,sys
import posixpath
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import io,shutil  
import urllib,time
import getopt,string
import json

class MapRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.get_process()

    def do_POST(self):
        print '--------'
        self.post_process()

    def get_process(self):
        #print self.path
        if self.path in ['/','/index','/index.html']:
            #self.send_response(200)
            path=os.path.join(os.getcwd(), 'index.html')
            f = open(path, 'rb')
            self.wfile.write(f.read())
            f.close()
        else:
            self.send_error(404, "File not found !")

    def post_process(self):
        datas = self.rfile.read(int(self.headers['content-length']))
        #datas = urllib.unquote(datas).decode("utf-8", 'ignore')#指定编码方式
        datas = transDicts(datas)#将参数转换为字典
        #print datas

        if datas['action']=='address':
            self.send_address(datas)

        elif datas['action']=='coordinate':
            # save coordinate
            coordinate_file=open(r'D:\code\spider\lg\coordinate.txt')

            content=json.loads(datas['content'])
            for item in content:
                print item
                #line=item['id']+'X'+item['x']+'Y'+item['y']
                #coordinate_file.write(line+'\n')

            coordinate_file.close()
            # send address
            #self.send_address(datas)
        else:
            print 'request error !'

    def send_address(self,data):
        begin=int(data['begin'])
        end=begin+99
        addr_file=open(r'D:\code\spider\lg\address_sort_one_modify.txt')
        content=[]
        count=0
        for line in addr_file:
            count+=1
            if count<begin:
                continue
            elif count>end:
                break
            item_pos=line.index(' ')
            item_index=line[0:item_pos]
            item_content=line[item_pos+1:].strip()
            content.append({'id':item_index,'address':item_content})
        addr_file.close()
        response_data={}
        if count<=end:
            response_data['end']=1
        else:
            response_data['end']=0
        response_data['content']=content
        #需要以数组的形式返回，以对象的形式返回，客户端json解析会出错
        response_data=[response_data]
        enc="UTF-8" 
        response_data = json.dumps(response_data).encode(enc)
        self.send_response(200)  
        self.send_header("Content-type", "text/html; charset=%s" % enc)  
        self.send_header("Content-Length", str(len(response_data)))  
        self.end_headers()  
        self.wfile.write(response_data)

    def process(self,type):
        
        content =""
        if type==1:#post方法，接收post参数
            datas = self.rfile.read(int(self.headers['content-length']))
            datas = urllib.unquote(datas).decode("utf-8", 'ignore')#指定编码方式
            datas = transDicts(datas)#将参数转换为字典
            if datas.has_key('data'):
                content = "data:"+datas['data']+"\r\n"
        
        print self.path

        if '?' in self.path:
            query = urllib.splitquery(self.path)
            print query
            action = query[0] 
                     
            if query[1]:#接收get参数
                queryParams = {}
                for qp in query[1].split('&'):
                    kv = qp.split('=')
                    queryParams[kv[0]] = urllib.unquote(kv[1]).decode("utf-8", 'ignore')
                    content+= kv[0]+':'+queryParams[kv[0]]+"\r\n"
                    
            #指定返回编码
            enc="UTF-8"  
            content = content.encode(enc)          
            f = io.BytesIO()  
            f.write(content)  
            f.seek(0)  
            self.send_response(200)  
            self.send_header("Content-type", "text/html; charset=%s" % enc)  
            self.send_header("Content-Length", str(len(content)))  
            self.end_headers()  
            shutil.copyfileobj(f,self.wfile)

def transDicts(params):
    dicts={}
    if len(params)==0:
        return
    params = params.split('&')
    for param in params:
        dicts[param.split('=')[0]]=param.split('=')[1]
    return dicts
       
if __name__=='__main__':
    
    try:
        server = HTTPServer(('', 8000), MapRequestHandler)
        print 'started httpserver...'
        server.serve_forever()

    except KeyboardInterrupt:
        server.socket.close()
    
    pass
