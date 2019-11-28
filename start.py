# coding: utf-8
'''

@author: guimaizi
'''
from Lib import mongo_con
from Lib import fun_all
from Lib import dispatch_main
import os,sys,while_update
class start:
    def __init__(self):
        self.dispatch_main=dispatch_main.dispatch_main()
        self.config_main=fun_all.fun_all()
    def import_domain(self,list_domain):
        #导入域名list 格式['dsad.qq.com']
        list_domain=list(set(list_domain))
        mongodb=mongo_con.mongo_con()
        list_domain_start=[]
        for url in list_domain:
            if self.config_main.callback_detection_domain('http://'+url) and mongodb.find(self.config_main.callback_domain(), url)==0:
                list_domain_start.append(url)
        mongodb.exit_mongo()
        self.run(list(set(list_domain_start)))
    def import_url(self,list_domain):
        #导入URL list 格式['http://dsad.qq.com/dsadsa']
        list_domain=list(set(list_domain))
        mongodb=mongo_con.mongo_con()
        list_domain_start=[]
        for url in list_domain:
            if self.config_main.callback_detection_domain(url) and mongodb.find(self.config_main.callback_domain(), self.config_main.callback_split_domain(url, 1))==0:
                list_domain_start.append(self.config_main.callback_split_domain(url, 1))
        mongodb.exit_mongo()
        #print(list(set(list_domain_start)))
        self.run(list(set(list_domain_start)))
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
    def subfind(self):
        strs=self.config_main.callback_domain()
        filename=strs.replace('.','_')+'.txt'
        os.system('/Users/guimaizi/go/bin/subfinder -d %s -o %s'%(strs[1:len(strs)],filename))
        #print(filename)
        self.import_domain(self.config_main.import_domain_txt(filename))
        os.remove(filename)
    def log_main(self):
        log_main='''
        project:get_domain V3.0
        
        -s start get the domain list
        -u update all domain data and find new domain
        -i {filename.txt} import domain_list file type txt
        -iurl {filename.txt} import url_list file type txt
        ''' 
        print(log_main)
    def start(self):
        self.log_main()
        wage = sys.argv[1]
        if wage=='-s':
            self.subfind()
        elif wage=='-u':
            while_updates=while_update.while_update()
            while_updates.start_update()
        elif wage=='-i':
            wages = sys.argv[2]
            #print(wages)
            self.import_domain(self.config_main.import_domain_txt(wages))
        elif wage=='-iurl':
            wages = sys.argv[2]
            self.import_url(self.config_main.import_domain_txt(wages))
        else:print('input error,Please try again.')
if '__main__' == __name__:
    item=start()
    item.start()
    #item.import_domain(list_domain)
    #item.subfind() 