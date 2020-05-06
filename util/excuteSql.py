import pymysql
from util.readConfig import ReadConfig

class ExecuteSQL:
    def __init__(self):
        self.host=ReadConfig().get_config("DATABASE","hostname")
        self.user = ReadConfig().get_config("DATABASE", "username")
        self.password = ReadConfig().get_config("DATABASE", "password")
        self.database = ReadConfig().get_config("DATABASE", "database")




    def _cursor(self):
        if not self.database:
            raise(NameError,'未设置数据库信息')
        self.conn=pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database)
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def select_sql(self,sql):
        cur=self._cursor()
        cur.execute(sql)
        resList=cur.fetchall()
        self.conn.close()
        return resList

    def excute_sql(self,sql):
        cur=self._cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()#执行sql失败回滚
            self.conn.close()









