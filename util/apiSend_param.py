# -*- coding: utf-8 -*-
# !/bin/bash

import allure
from business import initializeCookie
from util import apiMethod
from util.log import Log
from util.readConfig import ReadConfig
from business import initializeParameter
from util import writeResult

readConfig = ReadConfig()
log = Log()


def send_request(url,method, parameter_type, parameter, cookie, header):
    '''

    :param request_data: 单条用例数据
    :return:
    '''



    # if depend_case:
    #     relevance = request_data['RelevanceList']
    #     # parameter = initializeParameter.ini_parameter(depend_case, relevance, parameter)
    #     parameter = initializeParameter.ini_requests(depend_case, relevance, parameter_type)

    if method == 'post':
        result = apiMethod.post(url=url, param_type=parameter_type, param=parameter, cookie=cookie, header=header)

    elif method == 'put':
        result = apiMethod.put(url=url, param_type=parameter_type, param=parameter, cookie=cookie, header=header)

    elif method == 'get':
        result = apiMethod.get(url=url, header=header, param=parameter)

    else:
        log.war('请求类型不存在！')
        result = {"code": False, "data": False}

    log.info("返回状态码:%s" % str(result[0]))
    log.info("返回response:\n %s" % result[1])
    # log.info("请求接口结果：\n %s" % str(result))

    # if is_depend == 'Yes':
    #     writeResult.write_result(case_name, result)

    return result
