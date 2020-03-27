# -*- coding: utf-8 -*-
# !/bin/bash


import setupMain
# import readrelevanceData
import allure
import json
from jsonpath import jsonpath
from util.log import Log

log = Log()


def ini_parameter(dependCase, relevanceList, parameter):
    '''
    读取关联case的response文件,获取关键字并修改
    :param dependCase: 依赖的caseName str
    :param relevanceList: 依赖的关键字 str
    :param parameter: 请求参数 str
    :return:
    '''
    param_dict = json.loads(parameter)
    relevance_dict = json.loads(relevanceList)
    path = setupMain.json_result_path + dependCase + '_result.json'
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            for key in relevance_dict:
                relevance_key = relevance_dict[key]
                if relevance_key in data:
                    param_dict[key] = jsonpath(data, '$..%s' % relevance_key)[0]
                else:
                    log.error('参数依赖关键字%s在关联结果中找不到' % relevance_key)

            # print('更新后params是：',param_dict)
            return json.dumps(param_dict)
    except FileNotFoundError:
        raise Exception("用例关联文件不存在\n文件路径： %s" % path)

# def ini_requests(dependCase,relevance,parameter):
#     '''
#     执行关联的用例，并更新参数
#     :param dependCase: 关联case_name str
#     :param relevance: 关联信息 str '{"key":"relevance_key"}'
#     :param parameter: 请求参数 str
#     :return: 替换后的请求参数
#     '''
#
#     response=readrelevanceData.read_relevance_data(dependCase)
#     if response:  #关联接口返回不为空
#         param_dict=json.loads(parameter)
#         relevance_dict = json.loads(relevance)
#         for key in relevance_dict:
#             relevance_key=relevance_dict[key]
#             if relevance_key in response:
#                 param_dict[key]=jsonpath(response,'$..%s'%relevance_key)[0]
#             else:
#                 log.info('关联接口响应中找不到关键字%s'%relevance_key)
#     else:
#         log.info('关联接口响应为空！')
# relevanceCase='create_sales_order'
# relevanceKeys=[{"ids":"id"}]
# param={"ids": "02R6zxnuQ30MkkRoltEu","search_AUTH_APPCODE ":"saleorder"}
#
# param_str=json.dumps(param)
#
# ini_parameter(relevanceCase,relevanceKeys,param_str)
