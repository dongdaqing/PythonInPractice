# -*- coding: utf-8 -*-
__author__ = 'waylidong'

import sys, os, httplib, urllib2, codecs, time, json
import urlparse, socket, logging

reload(sys)
# 解决ascii码显示问题
sys.setdefaultencoding("utf-8")

readUrl = r"/Users/waylidong/Desktop/url3.0.txt"
httpMothed = ""
interfaceName = ""
interfaceUrl = ""
#定义测试接口和正式接口域名列表"api.3g.youku.com"
urlList = ["test1.api.3g.youku.com"]

#log记录定义
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
#定义日志输出到文件的handler
inputFile = logging.FileHandler("/Users/waylidong/Desktop/mutSwitch/urlTest/testurl.log")
inputFile.setLevel(logging.DEBUG)
#定义日志输出到控制台的handler
inputConsole = logging.StreamHandler()
inputConsole.setLevel(logging.DEBUG)
#添加handler
logger.addHandler(inputFile)
logger.addHandler(inputConsole)


def reset(getSucessCount, getFailCount, postSucessCount, postFailCount, postCountTotal, getCountTotal):
    #重置各变量
    getSucessCount = 0
    getFailCount = 0
    postSucessCount = 0
    postFailCount = 0
    postCountTotal = 0
    getCountTotal = 0
    return getSucessCount, getFailCount, postSucessCount, postFailCount, postCountTotal, getCountTotal


def updateUrl(interfaceUrl, urlTest):
    #修改测试接口或正式接口域名
    #解析url组件为scheme, netloc, path, parameters, query, fragment
    openurl = urlparse.urlsplit(interfaceUrl)
    #将tuple转为list
    oldUrlChangeList = list(tuple(openurl))
    #更新list组件的scheme, netloc, path, parameters, query, fragment值
    oldUrlChangeList[1] = urlTest
    scheme = oldUrlChangeList[0]
    netloc = oldUrlChangeList[1]
    path = oldUrlChangeList[2]
    parameters = ""
    query = oldUrlChangeList[3]
    fragment = oldUrlChangeList[4]
    #使用urlunparse重新将list重新组成tuple
    interfaceUrl = urlparse.urlunparse((scheme, netloc, path, parameters, query, fragment))
    return interfaceUrl


def mothedGet(name, mothed, url, totalCount, failCount):
    #使用get方式访问server
    #totalCount默认认为递增和
    timeConsuming = time.time()
    statrTime = time.time()
    docUrlsucc = r"Interface name={}  Request mothed={}  testStatus = {}".format(name, mothed, "pass")
    docUrlfail = r"Interface name={}  Request mothed={}  testStatus = {}".format(name, mothed, "fail")
    #urllib2关于httpErrorCode只会报出400-599的range
    if mothed == "get":
        try:
            req = urllib2.Request(url)
            request = urllib2.urlopen(req, timeout=5)
            resulst = request.read()
            jsonResulst = json.loads(resulst)
            request.close()
        except urllib2.HTTPError, e:
            failCount += 1
            endTime = time.time()
            countTime = endTime - statrTime
            logger.info(r"{} {} time(s)={}".format(docUrlfail, e.code, endTime))
        except urllib2.URLError, e:
            failCount += 1
            endTime = time.time()
            countTime = endTime - statrTime
            #		    logger.exception(e)
            logger.info(r"{} time(s)={}".format(docUrlfail, endTime))
        #		    logger.exception(e)
        except socket.timeout, e:
            failCount += 1
            endTime = time.time()
            countTime = endTime - statrTime
            #		    logger.exception(e)
            logger.info(r"{} time(s)={}".format(docUrlfail, endTime))
        #		    logger.exception(e)
    elif mothed == "post":
        try:
            req = urllib2.Request(url, "")
            request = urllib2.urlopen(req, timeout=5)
            resulst = request.read()
            jsonResulst = json.loads(resulst)
            request.close()
        except urllib2.HTTPError, e:
            failCount += 1
            endTime = time.time()
            countTime = endTime - statrTime
            logger.info(r"{} {} time(s)={}".format(docUrlfail, e.code, endTime))
        #		    logger.info(timeConsuming)
        except urllib2.URLError, e:
            failCount += 1
            endTime = time.time()
            countTime = endTime - statrTime
            #		    logger.exception(e)
            logger.info(r"{} time(s)={}".format(docUrlfail, endTime))
        #		    logger.exception(e)
        except socket.timeout, e:
            failCount += 1
            endTime = time.time()
            countTime = endTime - statrTime
            #		    logger.exception(e)
            logger.info(r"{} time(s)={}".format(docUrlfail, endTime))
    endTime = time.time()
    countTime = endTime - statrTime
    logger.info(r"{} time(s)={}".format(docUrlsucc, countTime))
    return totalCount, failCount


#	logger.info(r"total={} fail={}".format(totalCount, failCount))
def main():
    totalCount = 0
    failCount = 0
    succ = 0
    fail = 0
    failTotal = 0
    #打开接口文件
    try:
        readFile = codecs.open(readUrl, encoding="utf-8")
        fileLine = readFile.read()
    finally:
        readFile.close()
    #设置重复访问次数，50接口访问/次
    timeStart = time.time()
    for j in range(3):
        totalCount += 1
        fisttime = time.time()
        #读取urlList服务器域名列表
        for urlTest in urlList:
            print "-" * 150
            print urlTest
            print "-" * 150
            #按行读取文件内容
            for line in fileLine.split("\n"):
                totalCount += 1
                if line:
                    #按空格分隔字段，以判断使用mothed方式
                    interfaceName, httpMothed, interfaceUrl = line.split(" ")
                    interfaceUrl = updateUrl(interfaceUrl, urlTest)
                    succ, fail = mothedGet(interfaceName, httpMothed, interfaceUrl, totalCount, failCount)
                fail += 1
            failTotal = failTotal + fail
    logger.info(r"Total and succCount={} echoFail={} totalFail={}".format(succ, fail, failTotal))
    failTotal = fail

#		reset(getSucessCount, getFailCount, postSucessCount, postFailCount, postCountTotal, getCountTotal)
if __name__ == "__main__":
    main()