# -*- coding: utf-8 -*-
__author__ = 'dongdaqing'


#字符串间插入空格
def add_blank(src_str):
    data=[]
    for i in range(0,len(src_str)):
        data.append(src_str[i])
    return ' '.join(data)

print add_blank("hello")