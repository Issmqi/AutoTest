# -*- coding: utf-8 -*-
from util.log import Log
import allure
import json
import pytest

log = Log()

flag = True


def check_json(src_data, res_data):
    '''
    校验返回json格式是否和预期一致
    :param src_data: 校验数据
    :param res_data: 接口返回数据
    :return:
    '''

    global flag

    if isinstance(src_data, dict):

        for key in src_data:
            # print('flag是', flag)
            if not flag:
                return False
            if key not in res_data:
                log.info("JSON格式校验，关键字%s不在返回结果%s中" % (key, res_data))
                flag = False

                # raise Exception("JSON格式校验，关键字%s不在返回结果%s中" % (key, res_data))
            else:
                this_key = key
                if isinstance(src_data[this_key], dict) and isinstance(res_data[this_key], dict):
                    check_json(src_data[this_key], res_data[this_key])  # 递归执行check_json

                elif type(src_data[this_key]) != type(res_data[this_key]):
                    log.info("json格式校验，校验关键字%s与返回关键字%s类型不一致" % (src_data[this_key], res_data[this_key]))
                    flag = False
                    # return flag
                    # raise Exception("json格式校验，校验关键字%s与返回关键字%s类型不一致"%(src_data[this_key],res_data[this_key]))
                else:
                    # print('%s校验通过'%this_key)
                    pass

    else:

        log.error("json校验数据不是dict类型")
        return False
        # raise Exception("json校验数据非dict类型")


def check_result(case, code, res_data):
    '''

    :param case: 用例数据
    :param code: 接口返回 HTTP状态码
    :param res_data: 接口返回数据
    :return:
    '''
    check_type = case['CheckTpye']

    if check_type == 'no_check':
        with allure.step('接口无需校验'):
            return True
    elif check_type == 'only_check_status':
        with allure.step('接口仅校验HTTP状态码'):
            allure.attach('预期code是', int(case['ExpectedCode']))
            allure.attach('实际code是', str(code))
            allure.attach('实际data是', str(res_data))
        if code == int(case['ExpectedCode']):
            log.info("HTTP状态码校验通过！")
            return True
        else:
            log.info(("HTTP返回状态码与预期不一致"))
            # raise Exception("HTTP返回状态码与预期不一致")
            return False

    elif check_type == 'check_json':
        with allure.step("校验返回json数据结构"):
            allure.attach('预期code是', int(case['ExpectedCode']))
            allure.attach('实际code是', str(code))
            allure.attach('预期data是', str(case['ExpectedData']))
            allure.attach('实际data是', str(res_data))
            if code == int(case['ExpectedCode']):
                if not res_data:  # 判断res_data为None,  False, 空字符串"", 0, 空列表[], 空字典{}, 空元组()
                    res_data = '{}'
                else:
                    expected_data_dict = json.loads(case['ExpectedData'])
                    result = check_json(expected_data_dict, res_data)
                    if result == False:
                        log.info('JSON格式校验失败！')
                        return False
                    else:
                        log.info('JSON格式校验成功！')
                        return True
            else:
                # raise Exception("HTTP返回状态码与预期不一致")
                log.info("HTTP返回状态码%s与预期%s不一致" % (str(code), int(case['ExpectedCode'])))
                return False
    else:
        log.error('校验类型不存在！')
