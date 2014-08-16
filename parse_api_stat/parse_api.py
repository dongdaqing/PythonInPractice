# -*- coding: utf-8 -*-
__author__ = 'dongdaqing'

import sys,os,time,platform
from pyExcelerator import *

class ParseLog(object):

    def __init__(self):

        #判断当前操作系统类型
        cur_sys = platform.system()
        if cur_sys=='Windows':
            file_path = r'c:\temp'
        else:
            file_path = '/Users/dongdaqing/temp'

        time_as_path = time.strftime('%Y%m%d%H%M%S',time.localtime())
        self.root_path = os.path.join(file_path,time_as_path)

        if not os.path.exists(self.root_path):
            os.mkdir(self.root_path)

        #excel列名称
        self.excel_title = ['ApiName','TestResults','Params','PhoneType','OS','Version','AppVersion']
        self.excel_fixed_name = ['','','','Galaxy Nexus','Android','4.2.1','Youku_Android_3.5_1125_7519_test1.apk']
        self.user_agent = "User-Agent:Youku;3.5;Android;"+self.excel_fixed_name[5]+';'+self.excel_fixed_name[3]

        #这里设置边框
        borders = Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1

        #水平向左，垂直居中对齐
        al1 = Alignment()
        al1.horz = Alignment.HORZ_LEFT
        al1.vert = Alignment.VERT_CENTER
        al1.wrap = Alignment.WRAP_AT_RIGHT

        #绿色单元格
        pattern = Pattern()
        pattern.pattern_back_colour = 0x11
        pattern.pattern_fore_colour = 0x11
        pattern.pattern = pattern.SOLID_PATTERN

        self.excel_style = XFStyle()
        self.excel_style.alignment=al1
        self.excel_style.borders = borders

        self.excel_style_green = XFStyle()
        self.excel_style_green.alignment=al1
        self.excel_style_green.pattern = pattern
        self.excel_style_green.borders = borders

    def readfilelog(self,file_name):

        try:
            f = open(file_name,'r')
        except IOError:
            sys.exit('read file error:%s'%file_name)
        else:
            filelines = f.readlines()
        finally:
            f.close()

        row_count=1

        w = Workbook()
        ws = w.add_sheet('static')
        #写入列名称
        for i in range(0,len(self.excel_title)):
            ws.write(0,i,self.excel_title[i],self.excel_style)

        for eachline in filelines:
            if eachline.find('api')!=-1:
                self.analyzelog(ws,row_count,eachline)
                row_count+=1

        save_path = os.path.join(self.root_path,'staticlog.xls')
        if os.path.exists(save_path):
            os.remove(save_path)
        w.save(save_path)

    def analyzelog(self,ws,row_count,eachline):

        api_name=''
        params=''

        temp_data = eachline.split('?')
        api_name = temp_data[0]
        api_body = temp_data[1].split('&')

        for i in range(0,len(api_body)):
            if i == len(api_body)-1:
                params += api_body[i].strip()
                params += '\n'+self.user_agent
            else:
                params += api_body[i]+'\n'

        for j in range(0,len(self.excel_fixed_name)):
            if j==0:
                ws.write(row_count,j,api_name,self.excel_style)
            elif j==1:
                ws.write(row_count,j,'Passed',self.excel_style_green)
            elif j==2:
                ws.write(row_count,j,params.strip(),self.excel_style)
            else:
                ws.write(row_count,j,self.excel_fixed_name[j],self.excel_style)

if __name__ == '__main__':
    #统计接口文件
#    file_name = sys.argv[1]
    file_name = '/Users/dongdaqing/Desktop/pop_entry.txt'
    parselog_obj = ParseLog()
    parselog_obj.readfilelog(file_name)