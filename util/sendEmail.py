
# -*- coding: utf-8 -*-
# !/bin/bash

import yagmail
from readConfig import ReadConfig
from log import Log

ReadConfig=ReadConfig()
log=Log()

class SendEmail:
    def __init__(self):
        '''从配置文件中读取收发邮箱信息'''
        self.mail_host = ReadConfig.get_config("EMAIL", "mail_host")
        self.mail_user = ReadConfig.get_config("EMAIL", "mail_user")
        self.mail_pass = ReadConfig.get_config("EMAIL", "mail_pass")
        self.mail_port = ReadConfig.get_config("EMAIL", "mail_port")

        self.receiver=ReadConfig.get_config("EMAIL", "receiver")
        self.subject=ReadConfig.get_config("EMAIL","subject")
        self.content=ReadConfig.get_config("EMAIL","content")
        self.on_off=ReadConfig.get_config("EMAIL","on_off")
    def sendEmail(self,report_address):
        content=self.content.encode('utf-8')
        print(self.content)
        if self.on_off=='1':
            try:
                yag=yagmail.SMTP(user=self.mail_user,password=self.mail_pass,host=self.mail_host,port=self.mail_port)
                yag.send(to=self.receiver,subject=self.subject,contents=self.content,attachments=report_address)
                log.info("邮件发送成功!")
            except Exception:
                log.info("邮件发送失败！")
        else:
            log.info("不发送邮件")
def main():

    a=SendEmail()
    a.sendEmail('aaa')
if __name__=='__main__':
    main()












