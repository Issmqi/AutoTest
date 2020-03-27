#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
'''

__author__: 'shimengqi'
__description__:'配置日志服务'
__mtime__:2018/2/22
'''
import time
import logging
import logging.config
import os,sys
import setupMain

class Log:
    def __init__(self):
        # proDir = os.path.split(os.path.realpath(__file__))[0]
        # # 连接目录和文件名
        # logConfigPath = os.path.join(proDir, "log.ini")
        # # print("log.ini的路径是",logConfigPath)
        # logging.config.fileConfig(logConfigPath)
        # self.logger = logging.getLogger('request')


        log_path=setupMain.PATH+"/result/log/config.log"
        self.logger=logging.getLogger('request')
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers = []

        fh = logging.FileHandler(log_path, 'a','utf-8')
        fh.setLevel(logging.INFO)

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        # runtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # mk_dir(path + "/log")
        # logfile = path + "/log/" + runtime + '.log'
        # logfile_err = path + "/log/" + runtime + '_error.log'
        #
        # logger = logging.getLogger()
        # logger.setLevel(logging.DEBUG)
        # logger.handlers = []
        #
        # # 第二步，创建一个handler，用于写入全部info日志文件
        #
        # fh = logging.FileHandler(logfile, mode='a+')
        # fh.setLevel(logging.DEBUG)
        #
        # # 第三步，创建一个handler，用于写入错误日志文件
        #
        # fh_err = logging.FileHandler(logfile_err, mode='a+')
        # fh_err.setLevel(logging.ERROR)
        #
        # # 第四步，再创建一个handler，用于输出到控制台
        # ch = logging.StreamHandler(sys.stdout)
        # ch.setLevel(logging.INFO)
        #
        # # 第五步，定义handler的输出格式
        # formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
        # fh.setFormatter(formatter)
        # fh_err.setFormatter(formatter)
        # ch.setFormatter(formatter)
        #
        # # 第六步，将logger添加到handler里面
        # logger.addHandler(fh)
        # logger.addHandler(fh_err)
        # logger.addHandler(ch)





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
