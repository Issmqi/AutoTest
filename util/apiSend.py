# -*- coding: utf-8 -*-

import allure
from business import initializeCookie
from util import apiMethod
from util.log import Log
from util.readConfig import ReadConfig
from business import initializeParameter
from util import writeResult

readConfig = ReadConfig()
log = Log()


def send_request(request_data):
    '''

    :param request_data: 单条用例数据
    :return:
    '''

    host = ReadConfig().get_config("HTTP", "host")
    casename = request_data['CaseName']
    user = request_data['User']
    header = request_data['Headers']
    parameter_type = request_data['ParameterType']
    method = request_data['Method']
    path = request_data['Path']
    parameter = request_data['Params']
    depend_case = request_data['DependCase']
    is_depend = request_data['IsDepend']

    url = host + path
    if user == 'Manager':
        cookie = initializeCookie.get_manager_cookie()
    elif user == 'Customer_01':
        cookie = initializeCookie.get_customer_01_cookie()
    elif user == 'Customer_02':
        cookie = initializeCookie.get_customer_02_cookie()
    else:
        cookie = None

    if depend_case:
        relevance = request_data['RelevanceList']
        parameter = initializeParameter.ini_parameter(depend_case, relevance, parameter)

    log.info("=" * 100)
    log.info('用例名称:%s' % (casename))
    log.info('请求头:%s' % header)
    log.info('请求地址:%s' % (url))
    log.info('请求参数:%s' % (parameter))
    log.info('测试用户：%s' % (user))

    if method == 'post':
        with allure.step("POST请求接口"):
            allure.attach("请求接口：", str(casename))
            allure.attach("请求地址", url)
            allure.attach("请求头", str(header))
            allure.attach("请求参数类型", parameter_type)
            allure.attach("请求参数", str(parameter))
        result = apiMethod.post(url=url, param_type=parameter_type, param=parameter, cookie=cookie, header=header)

    elif method == 'put':
        with allure.step("PUT请求接口"):
            allure.attach("请求接口：", str(casename))
            allure.attach("请求地址", url)
            allure.attach("请求头", str(header))
            allure.attach("请求参数类型", parameter_type)
            allure.attach("请求参数", str(parameter))
        result = apiMethod.put(url=url, param_type=parameter_type, param=parameter, cookie=cookie, header=header)

    elif method == 'get':
        with allure.step("GET请求接口"):
            allure.attach("请求接口：", str(casename))
            allure.attach("请求地址", url)
            allure.attach("请求头", str(header))
            allure.attach("请求参数", str(parameter))
        result = apiMethod.get(url=url, header=header, param=parameter)

    else:
        log.war('请求类型不存在！')
        result = {"code": False, "data": False}

    log.info("返回状态码:%s" % str(result[0]))
    log.info("返回response:\n %s" % result[1])
    # log.info("请求接口结果：\n %s" % str(result))

    if is_depend == 'Yes':
        writeResult.write_result(casename, result)

    return result

