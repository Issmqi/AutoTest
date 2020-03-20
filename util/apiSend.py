# -*- coding: utf-8 -*-

import allure
import initializeCookie
import apiMethod
from log import Log
from readConfig import ReadConfig
import initializeParameter
import writeResult

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
    parameter_type=request_data['ParameterType']
    method = request_data['Method']
    path = request_data['Path']
    parameter = request_data['Params']
    depend_case=request_data['DependCase']
    is_depend=request_data['IsDepend']


    url = host + path
    if user=='Manager':
        cookie=initializeCookie.get_manager_cookie()
    elif user=='Customer_01':
        cookie=initializeCookie.get_customer_01_cookie()
    elif user=='Customer_02':
        cookie=initializeCookie.get_customer_02_cookie()
    else:
        cookie=None


    if depend_case:
        relevance=request_data['RelevanceList']
        parameter=initializeParameter.ini_parameter(depend_case,relevance,parameter)


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
        # result = apiMethod.post(url=url,header=header,data=parameter,cookie=cookie)
        result = apiMethod.post_2(url=url, param_type=parameter_type, param=parameter, cookie=cookie,header=header)

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

    if is_depend=='Yes':
        writeResult.write_result(casename,result)

    return result

# data={'CaseId': 5.0, 'Designer': '师孟奇', 'CaseName': 'submit_purchase_order', 'APIName': '提交外部采购订单', 'ParameterType': 'parameter', 'Headers': "{'Content-Type':'application/json','charset': 'UTF-8'}", 'Path': '/occ-purchase/purchase/orders/submitWithoutBpm', 'Method': 'post', 'Params': '{"billId":"0S9WknJXMVYbEHf3qGGc"}', 'CheckTpye': 'check_json', 'ExpectedCode': '200', 'ExpectedData': '{"success":"success","message":null,"detailMsg":{"data":null}}', 'User': 'Manager', 'DependCase': 'create_common_purchase_order', 'RelevanceList': '{"billId":"id"}', 'IsDepend': '{"billId":"id"}'}
# #
# send_request(data)