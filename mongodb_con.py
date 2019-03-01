# coding: utf-8
'''
Created on 2018年11月26日

@author: guimaizi
'''
import config,time
from pymongo import MongoClient
class mongodb_con:
    def __init__(self):
        self.config_main=config.config()
        '''
            常用mongodb指令：
            db.qq_com.find({"url":/.*Cookie*./}) 
            db.qq_com.find({"state":"0"}) .limit(10)
            db.qq_com.update({ "state" : {$ne:0}} ,{$set:{"state":0}},false,true)
        '''
        self.client = MongoClient(self.config_main.callback_mongo_config()['ip'], self.config_main.callback_mongo_config()['port'])
        self.db_target_domain = self.client.domain
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
            collection.insert(data,manipulate=True)
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
        return collection.find({"state":0}, { "id": 1, "domain": 1 }).limit(limt)
    def callback_list_all_url(self,domain,limt):
        '''
        return 数据库里所有的url_list
        :domain 数据库名
        :limt 条数
        '''
        domain=domain.replace('.','_')
        collection = self.db_target_domian[domain]
        return collection.find({},{ "id": 1, "url": 1 }).limit(limt)
    def callback_all_list(self,domain,limt):
        '''
        return 数据库里所有的数据
        :domain 数据库名
        :limt 条数
        '''
        domain=domain.replace('.','_')
        collection = self.db_target_domain[domain]
        return collection.find({}).limit(limt)
    def callback_update(self,Domain,list_url_data):
        Domain=Domain.replace('.','_')
        collection = self.db_target_domain[Domain]
        for data in list_url_data:
            try:
                len_data=collection.find({"domain":data['domain']}, {"html_size": 1 })[0]['html_size']
                #len_data=collection.find({"url":"http://z.qq.com"}, {"html_size": 1 })[0]['html_size']
                if len_data/data['html_size']>=1.2 or len_data/data['html_size']<=0.8:
                    print(data)
                    collection.update_one({"domain": data['domain']},{"$set": {"state": 1,"html_size":data['html_size'],"title":data['title'],"time":time.strftime('%Y-%m-%d',time.localtime())}})
                else:
                    collection.update_one({"domain": data['domain']},{"$set": {"state": 1}})
            except:collection.update_one({"domain": data['domain']},{"$set": {"state": 1}})
    def update_date(self,Domain,url):
        Domain=Domain.replace('.','_')
        collection = self.db_target_domain[Domain]
        collection.update_one({"domain": url},{"$set": {"state": 1}})
    def update_all_date(self,Domain):
        print(Domain)
        Domain=Domain.replace('.','_')
        collection = self.db_target_domain[Domain]
        collection.update({ "state":{"$ne":0}} ,{"$set":{"state":0}},multi=True)
    def close(self):
        self.client.close()
if '__main__' == __name__:
    p=mongodb_con()
    p.into_target('aaaa', {"aaaaa":1})
    '''
    f=open('qq.txt','a',encoding='UTF-8')
    for i in p.callback_all_list('.qq.com',3000):
        f.write(str(i)+'\n')
    f.close()
    '''