# -*- coding: utf-8 -*-
# !/bin/bash

from readExcel import ReadExcel
import apiSend

from log import Log
log=Log()

def read_relevance_data(case_name):
    '''
    读取关联case请求参数
    :param case_name: str 被依赖case名称
    :return:关联测试用例
    '''
    response={}
    full_data=ReadExcel().get_full_dict()
    for i in full_data:
        if i['CaseName']==case_name:
            case_data=i
            result=apiSend.send_request(case_data)
            response=result[1]
            break
    if isinstance(response,dict):
        return response
    else:
        log.info('关联接口未返回dict响应')
        return None

# read_relevance_data('delete_sales_order')