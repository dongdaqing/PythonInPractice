# -*- coding: utf-8 -*-
__author__ = 'dongdaqing'

import sys, os, httplib, urllib2, codecs, time, json,platform
import urlparse, socket, logging, threading
import multiprocessing

reload(sys)
#���ascii����ʾ����
sys.setdefaultencoding( "utf-8" )
readUrl = r"/usr/local/repos/interfaceUrl3.0/url3.0.txt"
httpMothed = ""
interfaceName = ""
interfaceUrl = ""
#������Խӿں���ʽ�ӿ������б�"api.3g.youku.com"
urlList = ["test1.api.3g.youku.com"]
w_path = platform.system().lower() == 'linux' and r'/opt' or r'C:\interfaceUrl3.0' 
nowtime=time.strftime('%Y%m%d%H%M%S',time.localtime())+'_total'
folder_w_path=os.path.join(w_path,nowtime)

totalCount = 0
totalResponseTime=0
failTotal = 0
if not os.path.exists(folder_w_path):os.makedirs(folder_w_path)
#log��¼����
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#������־������ļ���handler
inputFile = logging.FileHandler(os.path.join(folder_w_path,'testInterfaceUrl.log'))
inputFile.setLevel(logging.DEBUG)

# ������־���������̨��handler
inputConsole = logging.StreamHandler()
inputConsole.setLevel(logging.DEBUG)
#���handler
logger.addHandler(inputFile)
logger.addHandler(inputConsole)

class MutiThread(threading.Thread):
    # ���캯��  
    def __init__(self, thread_name):  
        threading.Thread.__init__(self)  
        self.test_count = 0  
        
    def run(self):
        # �߳����е���ں���  
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
        #���ø�����
        getSucessCount = 0
        getFailCount = 0
        postSucessCount = 0
        postFailCount = 0
        postCountTotal = 0
        getCountTotal = 0
        return getSucessCount, getFailCount, postSucessCount, postFailCount, postCountTotal, getCountTotal

    def updateUrl(self, interfaceUrl, urlTest):
        #�޸Ĳ��Խӿڻ���ʽ�ӿ�����
        #����url���Ϊscheme, netloc, path, parameters, query, fragment
        openurl = urlparse.urlsplit(interfaceUrl)
        #��tupleתΪlist
        oldUrlChangeList = list(tuple(openurl))
        #����list�����scheme, netloc, path, parameters, query, fragmentֵ
        oldUrlChangeList[1] = urlTest
        scheme = oldUrlChangeList[0]
        netloc = oldUrlChangeList[1]
        path = oldUrlChangeList[2]
        parameters = ""
        query= oldUrlChangeList[3]
        fragment = oldUrlChangeList[4]
        #ʹ��urlunparse���½�list�������tuple
        interfaceUrl = urlparse.urlunparse((scheme, netloc, path, parameters, query, fragment))
        return interfaceUrl

    def mothedGet(self,name, mothed, url, failCount):
        #ʹ��get��ʽ����server
        #totalCountĬ����Ϊ������
        responseTime=0
        timeConsuming = time.time()
        statrTime = time.time()
        docUrlsucc = r"{} Interface name={}  Request mothed={}  testStatus = {}".\
            format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),name, mothed, "pass")
        docUrlfail = r"{} Interface name={}  Request mothed={}  testStatus = {}".\
            format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),name, mothed, "fail")
            
        #urllib2����httpErrorCodeֻ�ᱨ��400-599��range
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
        #���Ժ���
        global totalCount
        global failTotal
        global totalResponseTime
        global readUrl
        failCount = 0
        fail = 0
        responseTime=0
        
        #�򿪽ӿ��ļ�
        try:
            readFile = codecs.open(readUrl, encoding="utf-8")
            fileLine = readFile.read()
        finally:
            readFile.close()
        #�����ظ����ʴ���50�ӿڷ���/��
        #��ȡurlList�����������б�
        for urlTest in urlList:
            print "-" * 150
            print urlTest
            print "-" * 150
            #���ж�ȡ�ļ�����
            for line in fileLine.split("\n"):
                totalCount += 1
                if line:
                    #���ո�ָ��ֶΣ����ж�ʹ��mothed��ʽ
                    interfaceName, httpMothed, interfaceUrl = line.split(" ")
                    interfaceUrl = self.updateUrl(interfaceUrl, urlTest)
                    fail ,responseTime= self.mothedGet(interfaceName, httpMothed, interfaceUrl, failCount)
                    totalResponseTime+=responseTime
                    failTotal += fail

        return totalCount, failTotal, float(format(float(totalResponseTime)*1000/(totalCount-failTotal),'.3f'))

    def outputTestResult(self):
        #������Խ��
        startTime=time.time()
        result=self.testperfmance()
        #/*��ɵ���������*/
        logger.info('Complete requests:\t%d'%(result[0]))
        #/*ʧ�ܵ���������*/
        logger.info('Failed requests:\t%d'%result[1])
        #ƽ��������Ӧʱ�� �����������е� mean ��ʾ����һ��ƽ��ֵ
        logger.info('Time per request::\t%.3f [ms] (mean)'%result[2])
        endTime=time.time()
        logger.info('Time taken for tests:\t%.6f seconds'%(endTime-startTime))
def startThread(thread_count=10):
    #���̲߳���
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
    #/*������Գ����ʱ��*/
    logger.info('Time taken for tests:\t%.6f seconds'%(endTime-startTime))


