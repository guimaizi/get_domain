# coding: utf-8
'''
Created on 2018年11月13日

@author: guimaizi
'''
# coding: utf-8
'''
Created on 2018年5月21日

@author: guimaizi
'''
#import socket,re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time,config
class Browser:
    def __init__(self):
        self.config_main=config.config()
        #浏览器
        chrome_options = Options()
        #headless模式运行
        chrome_options.add_argument('--headless')
        #不加载图片
        chrome_options.add_argument('blink-settings=imagesEnabled=false')
        #调用当前chrome用户数据 cookie登陆方式
        #chrome_options.add_argument(r'user-data-dir=%s'%models.read_config()['chrome_user_data'])
        chrome_options.add_argument('--disable-gpu')
        #chrome_options.add_argument('--hide-scrollbars')
        chrome_options.binary_location = r'%s'%self.config_main.callback_chrome_path()
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.timeout=8
        self.time=time.strftime('%Y-%m-%d',time.localtime())
    def set_cookie(self,url,cookie):
        #js设置cookie
        self.driver.get(url)
        for i in cookie.split(';'):
            self.driver.execute_script("document.cookie = \"%s\"" % i)
    def access(self,url):
        #访问url
        try:
            #print(url)
            self.driver.get(url)
            self.driver.implicitly_wait(self.timeout)
            return True
        except Exception as e:
                print(e)
                return False
    def callback_network(self):
        #return 页面的网络请求信息
        try:
            list_net_url=[]
            performances = self.driver.execute_script("return window.performance.getEntries()")
            for i in performances:
                try:
                    #if i['initiatorType']=='xmlhttprequest':
                    list_net_url.append(i['name'])
                except:pass
            #list_net_url=list(set([i['name'] for i in performances]))
            return list(set(list_net_url))
        except:return []
    def callback_href_tmp(self):
        #return href
        try:
            list_url=list(set([i.get_attribute('href') for i in self.driver.find_elements_by_xpath("//a[@href]")]))
            return (list_url)
        except Exception as e:
            print(e)
            return []
    def callback_source(self):
        #return 页面源码
        return self.driver.page_source
    def callback_url(self):
        #return 当前url
        try:
            return self.driver.current_url
        except:
            return None
    def callback_title(self):
        #return html title
        return self.driver.title
    def callback_spider_data(self,url):
        try:
            print(url)
            self.driver.get(url)
            result = EC.alert_is_present()(self.driver)
            if result:result.dismiss()
            self.driver.implicitly_wait(self.timeout)
            self.driver.set_script_timeout(5)
            self.driver.set_page_load_timeout(self.timeout)   
            html_size=len(self.driver.page_source)
            if html_size!=76:
                return {'domain':self.config_main.callback_split_domain(url,1),'current_url':self.driver.current_url,'title':self.driver.title,'html_size':html_size,'state':0,'time':self.time}
            else:return False
        except Exception as e:
                print(url+':'+str(e))
                return False
    def callback_href(self):
        try:
            js='''
            var list_href=new Array();
            var hrefArr = document.getElementsByTagName('a'); //获取这个页面的所有A标签
              for( var i=0; i<hrefArr.length; i++ ){
                  //console.log(hrefArr[i].href) ; //修改语句
                  list_href[i]=hrefArr[i].href;
              }
            return list_href;
            list_href=true;
            '''
            performances = self.driver.execute_script(js)
            return performances
        except Exception as e:
            print(e)
            return []
    def callback_data(self):
        list_url=[]
        for i in list(set(self.callback_href())):
            list_url.append(self.config_main.callback_split_domain(i,0))
        for j in list(set(self.callback_network())):
            list_url.append(self.config_main.callback_split_domain(j,0))
        data=list(set(list_url))
        return data
    def close(self):
        #结束浏览器
        self.driver.quit()
if __name__ == '__main__':
    itme=Browser()
    for url in ['https://www.163.com','https://www.qq.com']:
        json_data=itme.callback_spider_data(url)
        print(json_data)
        if json_data!=False:
            print(itme.callback_data())
    #print(itme.callback_source())
    itme.close()