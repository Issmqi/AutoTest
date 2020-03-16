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
    result=checkResult.check_result(case, code, data)
    if result==True:
        return True
    else:
        return False



