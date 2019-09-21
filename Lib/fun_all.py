# coding: utf-8
'''

@author: guimaizi
'''
import re,os,json,threading,queue,threadpool,sys
from urllib.parse import urlparse
from pip._vendor.html5lib.treebuilders import dom
class fun_all:
    def __init__(self):
        main_path='/Users/guimaizi/eclipse-workspace/get_domain/config.json'
        with open(main_path,'r') as load_f:
            self.load_dict = json.load(load_f)
        with open(self.load_dict['target_json'],'r') as load_f:
            self.domain_dict = json.load(load_f)
        self.domain=self.domain_dict['domain']
        self.Blacklist_domain=self.domain_dict['Blacklist_domain']
    def callback_path(self):
        #返回程序路径
        return self.load_dict['path']
    def callback_chrome_path(self):
        #返回chrome路径
        return self.load_dict['chrome_path']
    def callback_mongo_config(self):
        #mongodb连接配置
        return self.load_dict['mongo_config']
    def callback_domain(self):
        #返回目标域名
        return self.domain
    def callback_split_domain(self,url,type):
        '''
        callback domain 
        :type 0 http?s://www.xxx.com 1 www.xxx.com
        '''
        try:
            url=urlparse(url)
            if type==0:
                return url.scheme+'://'+url.netloc
            elif type==1:
                return url.netloc
        except:return False
    def callback_detection_domain(self,url):
        #过滤域名
        url=self.callback_split_domain(url, 1)
        url_list=url.split('.')
        if url!=False and len(url_list)>2:
            url_list=url.split('.')
            #domain='.'+url_list[-2]+'.'+url_list[-1]
            if '.'+url_list[-2]+'.'+url_list[-1]==self.domain and self.fitle(url): 
                return url
        else:return False
    def fitle(self,url):
        #黑名单过滤
        for j in self.Blacklist_domain:
            if j  in url:
                return False
        return True
    def import_domain_txt(self,filename):
        try:
            list_url=[]
            for i in open(filename):
                list_url.append(i.strip())
            #os.remove(filename)
            return list(set(list_url))
        except:return []
    def write(self,data):
        #写文件
        f=open(r'%s/tmp/url_tmp.txt'%self.callback_path(),'a')
        for i in data:
            f.write(i+'\n')
        f.close()
    def del_tmp(self):
        #删文件
        os.remove(r"{path}/tmp/url_tmp.txt".format(path=self.path))
    def threading_start(self,fun,list_url):
            tsk = [threading.Thread(target=fun,args=(k,)) for k in list_url] 
            [ks.start() for ks in tsk]
            [ks.join() for ks in tsk]
    def threadpool_fun(self,fun,lists,num):
        '''
        thread多线程池

        :fun 函数
        :lists 数据
        :num 线程数
        '''
        q = queue.Queue()
        for i in lists:
            q.put(i)
        lst = [q.get() for i in range(q.qsize())]
        pool = threadpool.ThreadPool(num)
        requestss = threadpool.makeRequests(fun, lst)
        [pool.putRequest(req) for req in requestss]
        pool.wait()
        pool.dismissWorkers(num, do_join=True) 
if __name__ == '__main__':
    item=fun_all()
    #item.callback_chrome_path()
    print(item.callback_detection_domain('http://ww.aa.dsada.qq.com/.w.qq.com/?.qq.com'))