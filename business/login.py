import json
from jsonpath import jsonpath
import requests
from readConfig import ReadConfig
from log import Log
from jsonpath import jsonpath

readConfig=ReadConfig()
log=Log()

host=readConfig.get_config("HTTP","host")
manager_user=readConfig.get_config("HTTP","manager_user")
manager_pwd=readConfig.get_config("HTTP","manager_pwd")
customer_01_user=readConfig.get_config("HTTP","customer_01_user")
customer_01_pwd=readConfig.get_config("HTTP","customer_01_pwd")
customer_02_user=readConfig.get_config("HTTP","customer_02_user")
customer_02_pwd=readConfig.get_config("HTTP","customer_02_pwd")

def manager_login():
    '''企业业务员登录'''
    manager_s=requests.session()
    path = '/wbalone/account/login'
    params = {
        "username": manager_user,
        "password":manager_pwd
        # "password": get_encrypt_pwd(manager_pwd)
    }
    re = manager_s.post(host + path, data=params)

    result = re.json()
    status = jsonpath(result, '$.status')[0]
    if status == '1':
        log.info('企业业务员登录成功！')
        return manager_s
    else:
        log.info('企业业务员登录失败！')


def customer_01_login():
    customer_01_s = requests.session()
    '''一级渠道商登录'''
    path = '/wbalone/account/login'
    params = {
        "username": customer_01_user,
        # "password": get_encrypt_pwd(customer_01_pwd)
        "password": customer_01_pwd
    }
    re = customer_01_s.post(host + path, data=params)
    result = re.json()
    status = jsonpath(result, '$.status')[0]
    if status == '1':
        log.info('一级渠道商登录登录成功！' )
        return customer_01_s
    else:
        log.info('一级渠道商登录失败！')

def customer_02_login():
    customer_02_s=requests.session()
    '''二级渠道商登录'''
    path = '/wbalone/account/login'
    params = {
        "username": customer_02_user,
        "password": customer_02_pwd
        # "password": get_encrypt_pwd(customer_02_pwd)
    }
    re = customer_02_s.post(host + path, data=params)
    result = re.json()
    status = jsonpath(result, '$.status')[0]
    if status == '1':
        log.info('二级渠道商登录登录成功！' )
        return customer_02_s


def login(user,pwd):
    path = '/wbalone/account/login'
    params = {
        "username": user,
        "password": pwd
    }
    re = requests.session().post(host + path, data=params)
    result = re.json()
    status = jsonpath(result, '$.status')[0]
    if status == '1':
        log.info('用户%s登录成功！'%user)
        return requests.session()

def get_encrypt_pwd(pwd):
    url='http://wws.test.ximalaya.com/occ-tools/getDecryptPwd?&password=%s&profile=&domain='%pwd
    re=requests.get(url)
    result=re.json()
    # print(result)
    pwd_encrypt = jsonpath(result, '$..data')[0]
    # print(pwd_encrypt)
    return pwd_encrypt

# get_encrypt_pwd('111qqq')
# manager_login()
# customer_01_login()
# customer_02_login()