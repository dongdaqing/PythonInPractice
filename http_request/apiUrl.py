# -*- coding: utf-8 -*-
__author__ = 'dongdaqing'

import sys, os, httplib, urllib2, codecs, time, json,platform
import urlparse, socket, logging, threading
import multiprocessing

reload(sys)
#解决ascii码显示问题
sys.setdefaultencoding( "utf-8" )
readUrl = r"/usr/local/repos/interfaceUrl3.0/url3.0.txt"
httpMothed = ""
interfaceName = ""
interfaceUrl = ""
#定义测试接口和正式接口域名列表"api.3g.youku.com"
urlList = ["test1.api.3g.youku.com"]
w_path = platform.system().lower() == 'linux' and r'/opt' or r'C:\interfaceUrl3.0' 
nowtime=time.strftime('%Y%m%d%H%M%S',time.localtime())+'_total'
folder_w_path=os.path.join(w_path,nowtime)

totalCount = 0
totalResponseTime=0
failTotal = 0
if not os.path.exists(folder_w_path):os.makedirs(folder_w_path)
#log记录定义
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#定义日志输出到文件的handler
inputFile = logging.FileHandler(os.path.join(folder_w_path,'testInterfaceUrl.log'))
inputFile.setLevel(logging.DEBUG)

# 定义日志输出到控制台的handler
inputConsole = logging.StreamHandler()
inputConsole.setLevel(logging.DEBUG)
#添加handler
logger.addHandler(inputFile)
logger.addHandler(inputConsole)

