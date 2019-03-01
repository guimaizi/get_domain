# coding: utf-8
'''
Created on 2019年2月16日

@author: guimaizi
'''
import dns.resolver,requests,random,queue,time,threadpool,config,mongodb_con,Browser
from pymongo import MongoClient
from bs4 import BeautifulSoup
class random_start:
    def __init__(self):
        '''
        :domian 子域名收集
        '''
        self.config_main=config.config()
        self.domain=self.config_main.callback_domain()
        #超时
        self.timeout=5
        #线程数
        self.thread_num=100
        self.domain_list=[]
        self.result=[]
        #每次任务标记
        self.random=self.generate_random_str(16)
    def generate_random_str(self,randomlength):
        """
        :randomlength 生成一个指定长度的随机字符串
        """
        random_str = ''
        base_str = 'abcdefghigklmnopqrstuvwxyz0123456789.'
        length = len(base_str) - 1
        for i in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str

    def query(self,domain):
        '''
        dns查询存在域名
        '''
        myResolver = dns.resolver.Resolver()
        myResolver.nameservers = ['8.8.8.8', '8.8.4.4']

        try:
                myAnswers = myResolver.query(domain, "A")
                self.domain_list.append(domain)
        except Exception as e:print(e)
    def get_http(self,domain):
        '''
        http获取:
        {"domain":domain,"url":target_url,"status_code":"%s"%str(r.status_code),"size_html":len(r.text),"title":"%s"%str(self.get_title(r.text)),"mark":self.random,"time":time.strftime('%Y-%m-%d',time.localtime())}
        '''
        try:
            kv={'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
            target_url='http://'+domain
            r = requests.get(target_url,headers=kv,timeout=self.timeout)
            r.encoding='utf-8'
            data={"domain":domain,"url":target_url,"status_code":"%s"%str(r.status_code),"size_html":len(r.text),"title":"%s"%str(self.get_title(r.text)),"mark":self.random,"time":time.strftime('%Y-%m-%d',time.localtime())}
            print(data)
            self.result.append(data)
        except Exception as e:print(e)
    def get_title(self,html):
        '''
        返回title
        '''
        try:
            soup = BeautifulSoup(html, 'html5lib')
            title = soup.find('title')
            return title
        except:
            return 'not'
    def save_result(self,data_list):
        '''
        #保存数据
        :filename 文件路径及文件名
        :data_list list数据
        '''
        domain=self.domain.replace('.','_')
        f=open('%s.txt'%domain,'a',encoding='utf-8')
        for i in data_list:
            f.write('%s\n'%str(i))
        f.close()
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
    def run(self,list_str):
        #去重
        #print(list_str)
        mongodb_cons=mongodb_con.mongodb_con()
        list_domain=[]
        for i in list_str:
            i=i+self.domain
            #print(i)
            if mongodb_cons.find(self.config_main.callback_domain(),i)==0 and self.config_main.fitle (i):
                list_domain.append(i)
        
        #print(list_domain)
        #运行
        self.threadpool_fun(self.query, list_domain, self.thread_num)
        time.sleep(self.timeout)
        try:
            Browsers=Browser.Browser()
            for url in self.domain_list:
                print('http://%s'%url)
                data=Browsers.callback_spider_data('http://%s'%url)
                print(data)
                if data!=False:
                    mongodb_cons.into_target(self.config_main.callback_domain(),data) 
        finally:Browsers.close()          
    def random_str(self):
        list_str=[]
        for i in range(100):
            list_str.append(self.generate_random_str(random.randint(1,10)))
        #运行
        self.run(list(set(list_str)))
if __name__=="__main__":
    #while 1:
        try:
            item=random_start() 
            item.random_str()
        except Exception as e:
            print(e)
            #continue