# -*- coding: utf-8 -*-


import allure
import initializeCookie
import apiMethod
from log import Log
from readConfig import ReadConfig

readConfig=ReadConfig()
log=Log()

def send_request(request_data):
    '''

    :param request_data: 单条用例数据
    :return:
    '''

    host = ReadConfig().get_config("HTTP", "host")
    casename = request_data['CaseName']
    user = request_data['User']
    header = request_data['Headers']
    method = request_data['Method']
    path = request_data['Path']
    parameter = request_data['Params']

    url = host + path
    if user=='Manager':
        cookie=initializeCookie.get_manager_cookie()
    elif user=='Customer_01':
        cookie=initializeCookie.get_customer_01_cookie()
    elif user=='Customer_02':
        cookie=initializeCookie.get_customer_02_cookie()
    else:
        cookie=None

    log.info("="*100)
    log.info('用例名称:%s'%(casename))
    log.info('请求头:%s'%header)
    log.info('请求地址:%s'%(url))
    log.info('请求参数:%s'%(parameter))
    log.info('测试用户：%s'%(user))

    if method == 'post':
        with allure.step("POST请求接口"):
            allure.attach("请求接口：", str(casename))
            allure.attach("请求地址", url)
            allure.attach("请求头", str(header))
            allure.attach("请求参数", str(parameter))
        result = apiMethod.post(url=url,header=header,data=parameter,cookie=cookie)

    elif method == 'get':
        with allure.step("GET请求接口"):
            allure.attach("请求接口：", str(casename))
            allure.attach("请求地址", url)
            allure.attach("请求头", str(header))
            allure.attach("请求参数", str(parameter))
        result = apiMethod.post(url=url,header=header,data=parameter)

    else:
        result = {"code": False, "data": False}
    log.info("请求接口结果：\n %s" % str(result))
    return result

