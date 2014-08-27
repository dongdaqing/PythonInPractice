# -*- coding: utf-8 -*-
__author__ = 'dongdaqing'

import urllib2
import urllib
import cookielib
#登陆用户名和密码
data={
    "email":"账号",
    "password":"密码"
}
#生成post数据，含有登录名和密码
post_data=urllib.urlencode(data)
#获得一个cookieJar实例
cj=cookielib.CookieJar()
#cookieJar作为参数，获得opener实例
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#另外一种方法
# urllib2.install_opener(opener)
#伪装正常浏览器
headers ={"User-agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
req=urllib2.Request("http://www.renren.com/PLogin.do",post_data,headers)
#带cookie访问页面
content=opener.open(req)
#读取页面源码
print content.read().decode("utf-8")
#另外一种方法
# print urllib2.urlopen(req).read()
#获得访问网页返回的cookie
# for index, cookie in enumerate(cj):
#     print '[',index,']', cookie
