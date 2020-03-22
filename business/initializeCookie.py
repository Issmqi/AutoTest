from jsonpath import jsonpath
import sys,os
path = os.path.dirname(sys.path[0])
# print(path)
sys.path.append(path)
print(sys.path)
import requests
from util.readConfig import ReadConfig
# from readConfig import ReadConfig
from util.log import Log


readConfig=ReadConfig()
log=Log()

host=readConfig.get_config("HTTP","host")
manager_user=readConfig.get_config("HTTP","manager_user")
manager_pwd=readConfig.get_config("HTTP","manager_pwd")
customer_01_user=readConfig.get_config("HTTP","customer_01_user")
customer_01_pwd=readConfig.get_config("HTTP","customer_01_pwd")
customer_02_user=readConfig.get_config("HTTP","customer_02_user")
customer_02_pwd=readConfig.get_config("HTTP","customer_02_pwd")


def login(user,pwd):
    path = '/wbalone/account/login'
    params = {
        "username": user,
        "password": pwd
    }
    re = requests.post(host + path, data=params)
    status = jsonpath(re.json(), '$.status')[0]
    if re.status_code==200:
        if status == '1':
            log.info('用户%s登录成功！'%user)
            cookie=re.cookies
            return cookie
        else:
            log.info('用户%s登录失败！' % user)
            return None
    else:
        raise Exception('HTTP状态码错误！')

def get_manager_cookie():
    return login(manager_user,manager_pwd)

def get_customer_01_cookie():
    return login(customer_01_user,customer_01_pwd)

def get_customer_02_cookie():
    return login(customer_02_user,customer_02_pwd)

def get_encrypt_pwd(pwd):
    url='http://wws.test.ximalaya.com/occ-tools/getDecryptPwd?&password=%s&profile=&domain='%pwd
    re=requests.get(url)
    result=re.json()
    # print(result)
    pwd_encrypt = jsonpath(result, '$..data')[0]
    # print(pwd_encrypt)
    return pwd_encrypt

# get_encrypt_pwd('111qqq')
# get_manager_cookie()
# if __name__ == '__main__':
#
#     customer_01_login()
# customer_02_login()