# 域名收集2.0
### 域名监控概括
子域名收集这个路子真的是被玩烂了，花样百出、工具没有八百也有一千，无非是爆破、爬、调用搜索引擎之类，有资源的大厂有自己的dns库，但是这些在我眼里真的都很low。

为什么说很low，因为在职业刷src或者apt攻击者的角度，单单过一遍爆破的域名是不能满足持续性漏洞挖掘的;从职业刷src的角度，过一遍收集的子域名，已经发现了所有漏洞并已经提交后修复，或者用当前漏洞测试方法并没发现有漏洞，这样业务是安全的，但这个安全是在当下时间的，企业要发展、要解决当前问题，就会出新业务不断的pull代码更新旧问题，这就是业务的变化，通过持续性监控子域名就会发现业务的变化，最快速度的发现变化，对变化进行安全测试、漏洞挖掘。有经验的刷src的同学都知道，新业务发现漏洞概率都很高。

懒惰使人创造工具，而我就拥有这么一个工具，从14年搞的子域名爆破工具(送给过一个小姐姐，刷了好多漏，如今以身为人妻，而我还没有女朋友。)，到如今的子域名监控工具。

具体实现思路
1、通过域名爆破、搜索引擎之类方法，获得子域名后爬取子域名http响应数据保存入数据库。
2、设定时间、可以是一分钟、一小时、一天一次循环读取库内子域名，进行爬取子域名和库类http响应数据对比，对比出变化推送提醒。

### 功能流程:  
>1、subfinder爆破、chrome爬取subfinder结果域名首页入库。  
2、爬取时执行js取出a标签url和performance.getEntries()取出页面网络请求url。  
3、格式化取出的url生成域名、库内非重复后进行二次爬取入库。  
4、无限循环2、3操作，直至爬取url和网络请求url不存在新域名。  
5、重新爬取库内域名，对比渲染后html大小、判断业务变化，并执行2、3操作发现新域名。  
6、7x24小时0-9\a-Z 随机生成域名dns爆破、非库内域名爬取入库。

### 代码结构
>browser.py  浏览器功能 获取html、执行js等  
config.py 配置文件，一些需要的功能  
mongodb_con.py mongo连接文件  
start.py 开始爆破和爬取子域名获取http响应入mongo库  对应功能:1、2、3  
while_update.py 域名监测功能、遍历mongo库内数据 对比出变化域名和爬取新域名 对应功能:5
random_start.py 对应功能:6  
\subfinder 用来启动最初爆破子域名
\tmp 存放browser爬取的 href network请求的url    
\target  存放要监测域名的配置信息  
### 环境配置
需要环境:python3 mongodb chrome chromedriver subfinder  

搭建参考链接:  
[mongodb-server请自行百度适合自己系统的mongodb搭建方式。](https://www.mongodb.com/)  
[python-selenium-chrome搭建方式](https://www.jianshu.com/p/dd848e40c7ad)  

python3依赖:
>pymongo  
requests  
dnspython  
threadpool  
queue  
selenium
BeautifulSoup4

#### 注:
***只要你把python3+selenium+chrome跑起来，我的程序基本就能跑起来,其次是配置config。***  
***如果非windows系统，请自行下载subfinder 并放代码目录下 修改start.py 72行。***

### 具体设置:  
配置目标domain.json(请注意格式)
![](https://raw.githubusercontent.com/guimaizi/cloud/test/img/20190301175907.png)  
domain 为要收集监测的目标域名，格式必须是.domain.com，如:   
.qq.com  
.163.com  
.weibo.com  
Blacklist_domain 为子域名黑名单，比如46456.qzone.qq.com qq空间业务，.qzone.qq.com绕过收集。  

进入config.py配置文件，进行配置
![](https://raw.githubusercontent.com/guimaizi/cloud/test/img/20190301180047.png)
然后执行python start.py 开始爆破、爬取子域名…域名数据决定运行时间。

while_update.py进行域名监控、功能流程:5。  
以上两功能执行结束后建议后台执行random_start.py 随机爆破，可能爆破出意想不到的业务，对应功能流程:6。

### 码个代码不容易，欢迎有钱人打赏。
![](https://raw.githubusercontent.com/guimaizi/cloud/test/img/20190301182006.jpg)
