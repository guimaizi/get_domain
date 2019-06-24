# coding: utf-8
'''
Created on 2019��6��19��

@author: guimaizi
'''
from Lib import mongo_con
from Lib import fun_all
from Lib import dispatch_main
class while_update:
    def __init__(self):
        #资产监控
        self.dispatch_main=dispatch_main.dispatch_main()
        self.config_main=fun_all.fun_all()
        mongodb=mongo_con.mongo_con()
        mongodb.update_all_date(self.config_main.callback_domain())
        mongodb.exit_mongo()
    def get_domain(self):
        mongodb=mongo_con.mongo_con()
        #list_domain=[i['domain'] for i in mongodb.callback_list_url(self.config_main.callback_domain(), 100) ]
        list_domain=[]
        for url in mongodb.callback_list_url(self.config_main.callback_domain(), 120):
            mongodb.update_date(self.config_main.callback_domain(), url['domain'])
            list_domain.append(url['domain'])
        mongodb.exit_mongo()
        return list_domain
    def start_update(self):
        #开始发现新域名
        while 1:
            list_data=self.get_domain()
            if list_data==[]:break
            self.dispatch_main.control(list_data)
            mongodb=mongo_con.mongo_con()
            mongodb.callback_update(self.config_main.callback_domain(), self.dispatch_main.callback_result())
            list_domain=[]
            for url in self.dispatch_main.callback_domain():
                if self.config_main.callback_detection_domain('http://'+url) and mongodb.find(self.config_main.callback_domain(), url)==0:
                    list_domain.append(url)
            mongodb.exit_mongo()
            self.run(list_domain)
            list_data=[]
    def run(self,list_domain):
        #开始获取域名
        while 1:
            self.dispatch_main.control(list_domain)
            result_data=self.dispatch_main.callback_result()
            mongodb=mongo_con.mongo_con()
            mongodb.into_target(self.config_main.callback_domain(), result_data)
            mongodb.exit_mongo()
            while_data=self.dispatch_main.callback_domain()
            list_domain=[]
            mongodb=mongo_con.mongo_con()
            for url in while_data:
                if self.config_main.callback_detection_domain('http://'+url) and mongodb.find(self.config_main.callback_domain(), url)==0:
                    list_domain.append(url)
            mongodb.exit_mongo()
            if list_domain==[]:break
    
if '__main__' == __name__:
    item=while_update()
    item.start_update()