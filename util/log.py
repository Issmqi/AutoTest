#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
'''

__author__:'shimengqi'
__description__:'配置日志服务'
__mtime__:2018/2/22
'''

import logging
import logging.config
import os

class Log:
    def __init__(self):
        proDir = os.path.split(os.path.realpath(__file__))[0]
        # 连接目录和文件名
        logConfigPath = os.path.join(proDir, "log.ini")
        # print("log.ini的路径是",logConfigPath)
        logging.config.fileConfig(logConfigPath)
        # logging.config.fileConfig('D:/PythonWorkspace/requestTest/util/log.ini')

        # create logger
        self.logger = logging.getLogger('request')

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def war(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)


def main():
    logyyx = Log()
    logyyx.debug('一个debug信息')
    logyyx.info('一个info信息')
    logyyx.war('一个warning信息')
    logyyx.error('一个error信息')
    logyyx.cri('一个致命critical信息')

if __name__ == '__main__':
    main()
