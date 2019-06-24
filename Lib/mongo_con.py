# coding: utf-8
'''
Created on a

@author: guimaizi
'''
import json,time
from Lib import fun_all
from pymongo import MongoClient
class mongo_con:
    def __init__(self):
        self.config_main=fun_all.fun_all()
        self.client = MongoClient(self.config_main.callback_mongo_config()['ip'], self.config_main.callback_mongo_config()['port'])
        self.db_target_domain = self.client.domain
        if self.config_main.callback_mongo_config()['name']!='':
            self.db_target_domain.authenticate(self.config_main.callback_mongo_config()['name'], self.config_main.callback_mongo_config()['password'])
    def into_target(self,domain,data):
        try:
            '''
            data数据写入
            :domain 数据库名
            :data 数据
            '''
            domain=domain.replace('.','_')
            collection = self.db_target_domain[domain]
            collection.insert_many(data)
        except Exception as e:
            print(e)
    def find(self,domain,url):
        '''
        url 是否存在
        :domain 数据库名
        :url 数据
        '''
        domain=domain.replace('.','_')
        collection = self.db_target_domain[domain]
        return collection.find({"domain": "%s"%url}).count()
    def callback_list_url(self,domain,limt):
        '''
        return 数据库里的state参数为0的url_list
        :domain 数据库名
        :limt 条数
        '''
        domain=domain.replace('.','_') 
        collection = self.db_target_domain[domain]
        return collection.find({"status":0}, { "id": 1, "domain": 1 }).limit(limt)
    def update_date(self,domain,url):
        domain=domain.replace('.','_')
        collection = self.db_target_domain[domain]
        collection.update_one({"domain": url},{"$set": {"status": 1}})
    def callback_update(self,domain,list_url_data):
        domain=domain.replace('.','_')
        collection = self.db_target_domain[domain]
        for data in list_url_data:
            try:
                len_data=collection.find({"domain":data['domain']}, {"http_length": 1 })[0]['http_length']
                #len_data=collection.find({"url":"http://z.qq.com"}, {"html_size": 1 })[0]['html_size']
                if len_data/data['http_length']>=1.2 or len_data/data['http_length']<=0.8:
                    print(data)
                    collection.update_one({"domain": data['domain']},{"$set": {"status": 1,"http_length":data['http_length'],"title":data['title'],"time":time.strftime('%Y-%m-%d',time.localtime())}})
                else:
                    collection.update_one({"domain": data['domain']},{"$set": {"status": 1}})
            except:collection.update_one({"domain": data['domain']},{"$set": {"status": 1}})
    def update_all_date(self,domain):
        #更新全部数据status为1
        domain=domain.replace('.','_')
        collection = self.db_target_domain[domain]
        collection.update({ "state":{"$ne":0}} ,{"$set":{"status":0}},multi=True)
    def exit_mongo(self):
        self.client.close()
if '__main__' == __name__:
    item=mongo_con()
    item.into_target('adasdas', [{"aa":"dasddasdass1a"}])