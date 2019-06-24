# coding: utf-8
'''
Created on 2019��6��17��

@author: guimaizi
'''
from Lib import fun_all
from Lib import mongo_con
from Lib import browser_control
class dispatch_main:
    def __init__(self):
        #浏览器调度中心
        self.config_main=fun_all.fun_all()
        self.domain_list=[]
        self.domain_result_list=[]
    def run(self,list_url):
        #开始访问获取http响应
        try:
            Browsers=browser_control.browser_control()
            for url in list_url:
                data=Browsers.run(url)
                if data!=[]:
                    print(data)
                    self.domain_result_list.append(data)
                    self.domain_list.extend(Browsers.callback_link())
        finally:
            Browsers.browser_exit()
    def control(self,list_url):
        #控制中心
        #print(list_url)
        if len(list_url)>=60:
            list_url_ready_first=[]
            list_url_ready_action=[]
            for url in list_url:
                list_url_ready_first.append(url)
                if len(list_url_ready_first)==10:
                    list_url_ready_action.append(list_url_ready_first)
                    list_url_ready_first=[]
                if len(list_url_ready_action)==5:
                    self.config_main.threading_start(self.run,list_url_ready_action)
                    list_url_ready_action=[]    
            self.config_main.threading_start(self.run,list_url_ready_action)
            list_url_ready_action=[]
        else:
            list_url_ready=[]
            for url in list_url:
                list_url_ready.append(url)
                if len(list_url_ready)>=12:
                    self.run(list_url_ready)
                    list_url_ready=[]
            self.run(list_url_ready)
            list_url_ready=[]
        self.data=[]
    def callback_domain(self):
        data=self.domain_list
        self.domain_list=[]
        return list(set(data))
    def callback_result(self):
        data=self.domain_result_list
        self.domain_result_list=[]
        return data
