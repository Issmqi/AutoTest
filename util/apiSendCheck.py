# -*- coding: utf-8 -*-

import apiSend
import checkResult

def api_send_check(case):
    """
    接口请求并校验结果
    :param case: 单条用例
    :return:
    """
    code, data = apiSend.send_request(case)
    # result=apiSend.send_request(case)

    print(code)
    print(data)
    result=checkResult.check_result(case, code, data)
    if result==True:
        return True
    else:
        return False

# data={'CaseId': 2.0, 'Designer': '师孟奇', 'CaseName': 'delete_sales_order', 'APIName': '删除销售订单', 'ParameterType': 'form_data', 'Headers': "{'Content-Type':'application/x-www-form-urlencoded','charset': 'UTF-8'}", 'Path': '/occ-b2b-order/b2b/order/delete', 'Method': 'post', 'Params': '{"ids":"02R6zxnuQ30MkkRoltEu","search_AUTH_APPCODE":"saleorder"}', 'CheckTpye': 'only_check_status', 'ExpectedCode': 200.0, 'ExpectedData': '', 'User': 'Manager', 'DependCase': 'create_sales_order', 'RelevanceList': '{"ids":"id"}', 'IsDepend': ''}
#
# api_send_check(data)
