# coding: utf-8
'''
Created on 2018年11月26日

@author: guimaizi
'''
import config,Browser,mongodb_con,os,threading
class start:
    def __init__(self):
        '''
        :开始扫描收集域名
        '''
        self.config_main=config.config()
        self.data=[]
    def get_data(self,list_url):
        #开始访问获取http响应
        try:
            Browsers=Browser.Browser()
            mongodb=mongodb_con.mongodb_con()
            for url in list_url:
                data=Browsers.callback_spider_data(url)
                if data!=False:
                    mongodb.into_target(self.config_main.callback_domain(),data)
                    self.data.extend(Browsers.callback_data())
        finally:
            Browsers.close()
            mongodb.close()
    def while_read(self):
        #读取href network_url进行处理
        while 1: 
            data=self.config_main.callback_tmp_list()
            if data!=[]:
                self.control(data)
            else:break
            data=[]
    def control(self,list_url):
        list_url=list(set([self.config_main.callback_split_domain(url, 1) for url in list_url if self.config_main.callback_Detection_domain(url)]))
        mongodb=mongodb_con.mongodb_con()
        list_url=[url for url in list_url if mongodb.find(self.config_main.callback_domain(),url)==0 and self.config_main.fitle(url)==True]
        mongodb.close()
        if len(list_url)>=60:
            list_url_ready_first=[]
            list_url_ready_action=[]
            for url in list_url:
                list_url_ready_first.append('http://%s'%url)
                if len(list_url_ready_first)==10:
                    list_url_ready_action.append(list_url_ready_first)
                    list_url_ready_first=[]
                if len(list_url_ready_action)==5:
                    self.config_main.threading_start(self.get_data,list_url_ready_action)
                    self.config_main.write(self.data)
                    self.data=[]
                    list_url_ready_action=[]    
            self.config_main.threading_start(self.get_data,list_url_ready_action)
            self.config_main.write(self.data)
            self.data=[]
            list_url_ready_action=[]
        else:
            list_url_ready=[]
            for url in list_url:
                list_url_ready.append('http://%s'%url)
                if len(list_url_ready)>=12:
                    self.get_data(list_url_ready)
                    list_url_ready=[]
            self.get_data(list_url_ready)
            self.config_main.write(self.data)
            self.data=[]
            list_url_ready=[]
    def subfind(self):
        str=self.config_main.callback_domain()
        filename=str.replace('.','_')+'.txt'
        os.system('subfinder.exe -d %s -o %s'%(str[1:len(str)],filename))
        self.control((self.config_main.import_domain_txt(filename)))
        os.remove(filename)
        item.while_read()
if __name__ == '__main__':
    item=start()
    item.subfind()
    #print(item.import_domain_txt(r'E:\hack\find_domain\qq.txt'))
    #item.control(item.import_domain_txt(r'E:\hack\find_domain\qq.txt'))
    #item.while_read()