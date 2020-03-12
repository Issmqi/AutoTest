import allure

def check_json(src_data,res_data):
    '''
    递归
    校验返回json数据结构是否和预期一致
    :param src_data: 校验数据
    :param res_data: 接口返回数据
    :return:
    '''

    if isinstance(src_data,dict):
        for key in src_data:
            if key in res_data:
                this_key=key
                if isinstance(src_data[this_key],dict) and isinstance(res_data[this_key],dict):
                    check_json(src_data[this_key],res_data[this_key])#递归执行check_json
                elif isinstance(type(src_data[this_key]),type(res_data[this_key])) is False:
                    raise Exception("json格式校验，校验关键字%s与返回关键字%s不一致"%(src_data[this_key],res_data[this_key]))
                else:
                    pass

            else:
                raise Exception("json格式校验，关键字%s不在返回数据%s中" %(key,res_data))
    else:
        raise Exception("json校验数据不是dict类型")

def check_result(case,code,res_data):
    '''

    :param case: 用例数据
    :param code: 接口返回 HTTP状态码
    :param res_data: 接口返回数据
    :return:
    '''
    check_type=case['check_type']

    if check_type=='no_check':
        with allure.step('接口无需校验'):
            pass
    elif check_type=='check_status':
        with allure.step('接口仅校验HTTP状态码'):
            allure.attach('预期code是', str(case['ExpectedCode']))
            allure.attach('实际code是', str(code))
            allure.attach('实际data是', str(res_data))
        if code==case['expected_code']:
            pass
        else:
            raise Exception("HTTP返回状态码与预期不一致")

    elif check_type=='check_json':
        with allure.step("校验返回json数据结构"):
            allure.attach('预期code是', str(case['ExpectedCode']))
            allure.attach('实际code是', str(code))
            allure.attach('预期data是', str(case['ExpectedData']))
            allure.attach('实际data是', str(res_data))
            if code==case['expected_code']:
                if not res_data:#判断res_data为None,  False, 空字符串"", 0, 空列表[], 空字典{}, 空元组()
                    res_data='{}'
                else:
                    check_json(case['ExpectedData'],res_data)
            else:
                raise Exception("HTTP返回状态码与预期不一致")










