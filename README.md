# 域名收集与监测V3.0
### 简介
在职业刷src或者apt攻击者的角度，单单过一遍爆破的域名是不能满足持续性漏洞挖掘;从职业刷src的角度，过一遍收集的子域名，已经发现了所有漏洞并已经提交后修复，或者用当前漏洞测试方法并没发现有漏洞，这样业务是安全的，但这个安全是在当下时间的，企业要发展、要解决当前问题，就会出新业务、或者不断的修复更新旧问题，这就是业务的变化，通过持续性监控子域名就会发现业务的变化，最快速度的发现变化，对变化进行安全测试、漏洞挖掘。有经验的刷src的同学都知道，新业务发现漏洞概率都很高。


### 环境配置
需要环境:
* win10/8/7/xp  
  其他请自行修改代码、反正是开源，改动也不大。
* python3  
  python3.5+ 自行官方下载
* mongodb  
  自行官方下载 建议docker搭建 参考:https://www.jianshu.com/p/6fdb2bcb4b43
* chrome  
  自行官方下载
* chromedriver  
  下载成功后放入python根目录或加入全局环境变量  
  chromedriver下载地址:http://npm.taobao.org/mirrors/chromedriver/ 注:与当前chrome匹配
* subfinder  
  https://github.com/subfinder/subfinder win默认带有,其他请自行修改代码。

以上配置完成,切进项目目录  
pip 安装requirements.txt
>pip install -r requirements.txt

# 搭建不成功的,自行google搜索"python3 selenium chrome on linux/win/mac"  这个只要跑成功,连接上mongodb就大功告成了 




设置config.json
```
{
	"path":"E:/code/test1", //项目所在绝对路径
	"target_json":"E:/code/test1/target/qq.json",   //目标域名文件绝对路径
	"chrome_path":"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe", //chrome文件绝对路径
  "chromedriver_path":"/Users/guimaizi/hack-tool/chromedriver" //chromedriver驱动路径
	"timeout":8, //全局超时设置,建议大于5
	"mongo_config":{"ip":"127.0.0.1","port":27017,"name":"","password":""} //mongodb 配置,ip 端口 name passwrod  空密码时name pwd设置为空
  
}
```

设置目标域名文件
```
{
"domain":".qq.com",  //目标域名 必须是.xx.xxx 如.qq.com .163.com .126.net
//子域名黑名单,解决泛解析问题
"Blacklist_domain":[
        ".qzone.qq.com",
        ".gamebbs.qq.com",
        ".ke.qq.com",
        ".house.qq.com",
        ".auto.qq.com",
        ".openwebgame.qq.com",
        ".house.qq.com",
        ".zhan.qq.com",
        ".114.qq.com",
        ".photo.store.qq.com",
        ".b.qq.com",
        ".m.qq.com",
        ".z.qq.com",
        ".t.qq.com",
        ".ly.qq.com",
        ".zg.qq.com",
        ".3g.qq.com",
        ".4g.qq.com",
        ".ia.qq.com",
		".city.qq.com",
		".photo.qq.com"
    ]
}
```

设置fun_all.py第12行
```
修改对应config.json绝对路径
```

### 运行说明
获取域名http响应结果写入mongodb库  

![](https://raw.githubusercontent.com/guimaizi/cloud/test/20190614112043.png)

获取子域名、子域名管理、子域名监控
>python start.py [argv]  
-s 开始通过subfinder爆破获取第一批域名;  
-u 调出数据库内domain重新爬行，通过新旧返回值比对，发现业务变化;  
-i 导入域名txt字典文件  格式为:xxx.xxx.com;  
-iurl 导入url txt文件 格式为:http://xxx.xxx.com/dasd.php;  

![](https://raw.githubusercontent.com/guimaizi/cloud/test/20190624222624.png)

### 结果
![](https://raw.githubusercontent.com/guimaizi/cloud/test/20190624222715.png)



### 码个代码不容易，希望有钱人打赏,万分感谢。
![](https://raw.githubusercontent.com/guimaizi/cloud/test/img/20190301182006.jpg)