if __name__ == '__main__':
    list_domain=['dreamreader.qq.com', 'wuxia.qq.com', 'btrace.video.qq.com', 'automall.qq.com', 'guanjia.qq.com', 'auto.qq.com', 'cfm.qq.com', 'support.qq.com', 'kuaibao.qq.com', 'l.qq.com', 'history.news.qq.com', 'book.qq.com', 'privacy.qq.com', 'cb.qq.com', 'sports.qq.com', 'kepu.qq.com', 'gouhuo.qq.com', 'lol.qq.com', 'iwan.qq.com', 'dj.captcha.qq.com', 'view.inews.qq.com', 'eafifa.qq.com', 'kf.qq.com', 'fiba.qq.com', 'pacaio.match.qq.com', 'huoying.qq.com', 'xian.qq.com', 'fans.sports.qq.com', 'yxwd.qq.com', 'apis.map.qq.com', 'nba.stats.qq.com', 'cf.qq.com', 'tlbb.qq.com', 'pc.qq.com', 'dn.qq.com', 'kg.qq.com', 'gu.qq.com', 'astro.fashion.qq.com', 'house.qq.com', 'player.qq.com', 'gy.qq.com', 'digi.tech.qq.com', 'vip.qq.com', 'v.qq.com', 'open.qq.com', 'time.qq.com', 'dnf.qq.com', 'om.qq.com', 'd.automall.qq.com', 'hdl.qq.com', 'users.qq.com', 'speed.qq.com', 'tech.qq.com', 'fm.qq.com', 'new.qq.com', 'news.house.qq.com', 'js.aq.qq.com', 'pvp.qq.com', 'weixin.qq.com', 'dajia.qq.com', 'www.qq.com', 'dp3.qq.com', 'kid.qq.com', 'browser.qq.com', 'qzone.qq.com', 'g.qq.com', 'pingjs.qq.com', 'map.qq.com', 'finance.qq.com', 'stock.qq.com', 'dldir1.qq.com', 'mail.qq.com', 'tianqi.qq.com', 'openapi.finance.qq.com', '110.qq.com', 'health.qq.com', 'vd.l.qq.com', 'docs.qq.com', 'class.qq.com', 'gongyi.qq.com', 'pay.qq.com', 'work.weixin.qq.com', 'matchweb.sports.qq.com', 'kbs.sports.qq.com', 'data.auto.qq.com', 'xing.qq.com', 'y.qq.com', 'mp.weixin.qq.com', 'imgcache.qq.com', 'wis.qq.com', 'news.qq.com', 'money.qq.com', 'qian.qq.com', 'im.qq.com', '888.qq.com', 'nz.qq.com', 'c.l.qq.com', 'ad.weixin.qq.com', 'pc.weixin.qq.com', 'service.qq.com', 'kf.qq.com', 'mac.weixin.qq.com', 'mp.weixin.qq.com', 'work.weixin.qq.com', 'support.weixin.qq.com', 'wx.qq.com', 'www.qq.com', 'news.qq.com', 'tajs.qq.com', 'fun.qq.com', 'babyting.qq.com', 'service.qq.com', 'kid.qq.com', 'open.qq.com', 'js.aq.qq.com', 'gongyi.qq.com', 'fun.kid.qq.com', 'game.kid.qq.com', 'bbs.kid.qq.com', 'v.qq.com', 'panshi.qq.com', 'news.qq.com', 'graph.qq.com', 'stock.qq.com', 'astro.lady.qq.com', 'house.qq.com', 'cul.qq.com', 'v.qq.com', 'auto.qq.com', 'tech.qq.com', 't.qq.com', 'book.qq.com', 'comic.qq.com', 'finance.qq.com', 'digi.qq.com', 'games.qq.com', 'sports.qq.com', 'www.qq.com', 'fashion.qq.com', 'class.qq.com', 'ent.qq.com', 'ilike.qq.com', 'edu.qq.com', 'dajia.qq.com', 'kid.qq.com', 'browser.qq.com', 'pingjs.qq.com', 'tajs.qq.com', 'tq.qq.com', 'i.browser.qq.com', 'safebrowsing.qq.com', 'stdl.qq.com', 'dldir1.qq.com', 'wis.qq.com', 'www.qq.com', 'xui.ptlogin2.qq.com', 'support.qq.com', 'qzone.qq.com', 'act.qzone.qq.com', 'wiki.open.qq.com', 'i.qq.com', 'qz.qzone.qq.com', 'my.qzone.qq.com', 'abcmouse.qq.com', 'connect.qq.com', 'user.qzone.qq.com', 'qzone.qzone.qq.com', 'vd.l.qq.com', 'docs.qq.com', 'sqimg.qq.com', 'g.qq.com', 'pingjs.qq.com', 'www.qq.com', 'xui.ptlogin2.qq.com', 'support.qq.com', 'tajs.qq.com', 'open.weixin.qq.com', 'class.qq.com', 'service.qq.com', 'open.qq.com', 'edu.qq.com', 'ke.qq.com', 'static.campus.qq.com', 'gongyi.qq.com', 'cp.class.qq.com', 'router.map.qq.com', 'confinfo.map.qq.com', 'user.map.qq.com', 's.map.qq.com', 'ssl.captcha.qq.com', 'sv.map.qq.com', 'apikey.map.qq.com', 'huitu.map.qq.com', 'bbs.map.qq.com', 'map.qq.com', 'ugc.map.qq.com', '3gimg.qq.com', 'overseactrl.map.qq.com', 'heat.qq.com', 'lbs.qq.com', 'www.qq.com', 'view.inews.qq.com', 'news.qq.com', 'support.qq.com', 'pingjs.qq.com', 'tech.qq.com', 'service.qq.com', 'open.qq.com', 't.qq.com', 'mp.weixin.qq.com', 'js.aq.qq.com', 'gongyi.qq.com', 'comment5.news.qq.com', 'new.qq.com', 'ssl.gongyi.qq.com', 'v.qq.com', 'thinker.qq.com', 'news.qq.com', 'tajs.qq.com', 'i.gdt.qq.com', 'service.qq.com', 'imgcache.qq.com', 'coral.qq.com', 'new.qq.com', 'v.qq.com', 'v.gdt.qq.com', 'pacaio.match.qq.com', 'open.qq.com', 'finance.qq.com', 'gongyi.qq.com', 'sports.qq.com', 'www.qq.com', 'support.qq.com', 'l.qq.com', 'fw.qq.com', 'users.qq.com', 'pingjs.qq.com', 'docs.qq.com', 'js.aq.qq.com', 'www.qq.com', 'view.inews.qq.com', 'news.qq.com', 'support.qq.com', 'pingjs.qq.com', 'tajs.qq.com', 'service.qq.com', 'open.qq.com', 'pacaio.match.qq.com', 'imgcache.qq.com', 'finance.qq.com', 'js.aq.qq.com', 'coral.qq.com', 'gongyi.qq.com', 'stockapp.finance.qq.com', 'new.qq.com', 'sports.qq.com', 'fw.qq.com', 'qingdao.auto.qq.com', 'dalian.auto.qq.com', 'taizhou.auto.qq.com', 'vs.qq.com', 'hangzhou.auto.qq.com', 'hengyang.auto.qq.com', 'baise.auto.qq.com', 'chengdu.auto.qq.com', 'siping.auto.qq.com', 'e.t.qq.com', 'yinchuan.auto.qq.com', 'zhenjiang.auto.qq.com', 'dp3.qq.com', 'yangjiang.auto.qq.com', 'changchun.auto.qq.com', 'taian.auto.qq.com', 'deyang.auto.qq.com', 'fuzhou.auto.qq.com', 'hhht.auto.qq.com', 'xiangtan.auto.qq.com', 'film.qq.com', 'nanyang.auto.qq.com', 'ningbo.auto.qq.com', 'guangan.auto.qq.com', 'fuyang.auto.qq.com', 'ziyang.auto.qq.com', 'qinzhou.auto.qq.com', 'zhengzhou.auto.qq.com', 'api.ait.auto.qq.com', 'huaibei.auto.qq.com', 'wecar.qq.com', 'yining.auto.qq.com', 'baojia.auto.qq.com', 'handan.auto.qq.com', 'wuzhou.auto.qq.com', 'suzhou.auto.qq.com', 'huaihua.auto.qq.com', 'quanzhou.auto.qq.com', 'guangzhou.auto.qq.com', 'dongguan.auto.qq.com', 'datong.auto.qq.com', 'pingdingshan.auto.qq.com', 'foshan.auto.qq.com', 'luan.auto.qq.com', 'automall.qq.com', 'liuzhou.auto.qq.com', 'heze.auto.qq.com', 'tianjin.auto.qq.com', 'fw.qq.com', 'xianning.auto.qq.com', 'gongyi.qq.com', 'huangshan.auto.qq.com', 'lyg.auto.qq.com', 'mas.auto.qq.com', 'c.l.qq.com', 'yuncheng.auto.qq.com', 'coral.qq.com', 'view.inews.qq.com', 'huzhou.auto.qq.com', 'guilin.auto.qq.com', 'support.qq.com', 'c.gdt.qq.com', 'd.automall.qq.com', 'xingtai.auto.qq.com', 'auto.qq.com', 'weihai.auto.qq.com', 'nanjing.auto.qq.com', 'open.qq.com', 'jilin.auto.qq.com', 'nanning.auto.qq.com', 'dali.auto.qq.com', 'anqing.auto.qq.com', 'shenzhen.auto.qq.com', 'new.qq.com', 'users.qq.com', 'wj.qq.com', 'www.qq.com', 'de.qq.com', 'lbs.qq.com', 'avlab.qq.com', 'trustsql.qq.com', 'c.qq.com', 'e.qq.com', 'gad.qq.com', 'miying.qq.com', 'tour.qq.com', 'vc.open.qq.com', 'connect.qq.com', 'adb.qq.com', 'gcloud.qq.com', 's.qq.com', 'ar.qq.com', 'kandian.mp.qq.com', 'compass.qq.com', 'mp.weixin.qq.com', 'wiki.connect.qq.com', 'qteng.qq.com', 'h5e.qq.com', 'uni.qq.com', 'ai.qq.com', 'heat.qq.com', 'youpin.qq.com', 'win.qq.com', 'jia.qq.com', 'tmc.qq.com', 'mta.qq.com', 'weixiao.qq.com', 'doctor.qq.com', 'tas.qq.com', 'gls.qq.com', 'shang.qq.com', 'medialab.qq.com', 'data.qq.com', 'om.qq.com', 'adx.qq.com', 'open.weixin.qq.com', 'wiki.open.qq.com', 'op.open.qq.com', 'open.qq.com', 'tajs.qq.com', 'support.qq.com', 'campus.qq.com', 'beacon.qq.com', 'wetest.qq.com', 'reteng.qq.com', 'service.qq.com', 'imgcache.qq.com', 'www.qq.com', 'support.qq.com', 'tajs.qq.com', 'confinfo.map.qq.com']
    print(len(list_domain))
    list_domain=list(set(list_domain))
    print(len(list_domain))
    item=dispatch_main()
    item.control(list_domain)
    print(item.callback_result())
    print(item.callback_domain())