class MutiThread(threading.Thread):
    # 构造函数  
    def __init__(self, thread_name):  
        threading.Thread.__init__(self)  
        self.test_count = 0  
        
    def run(self):
        # 线程运行的入口函数  
        a=self.outputTestResult()
    
    def comment(self,string,fileName='Details'):
        '''Print log info'''
        currentTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        print '%s %s %s'%(currentTime,fileName,string)
        
    def additional_data(self,data,fileName='exception.log'):
        '''
            add data into file
        '''
        global folder_w_path
        f2=None
        if not os.path.exists(folder_w_path):
            os.makedirs(folder_w_path)
        file_w_path=os.path.join(folder_w_path,fileName)
        try:
            f2=open(file_w_path ,'a')
        except IOError:
            sys.exit('Write error:--->%s'%file_w_path)
        else:
            f2.write(data+'\n')
        finally:
            f2.close()

    def reset(self, getSucessCount, getFailCount, postSucessCount, postFailCount, postCountTotal, getCountTotal):
        #重置各变量
        getSucessCount = 0
        getFailCount = 0
        postSucessCount = 0
        postFailCount = 0
        postCountTotal = 0
        getCountTotal = 0
        return getSucessCount, getFailCount, postSucessCount, postFailCount, postCountTotal, getCountTotal

    def updateUrl(self, interfaceUrl, urlTest):
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
        query= oldUrlChangeList[3]
        fragment = oldUrlChangeList[4]
        #使用urlunparse重新将list重新组成tuple
        interfaceUrl = urlparse.urlunparse((scheme, netloc, path, parameters, query, fragment))
        return interfaceUrl

    def mothedGet(self,name, mothed, url, failCount):
        #使用get方式访问server
        #totalCount默认认为递增和
        responseTime=0
        timeConsuming = time.time()
        statrTime = time.time()
        docUrlsucc = r"{} Interface name={}  Request mothed={}  testStatus = {}".\
            format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),name, mothed, "pass")
        docUrlfail = r"{} Interface name={}  Request mothed={}  testStatus = {}".\
            format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),name, mothed, "fail")
            
        #urllib2关于httpErrorCode只会报出400-599的range
        if mothed == "get":
            try:
                req = urllib2.Request(url)
                request = urllib2.urlopen(req, timeout=1)
                resulst = request.read()
                jsonResulst = json.loads(resulst)
                request.close()
                endTime = time.time()
                responseTime = endTime - statrTime
                logger.info(r"{} time(s)={}".format(docUrlsucc, responseTime))
            except urllib2.HTTPError, e:
                failCount += 1
                endTime = time.time()
                countTime = endTime - statrTime
                logger.info(r"{} {} time(s)={}".format(docUrlfail, e.code, countTime))
                self.additional_data(r"{} Exception:{}".format(docUrlfail, e.code))
            except urllib2.URLError, e:
                failCount += 1
                endTime = time.time()
                countTime = endTime - statrTime
                logger.info(r"{} time(s)={}".format(docUrlfail, countTime))
                self.additional_data(r"{} Exception:{}".format(docUrlfail, e))
            except socket.timeout, e:
                failCount += 1
                endTime = time.time()
                countTime = endTime - statrTime
                logger.info(r"{} time(s)={}".format(docUrlfail, countTime))
                self.additional_data(r"{} Exception:{}".format(docUrlfail, e))
        elif mothed == "post":
            try:
                req = urllib2.Request(url, "")
                request = urllib2.urlopen(req, timeout=1)
                resulst = request.read()
                jsonResulst = json.loads(resulst)
                request.close()
                endTime = time.time()
                responseTime = endTime - statrTime
                logger.info(r"{} time(s)={}".format(docUrlsucc, responseTime))
            except urllib2.HTTPError, e:
                failCount += 1
                endTime = time.time()
                countTime = endTime - statrTime
                logger.info(r"{} {} time(s)={}".format(docUrlfail, e.code, countTime))
                self.additional_data(r"{} Exception:{}".format(docUrlfail, e.code))
            except urllib2.URLError, e:
                failCount += 1
                endTime = time.time()
                countTime = endTime - statrTime
                logger.info(r"{} time(s)={}".format(docUrlfail, countTime))
                self.additional_data(r"{} Exception:{}".format(docUrlfail, e)) 
            except socket.timeout, e:
                failCount += 1
                endTime = time.time()
                countTime = endTime - statrTime
                logger.info(r"{} time(s)={}".format(docUrlfail, countTime))
                self.additional_data(r"{} Exception:{}".format(docUrlfail, e))
                
        return failCount,responseTime
        
    def testperfmance(self):
        #测试函数
        global totalCount
        global failTotal
        global totalResponseTime
        global readUrl
        failCount = 0
        fail = 0
        responseTime=0
        
        #打开接口文件
        try:
            readFile = codecs.open(readUrl, encoding="utf-8")
            fileLine = readFile.read()
        finally:
            readFile.close()
        #设置重复访问次数，50接口访问/次
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
                    interfaceUrl = self.updateUrl(interfaceUrl, urlTest)
                    fail ,responseTime= self.mothedGet(interfaceName, httpMothed, interfaceUrl, failCount)
                    totalResponseTime+=responseTime
                    failTotal += fail

        return totalCount, failTotal, float(format(float(totalResponseTime)*1000/(totalCount-failTotal),'.3f'))

    def outputTestResult(self):
        #输出测试结果
        startTime=time.time()
        result=self.testperfmance()
        #/*完成的请求数量*/
        logger.info('Complete requests:\t%d'%(result[0]))
        #/*失败的请求数量*/
        logger.info('Failed requests:\t%d'%result[1])
        #平均事务响应时间 ，后面括号中的 mean 表示这是一个平均值
        logger.info('Time per request::\t%.3f [ms] (mean)'%result[2])
        endTime=time.time()
        logger.info('Time taken for tests:\t%.6f seconds'%(endTime-startTime))
def startThread(thread_count=10):
    #多线程并发
    start_time = time.time()  
    i = 0  
    while i < thread_count: 
        t = MutiThread("thread" + str(i))  
        t.start()  
        i += 1
        
if __name__ == '__main__':
    startTime=time.time()
    startThread()
    endTime=time.time()
    #/*整个测试持续的时间*/
    logger.info('Time taken for tests:\t%.6f seconds'%(endTime-startTime))


