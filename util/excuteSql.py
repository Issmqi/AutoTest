'''
__author__:'shimengqi'
__description__:'执行sql'
__mtime__:2020/05/07
'''

import setupMain
import pymysql
from util.log import Log
from util.readConfig import ReadConfig

log = Log()


class ExecuteSQL:
    def __init__(self):
        self.host = ReadConfig().get_config("DATABASE", "hostname")
        self.user = ReadConfig().get_config("DATABASE", "username")
        self.password = ReadConfig().get_config("DATABASE", "password")
        self.database = ReadConfig().get_config("DATABASE", "database")

    def _cursor(self):
        '''
        获取游标
        :return:
        '''
        if not self.database:
            raise (NameError, '未设置数据库信息')
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def select_sql(self, sql):
        '''
        执行查询sql
        :param sql:
        :return: 查询结果
        '''
        cur = self._cursor()
        cur.execute(sql)
        resList = cur.fetchall()
        self.conn.close()
        return resList

    def excute_sql(self, sql):
        '''
        执行增删改sql
        :param sql:
        :return:
        '''
        cur = self._cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
        except e:
            print(e)
            self.conn.rollback()  # 执行sql失败回滚
            self.conn.close()

    def execute_scripts_from_file(self, filename):
        '''
        执行sql脚本
        :param filename:
        :return:
        '''
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                sqlFile = f.read()
                sqlFile=sqlFile.replace('\n','')
                sqlCommands = sqlFile.split(';')
                sqlCommands.pop(-1)
                # print('sql列表是',sqlCommands)
                cursor = self._cursor()
                for command in sqlCommands:
                    # print('当前命令行是：',command)
                    try:
                        cursor.execute(command)
                        self.conn.commit()
                    except Exception as e:
                        log.error(e)
                        self.conn.rollback()  # 执行sql失败回滚
                        self.conn.close()
                log.info('sql执行完成！')

        except Exception as e:
            log.error('读取sql文件失败！')
            log.error(e)

    def execute_scripts_from_file_bat(self, filename):
        '''
        执行sql脚本批量操作
        :param filename:
        :return:
        '''
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                sqlFile = f.read()
                # print('文件是',sqlFile)
                sqlCommands = sqlFile.split(';')
                cursor = self._cursor()
                for command in sqlCommands:
                    # print(command)
                    try:
                        cursor.executemany(command)
                        self.conn.commit()
                    except Exception as e:
                        log.error(e)
                        self.conn.rollback()  # 执行sql失败回滚
                        self.conn.close()
                log.info('SQL执行完成！')

        except Exception as e:
            log.error('SQL执行失败！！')
            log.error(e)

if __name__ == '__main__':

    e = ExecuteSQL()
    # # sql = "insert ignore into stock_transfer_bill " \
    #       "(ID,STOCK_ORG,STOCK_ORG_IN,BILL_CODE,BILL_DATE,BILL_TYPE,BILL_TRAN_TYPE,OUT_STORAGE,IN_STORAGE,TRANSFER_STATUS) " \
    #       "values " \
    #       "('allocationiddnjdjhe','abd7cf79-511d-4307-9bbd-d288b18d0ef9','abd7cf79-511d-4307-9bbd-d288b18d0ef9','DBO20200507000100',now()," \
    #       "'Allocation','Allocation','1001ZZ100000000DPAP4','1001ZZ100000000DPAP6','2')"
    # sql="delete from stock_transfer_bill where id ='allocation-add-and-approve'"
    # e.excute_sql(sql)
    # # path=setupMain.PATH + '/data/allocation_sql'
    path=setupMain.PATH + '/data/allocation/allocation_setup_sql'
    e.execute_scripts_from_file(path)
