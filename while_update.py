# coding: utf-8
'''
Created on 2018年12月6日

@author: guimaizi
'''
import config,Browser,mongodb_con,start
class while_update:
    def __init__(self):
        '''
        :域名监控
        '''
        self.config_main=config.config()
        mongodb=mongodb_con.mongodb_con()
        mongodb.update_all_date(self.config_main.callback_domain())
        mongodb.close()
        self.data=[]
        self.contrast_data=[]
    def get_data(self,list_url):
        #开始访问获取http响应
        #print(list_url)
        try:
            Browsers=Browser.Browser()
            mongodb=mongodb_con.mongodb_con()
            for url in list_url:
                data=Browsers.callback_spider_data(url)
                print(data)
                if data!=False and mongodb.find(self.config_main.callback_domain(),self.config_main.callback_split_domain(url, 1))==0:
                    mongodb.into_target(self.config_main.callback_domain(),data)
                    self.data.extend(Browsers.callback_data())
                elif data!=False:
                    self.contrast_data.append(data)
                    self.data.extend(Browsers.callback_data())
        finally:
            Browsers.close()
            mongodb.close()
    def control(self,list_url):
        #控制中心
        print(list_url)
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
        self.contrast()
    def contrast(self):
        #对比更新
        mongodb=mongodb_con.mongodb_con()
        mongodb.callback_update(self.config_main.callback_domain(), self.contrast_data)
        mongodb.close()
        import_data=start.start()
        import_data.while_read()
        self.contrast_data=[]
    def start(self):
        #开始检测域名变化
        while 1:
            mongodb=mongodb_con.mongodb_con()
            list_url=[url['domain'] for url in mongodb.callback_list_url(self.config_main.callback_domain(), 60)]
            if list_url==[]:
                break
            [mongodb.update_date(self.config_main.callback_domain(), i) for i in list_url]
            self.control(list_url)
            mongodb.close()
if __name__ == '__main__':
    item=while_update()
    item.start()
        