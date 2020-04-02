# -*- coding: utf-8 -*-
# !/bin/bash

from readExcel import ReadExcel
from util.log import Log
from util import apiSend_param
log = Log()




def read_relevance_data(case_name,case_address):
    '''
    读取关联case请求参数
    :param case_name: str 被依赖case名称
    :return:关联测试用例
    '''


    # response={}
    # full_data=ReadExcel(case_address).get_full_dict()
    # for i in full_data:
    #     if i['CaseName']==case_name:
    #         url=i['url']
    #         method=
    #         # case_data=i
    #         # result=apiSend_param.send_request(url,method, parameter_type, parameter, cookie, header)
    #         response=result[1]
    #         break
    # if isinstance(response,dict):
    #     print(response)
    #     return response
    # else:
    #     log.info('关联接口未返回dict响应')
    #     return None




