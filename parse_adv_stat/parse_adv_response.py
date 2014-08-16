# -*- coding: utf-8 -*-
__author__ = 'dongdaqing'

import urllib2,json,socket

class AdvResponse(object):

    def __init__(self):
        self.url = "http://test1.api.3g.youku.com/adv?vid=d4edea60e0d011df97c0&site=1&position=7&is_fullscreen=1&player_type=mdevice&sessionid=bd5504c05ed2144bb26a03dfa7c953cb&device_type=phone&device_brand=samsung&ouid=4ea59c7e5e8e1c8d&aw=a&rst=flv&mac=&_os_=android&version=1.0&pid=4e308edfc33936d7&guid=276fb948188c651af9e1111832404920&mac=a0:0b:ba:d5:f7:87&imei=351565052124382&ver=3.3&operator=CMCC_46002&network=WIFI"

    def getresponse(self,testurl):

        try:
            req = urllib2.Request(testurl)
            request = urllib2.urlopen(req,timeout=5)
            result = request.read()
            json_result = json.loads(result)
            request.close()
        except urllib2.HTTPError, e:
            print e
        except urllib2.URLError, e:
            print e
        except socket.timeout, e:
            print e

        return json_result

    def writetoexcel(self,adv_list):

        for index in range(0,len(adv_list)):
            print adv_list[index]



    def analyzelog(self):

        json_result = self.getresponse(self.url)

        adv_list=[]
        #解析广告位
        P = json_result['P']
        temp = "\"U\":"+"\""+str(P)+"\""
        adv_list.append(temp)
        val_list = json_result['VAL']
        for res in val_list:
            #解析sus
            SUS0_U = res['SUS'][0]['U']
            SUS1_U = res['SUS'][1]['U']
            SUS2_U = res['SUS'][2]['U']
            temp = "\"U\":"+"\""+SUS0_U+"\""
            adv_list.append(temp)
            temp = "\"U\":"+"\""+SUS1_U+"\""
            adv_list.append(temp)
            temp = "\"U\":"+"\""+SUS2_U+"\""
            adv_list.append(temp)
            #解析sue
            SUE1_U = res['SUE'][0]['U']
            SUE2_U = res['SUE'][1]['U']
            temp = "\"U\":"+"\""+SUE1_U+"\""
            adv_list.append(temp)
            temp = "\"U\":"+"\""+SUE2_U+"\""
            adv_list.append(temp)
            #解析cum
            CUM = res['CUM'][0]['U']
            temp = "\"U\":"+"\""+CUM+"\""
            adv_list.append(temp)
            #解析cu
            CU = res['CU']
            temp = "\"U\":"+"\""+CU+"\""
            adv_list.append(temp)
            #解析广告类型at
            AT = res['AT']
            temp = "\"U\":"+"\""+str(AT)+"\""
            adv_list.append(temp)
            #解析广告时长al
            AL = res['AL']
            temp = "\"U\":"+"\""+str(AL)+"\""
            adv_list.append(temp)
            #解析rs
            RS = res['RS']
            temp = "\"U\":"+"\""+RS+"\""
            adv_list.append(temp)
            #解析vc
            VC = res['VC']
            temp = "\"U\":"+"\""+VC+"\""
            adv_list.append(temp)
            #解析vt
            VT = res['VT']
            temp = "\"U\":"+"\""+VT+"\""
            adv_list.append(temp)

        return adv_list

if __name__== '__main__':

    adv_obj = AdvResponse()
    adv_list = adv_obj.analyzelog()
    adv_obj.writetoexcel(adv_list)