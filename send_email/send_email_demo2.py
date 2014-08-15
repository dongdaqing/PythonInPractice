# -*- coding: utf-8 -*-
__author__ = 'dongdaqing'

import os, smtplib, mimetypes
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

MAIL_TO_LIST = ["dongdaqing@youku.com"]
MAIL_CC_LIST = ["dongdaqing@youku.com"]
MAIL_HOST = "mail.youku.com"
MAIL_USER = "dongdaqing"
MAIL_PASS = "password"
MAIL_POSTFIX = "youku.com"
MAIL_FROM = MAIL_USER + "<"+MAIL_USER + "@" + MAIL_POSTFIX + ">"

file_path = '/Users/dongdaqing/temp/filelist'
file_name = '/Users/dongdaqing/temp/filelist/ChannelActivityTest.java'

def send_mail(subject, content, filename = None):
    try:
        message = MIMEMultipart()
        message.attach(MIMEText(content))
        message["Subject"] = subject
        message["From"] = MAIL_FROM
        message["To"] = ";".join(MAIL_TO_LIST)
        message["Cc"] = ";".join(MAIL_CC_LIST)
#        if filename != None and os.path.exists(filename):
#            ctype, encoding = mimetypes.guess_type(filename)
#            if ctype is None or encoding is not None:
#                ctype = "application/octet-stream"
#            maintype, subtype = ctype.split("/", 1)
#            attachment = MIMEImage((lambda f: (f.read(), f.close()))(open(filename, "rb"))[0], _subtype = subtype)
#            attachment.add_header("Content-Disposition", "attachment", filename = os.path.basename(filename))
#            message.attach(attachment)

        for file in filename:
            ctype, encoding = mimetypes.guess_type(file)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"
            maintype, subtype = ctype.split("/", 1)
            attachment = MIMEImage((lambda f: (f.read(), f.close()))(open(file, "rb"))[0], _subtype = subtype)
            attachment.add_header("Content-Disposition", "attachment", filename = os.path.basename(file))
            message.attach(attachment)

        smtp = smtplib.SMTP()
        smtp.connect(MAIL_HOST)
        smtp.login(MAIL_USER, MAIL_PASS)
        smtp.sendmail(MAIL_FROM, MAIL_TO_LIST+MAIL_CC_LIST, message.as_string())
        smtp.quit()

        return True
    except Exception, errmsg:
        print "Send mail failed to: %s" % errmsg
        return False

if __name__ == "__main__":
    os.chdir(file_path)
    cur_filelist = os.listdir('.')
    if send_mail("测试信", "我的博客欢迎您：http://www.linuxidc.com/", cur_filelist):
        print "发送成功！"
    else:
        print "发送失败！"