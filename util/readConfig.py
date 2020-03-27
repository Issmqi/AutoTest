# -*- coding: utf-8 -*-
# !/bin/bash

'''
__author__:'shimengqi'
__description__:'读取配置文件信息'
__mtime__:2018/2/10
'''
import os
import configparser
from util import log
log=log.Log()

proDir = os.path.split(os.path.realpath(__file__))[0]   # 获取当前py文件地址
configPath = os.path.join(proDir, "config.ini")         # 组合config文件地址
# print("config.ini的路径是",configPath)


class ReadConfig:
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath,encoding="utf-8-sig")

    def get_config(self, field, key):
        '''获取config.ini信息'''
        result = self.cf.get(field, key)
        # log.debug('%s的%s是：%s' % (field, key, result))
        return result

    def set_config(self, field, key, value):
        '''修改config.ini信息'''
        fd = open(configPath, "w")
        self.cf.set(field, key, value)
        log.debug('%s的%s修改成功 ,value=%s' % (field, key, value))
        self.cf.write(fd)


def main():
    config = ReadConfig()
    config.get_config("DATABASE", "data_address")
if __name__ == '__main__':
    main()