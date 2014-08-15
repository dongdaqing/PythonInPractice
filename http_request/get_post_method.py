__author__ = 'dongdaqing'


import urllib2,json,urlparse,urllib
import httplib

posturl = "http://test.api.3g.youku.com/user/login?_cookie=_l_lgi%3D70994840%3B%20k%3D%25E7%25A2%258E%25E5%25BD%25AA%3B%20logintime%3D1348481501%3B%20u%3D%25E7%25A2%258E%25E5%25BD%25AA%3B%20v%3DUMjgzOTc5MzYw__1%257C1348481501%257C15%257CaWQ6NzA5OTQ4NDAsbm4656KO5b2q%257Cc2c9e54a6d75b1fd0888809efe1fde12%257Cf067914723d4925277d0e0f71fe05f716774c024%257C1____dd316050b67516220971eff7%3B%20ykss%3Ddd316050b67516220971eff7%3B%20yktk%3D1%257C1348481501%257C15%257CaWQ6NzA5OTQ4NDAsbm4656KO5b2q%257Cc2c9e54a6d75b1fd0888809efe1fde12%257Cf067914723d4925277d0e0f71fe05f716774c024%257C1%3B%20_1%3D1&uname=lgypp2013&pwd=e10adc3949ba59abbe56e057f20f883e&guid=9c553730ef5b6c8c542bfd31b5e25b69"
posturl1_1 = "http://test.api.3g.youku.com/user/login"
posturl1_2 = "_cookie=_l_lgi%3D70994840%3B%20k%3D%25E7%25A2%258E%25E5%25BD%25AA%3B%20logintime%3D1348481501%3B%20u%3D%25E7%25A2%258E%25E5%25BD%25AA%3B%20v%3DUMjgzOTc5MzYw__1%257C1348481501%257C15%257CaWQ6NzA5OTQ4NDAsbm4656KO5b2q%257Cc2c9e54a6d75b1fd0888809efe1fde12%257Cf067914723d4925277d0e0f71fe05f716774c024%257C1____dd316050b67516220971eff7%3B%20ykss%3Ddd316050b67516220971eff7%3B%20yktk%3D1%257C1348481501%257C15%257CaWQ6NzA5OTQ4NDAsbm4656KO5b2q%257Cc2c9e54a6d75b1fd0888809efe1fde12%257Cf067914723d4925277d0e0f71fe05f716774c024%257C1%3B%20_1%3D1&uname=lgypp2013&pwd=e10adc3949ba59abbe56e057f20f883e&guid=9c553730ef5b6c8c542bfd31b5e25b69"
posturl2 = "http://10.103.13.25/push-proxy/msd/?vid=131550732&title=test&app=youku&batchid=1308081451136325f959b&guid=480e64e886dc8530678145e358a6bfe0&desc=test"
geturl1 = "http://test.api.3g.youku.com/v3/play/address?id=XNTk4MzkwNjU2&pid=69b81504767483cf&format=1%2C2%2C3&guid=9c553730ef5b6c8c542bfd31b5e25b69"
geturl2 = "id=XNTk4MzkwNjU2&pid=69b81504767483cf&format=1%2C2%2C3&guid=9c553730ef5b6c8c542bfd31b5e25b69"

def getMethod():
    header={"User-Agent":"Youku;3.4;Android;4.2.1;Galaxy Nexus","Connection":"Keep-Alive","Accept-Encoding":"gzip"}
    req = urllib2.Request(geturl1,headers=header)
    request = urllib2.urlopen(req)
    result = request.read()
    jsonResult = json.loads(result)
    request.close()
    print jsonResult

#    conn = httplib.HTTPConnection("test.api.3g.youku.com")
#    conn.request('GET',"/v3/play/address",geturl2)
#    res = conn.getresponse()
#    result = res.read()
#    print res.version
#    print res.status
#    print result

#    conn = httplib.HTTPConnection("www.python.org")
#    conn.request('GET',"/index.html")
#    res = conn.getresponse()
#    result = res.read()
#    print result

def postMethod():
#    data=""
    data = posturl1_2
    req = urllib2.Request(posturl1_1,data)
    request = urllib2.urlopen(req)
    result = request.read()
    jsonResult = json.loads(result)
    request.close()
    print jsonResult

#    params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
#    conn = httplib.HTTPConnection("musi-cal.mojam.com:80")
#    headers = {"Content-type": "application/x-www-form-urlencoded",\
#            "Accept": "text/plain"}
#    conn.request("POST", "/cgi-bin/query", params, headers)
#    response = conn.getresponse()
#    data = response.read()
#    conn.close()
#    print data

def splitUrl():
    spliturl = urlparse.urlsplit(geturl1)
    listspliturl = list(spliturl)
    print spliturl
    print listspliturl

def testurlencode():
    collectParam = {"pid":"09e7fb15198a277d",\
                    "token":"",\
                    "app":"1",\
                    "platform":"4",\
                    "version":"2.4.4",\
                    "deviceId":"abcdefghg1234",\
                    "mac":"ae:ff:00:12:de:00",\
                    "imei":"uyreoepq930183",\
                    "uuid":"230249wewoeprwer04775",\
                    "action":"1",\
                    "grade":"",\
                    "user_id":"",\
                    "ip":"",\
                    "latitude":"",\
                    "longitude":"",\
                    "status":"",\
                    "gdid":""\
    }
#    collectParam = {
#        "batchid": "1308081451136325f959b",
#        "app": "youku",
#        "vid": "131550732",
#        "title": "test",
#        "desc": "test",
#        "guid": "480e64e886dc8530678145e358a6bfe0"
#    }
    params = urllib.urlencode(collectParam)
    print type(params)
    print params

if __name__ == '__main__':
#    testurlencode()
#    splitUrl()
    postMethod()
#    getMethod()