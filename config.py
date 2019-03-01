# coding: utf-8
'''
Created on 2018年11月13日

@author: guimaizi
'''
import urllib,re,os,json,threading
class config:
    def __init__(self):
        '''
        domain.json
        {
        #domain 格式:.domain.com
        "domain":"domain",
        "Blacklist_domain":[
            ]
        }
        
        '''
        #域名配置文件
        self.tar_config='target/qq.json'
        #当前代码目录
        self.path='E:/source_code/get_domain'
        with open('%s/%s'%(self.path,self.tar_config),'r') as load_f:
            load_dict = json.load(load_f)
        self.domain=load_dict['domain']
        self.Blacklist_domain=load_dict['Blacklist_domain']
        #chrome路径
        self.chrome_path=r'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    def callback_mongo_config(self):
    	#mongodb连接配置
        return {"ip":"127.0.0.1","port":27017,"name":"target","password":"11111"}
    def callback_chrome_path(self):
        #返回chrome路径
        return self.chrome_path
    def callback_path(self):
        #返回绝对路径
        return self.path
    def callback_domain(self):
        #返回目标域名
        return self.domain
    def callback_split_domain(self,url,type):
        '''
        callback domain 
        :type 0 http?s://www.xxx.com 1 www.xxx.com
        '''
        try:
            url=urllib.parse.urlparse(url)
            if type==0:
                return url.scheme+'://'+url.netloc
            elif type==1:
                return url.netloc
        except:return False
    def callback_Detection_domain(self,url):
        #过滤域名
        domain=re.sub('\.','\\.',self.domain)
        #print(domain)
        if re.match('^(https|http):\/\/(.*)(%s)$'%domain, url):
            return True
        else:return False 
    def callback_tmp_list(self):
        #返回href network url数据
        try:
            list_url=[]
            for i in open(r"{path}/tmp/url_tmp.txt".format(path=self.path)):
                list_url.append(i.strip())
            os.remove(r"{path}/tmp/url_tmp.txt".format(path=self.path))
            return list(set(list_url))
        except:return []
    def del_tmp(self):
        os.remove(r"{path}/tmp/url_tmp.txt".format(path=self.path))
    def fitle(self,url):
        #黑名单过滤
        for j in self.Blacklist_domain:
            if j  in url:
                return False
        return True
    def write(self,data):
        f=open(r'%s/tmp/url_tmp.txt'%self.callback_path(),'a')
        for i in data:
            f.write(i+'\n')
        f.close()
    def import_domain_txt(self,filename):
        try:
            filename='%s'%filename
            list_url=[]
            for i in open(filename):
                list_url.append('http://%s'%i.strip())
            #os.remove(filename)
            return list(set(list_url))
        except:return []
    def threading_start(self,fun,list_url):
            tsk = [threading.Thread(target=fun,args=(k,)) for k in list_url] 
            [ks.start() for ks in tsk]
            [ks.join() for ks in tsk]
if __name__ == '__main__':
    item=config()
    print(item.callback_domain())