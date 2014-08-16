# -*- coding: utf-8 -*-

import time,os
import loggingmodule
from pyExcelerator import *


class StartPage(object):
    def __init__(self):
        self.time_as_path = time.strftime('%Y%m%d%H%M%S',time.localtime())
        self.rootpath = os.path.join('/Users/dongdaqing/SVN/MobileTest/DongDaqing/PyProject/parseadvertisement/temp',\
                                        self.time_as_path)
        if not os.path.exists(self.rootpath):
            os.mkdir(self.rootpath)

        #日志记录
        self.log_result = os.path.join(self.rootpath,'logResult.txt')
        #原始日志
        self.ori_log = '/Users/dongdaqing/SVN/MobileTest/DongDaqing/PyProject/parseadvertisement/P1010_adv_log.txt'
        #日志路径
#        self.log_path = '/Users/dongdaqing/SVN/MobileTest/DongDaqing/PyProject/parseadvertisement/logpath'
        self.log_path = '/Users/dongdaqing/Downloads'
        #初始化logger
        self.logger = loggingmodule.Logger('startpage',self.log_result)

    def parseLog(self,log_file):

#        self.logger.log('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t'%('Log_Time','User-Agent','Request','Exposure1',\
#                            'Exposure2','Exposure3','Exposure4','Response1','Response2','Response3','Response4'))

#        self.logger.log('%s\t%s\t%s\t%s\t%s\t%s\t'%('Request','User-Agent','Exposure1',\
#                                                                        'Exposure2','Exposure3','Exposure4'))

        write_file_tag = 0
        api = 'None'
        ua = 'None'
        mshow = 'None'
        show = 'None'
        iso = 'None'
        mover = 'None'

        f = open(log_file,'r')
        each_lines = f.readlines()
        for each_line in each_lines:
            if each_line.find('startpage') != -1:
                api = self.getAdvapi(each_line)
                if write_file_tag != 0:
                    self.logger.log('%s\t%s\t%s\t%s\t%s\t%s\t'%(api,ua,mshow,show,iso,mover))
                write_file_tag += 1
                print api
            elif each_line.find('User_Agent') != -1:
                ua = self.getUA(each_line)
                print ua
            elif (each_line.find('advertisement exposure url') != -1) and (each_line.find('mshow') != -1):
                mshow = self.getExposure(each_line)
                print mshow
            elif (each_line.find('advertisement exposure url') != -1) and (each_line.find('show') != -1):
                show = self.getExposure(each_line)
                print show
            elif (each_line.find('advertisement exposure url') != -1) and (each_line.find('iso') != -1):
                iso = self.getExposure(each_line)
                print iso
            elif (each_line.find('advertisement exposure url') != -1) and (each_line.find('mover') != -1):
                mover = self.getExposure(each_line)
                print mover
        self.logger.log('%s\t%s\t%s\t%s\t%s\t%s'%(api,ua,mshow,show,iso,mover))

    def openMultiLog(self):
        self.logger.log('%s\t%s\t%s\t%s\t%s\t%s\t'%('Request','User-Agent','Exposure1',\
                                                    'Exposure2','Exposure3','Exposure4'))
        os.chdir(self.log_path)
        file_names = os.listdir('.')
        for file_name in file_names:
            self.parseLog(file_name)

    def getUA(self,ua_str):
        ua_str_result = ua_str.strip().split(';')
        ua = ua_str_result[4]
        return ua

    def getAdvapi(self,api_str):
        api_str_result = api_str.strip().split(' ')
        api = api_str_result[6]
        return api

    def getExposure(self,exposure_str):
        exposure_str_result = exposure_str.strip().split(' ')
        result = exposure_str_result[5]
        return result

    def saveExcel(self):
        root_path = self.rootpath
        assert os.path.exists(root_path)

        w = Workbook()
        os.chdir(root_path)

        file_path = os.path.join(root_path,self.log_result)
        ws = w.add_sheet('ad_info')
        f = file(file_path,'r')
        lines = f.readlines()
        for i in range(0,len(lines)):
            line = lines[i].split('\t')
            for j in range(0,len(line)):
                b = line[j].strip()
                ws.write(i,j,b)
        save_path = os.path.join(root_path,'log_result.xls')
        if os.path.exists(save_path):
            os.remove(save_path)
        w.save(save_path)


if __name__ == '__main__':
    obj = StartPage()
    obj.openMultiLog()
    obj.saveExcel()