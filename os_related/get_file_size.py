__author__ = 'dongdaqing'

import os

# file_path = "/Users/dongdaqing/Desktop/Youku_Android_4.0.1_360.0.apk"
# print 'file is: '+str(os.path.getsize(file_path))+' Byte'

file_size=[]
file_dir = "/Users/dongdaqing/Desktop/file_dir"
for file in os.listdir(file_dir):
    if file.find("Android") != -1:
        file_name = os.path.join(file_dir,file)
        file_size.append(os.path.getsize(file_name))

for i in range(0,len(file_size)):
    print file_size[i]
    if file_size[i] != file_size[0]:
        flag = 1
    else:
        flag = 0
if flag == 1:
    print "not equal"
else:
    print "equal"