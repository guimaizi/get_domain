# coding: utf-8
'''
@author: guimaizi
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests, time
from Lib import fun_all
class browser_control:
    def __init__(self):
        #print(1111111)
        self.config_main=fun_all.fun_all()
        #浏览器
        chrome_options = Options()
        #headless模式运行
        chrome_options.add_argument('--headless')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        #不加载图片
        chrome_options.add_argument('blink-settings=imagesEnabled=false')
        #调用当前chrome用户数据 cookie登陆方式
        #chrome_options.add_argument(r'user-data-dir=%s'%models.read_config()['chrome_user_data'])
        chrome_options.add_argument('--disable-gpu')
        #chrome_options.add_argument('--hide-scrollbars')
        #print(self.config_main.callback_chrome_path)
        chrome_options.binary_location = r'%s'%self.config_main.callback_chrome_path()
        self.driver = webdriver.Chrome(executable_path=self.config_main.load_dict['chromedriver_path'],options=chrome_options)
        self.time=time.strftime('%Y-%m-%d',time.localtime())
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
    def callback_link(self):
        list_url_tmp=[]
        list_url_tmp.extend(self.callback_href_tmp())
        list_url_tmp.extend(self.callback_network())
        list_url=[]
        for i in list_url_tmp:
            url=self.config_main.callback_detection_domain(i)
            if url!=False and url!=None:
                list_url.append(url)
        return list(set(list_url))
    def run(self,domain):
        try:
            print(domain)
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
            url='http://%s'%domain
            r = requests.get(url,timeout=self.config_main.load_dict['timeout']-2,headers=headers)
            if r.status_code in [200,301,302,500,404,403,401]:
                self.driver.get(url)
                result = EC.alert_is_present()(self.driver)
                if result:result.dismiss()
                self.driver.implicitly_wait(self.config_main.load_dict['timeout']-1)
                self.driver.set_script_timeout(self.config_main.load_dict['timeout']-1)
                self.driver.set_page_load_timeout(self.config_main.load_dict['timeout'])   
                html_size=len(self.driver.page_source)
                return {"domain":domain,"url":self.driver.current_url,"status":0,"title":self.driver.title,"http_length":html_size,"http_status":r.status_code,"time":self.time,"Remarks":""}
            else:return []
            r.close()
        except Exception as e:
            print(url+':'+str(e))
            return []
    def browser_exit(self):
        self.driver.quit()
if __name__ == '__main__':
    try:
        print(111)
        item=browser_control()
        print(item.run('www.qq.com'))
        #print(item.callback_href_tmp())
        print(item.callback_link())
    except Exception as e:print(e)
    finally:item.browser_exit()