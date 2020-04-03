# -*- coding: utf-8 -*-
# !/bin/bash

import allure
import setupMain
from business import initializeCookie
from util import apiMethod
from util.log import Log
from util.readConfig import ReadConfig
from util import writeResult

readConfig = ReadConfig()
log = Log()




def send_request(request_data):
    '''

    :param request_data: 单条用例数据
    :return:
    '''

    host = ReadConfig().get_config("HTTP", "host")
    case_name = request_data['CaseName']
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
        from business import initializeParameter
        relevance = request_data['RelevanceList']
        parameter = initializeParameter.ini_parameter(depend_case, relevance, parameter)
        # parameter = initializeParameter.ini_requests(depend_case, relevance, parameter_type)

    log.info("=" * 100)
    log.info('用例名称:%s' % case_name)
    log.info('请求头:%s' % header)
    log.info('请求地址:%s' % url)
    log.info('请求参数:%s' % parameter)
    log.info('测试用户：%s' % user)

    if method == 'post':
        with allure.step("POST请求接口"):
            allure.attach("请求接口:", str(case_name))
            allure.attach("请求地址:", url)
            allure.attach("请求头", header)
            allure.attach("请求参数类型", parameter_type)
            allure.attach("请求参数", parameter)
        result = apiMethod.post(url=url, param_type=parameter_type, param=parameter, cookie=cookie, header=header)

    elif method == 'put':
        with allure.step("PUT请求接口"):
            allure.attach("请求接口：", case_name)
            allure.attach("请求地址", url)
            allure.attach("请求头", header)
            allure.attach("请求参数类型", parameter_type)
            allure.attach("请求参数", parameter)
        result = apiMethod.put(url=url, param_type=parameter_type, param=parameter, cookie=cookie, header=header)

    elif method == 'get':
        with allure.step("GET请求接口"):
            allure.attach("请求接口：", case_name)
            allure.attach("请求地址", url)
            allure.attach("请求头", header)
            allure.attach("请求参数类型", parameter_type)
            allure.attach("请求参数", parameter)
        result = apiMethod.get(url=url, header=header, param=parameter)

    else:
        log.war('请求类型不存在！')
        result = {"code": False, "data": False}

    log.info("返回状态码:%s" % str(result[0]))
    log.info("返回response:\n %s" % result[1])
    # log.info("请求接口结果：\n %s" % str(result))

    if is_depend == 'Yes':
        writeResult.write_result(case_name, result)

    return result


#
address = setupMain.PATH + '/data/testdata.xlsx'
data = {'CaseId': 2.0, 'CaseName': 'get_allocation_bill_detail', 'APIName': '查询调拨订单详情', 'Headers': '',
        'Path': '/occ-stock/stock/allocation-bill/findByParentid', 'Method': 'get', 'ParameterType': 'parameter',
        'Params': '{"id":"040pnM4EHJ4dzuEqtgxG","search_AUTH_APPCODE":"allocation"}', 'CheckTpye': 'check_json',
        'ExpectedCode': 200.0,
        'ExpectedData': '{"id":"0cVwUbuRXnzAhyFKRyaq","dr":0,"ts":1585301477000,"creator":"smq","creationTime":1585301477000,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":null,"state":0,"approver":null,"approveTime":null,"approveOpinion":null,"sycnNCStatus":null,"sycnOutStatus":null,"pkOrgId":"abd7cf79-511d-4307-9bbd-d288b18d0ef9","pkOrgCode":"1210","pkOrgName":"西安喜马拉雅网络科技有限公司","pkOrgInId":"abd7cf79-511d-4307-9bbd-d288b18d0ef9","pkOrgInCode":"1210","pkOrgInName":"西安喜马拉雅网络科技有限公司","code":"DBO20200327000005","billDate":1585238400000,"billType":"Allocation","billTranTypeId":"Allocation","billTranTypeCode":"Allocation","billTranTypeName":"调拨单","outStorageId":"1001ZZ100000000DPAP4","outStorageCode":"test030201","outStorageName":"测试仓库030201","outIfSlotManage":null,"inStorageId":"1001ZZ100000000DPAP6","inStorageCode":"test030202","inStorageName":"test030202","inIfSlotManage":null,"outBizPersonId":"0mWG6nOSCxjsi1zoKEYs","outBizPersonCode":"007","outBizPersonName":"师孟奇","inBizPersonId":"0wsjdHVUBFlca3pyH155","inBizPersonCode":"2539","inBizPersonName":"唐林","outDeptId":"ae96b9ed-82dc-4aa7-bf97-cdd18a18c1a9","outDeptCode":"01010102","outDeptName":"城市经理","inDeptId":"02f265b0-aca6-4364-bd1b-50de07ef9482","inDeptCode":"02","inDeptName":"中台&业务支撑","planSendDate":null,"planArriveDate":null,"currencyId":"CURRENCY-01","currencyCode":"RMB","currencyName":"人民币","totalFactOutNum":null,"totalFactInNum":null,"billStatusId":null,"billStatusCode":null,"billStatusName":null,"transferStatusId":"0s21f51f-4f42-4100-dkd0-3254fbq33e6k","transferStatusCode":"1","transferStatusName":"待处理","stockBillBelong":null,"customerId":null,"customerName":null,"customerCode":null,"isClose":0,"closer":null,"closeDate":null,"closeReason":null,"remark":"自动化测试新增调拨单","transferBillItems":[{"id":"0nDo9IaykpX0aSOxITRr","dr":0,"ts":1585301487000,"creator":"smq","creationTime":1585301487000,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":null,"rowNum":10,"transferBillId":"0cVwUbuRXnzAhyFKRyaq","goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","goodsCode":"301020000049","goodsName":"小雅AI音箱旗舰版_石墨绿","goodsFullName":null,"goodsBasicUnitName":"个","goodsAssistUnitName":"个","goodsConversionRate":1.000000,"enableBatchNumberManage":null,"productId":null,"productLineId":null,"isOptional":null,"unitId":"UNIT-12","unitCode":"EA","unitName":"个","transferNum":5.00000000,"onwayNum":null,"totalOutNum":null,"totalInNum":null,"unitPrice":null,"amountMoney":0E-8,"remark":null,"batchNumId":null,"batchNumCode":null,"batchNumName":null,"goodsPositionId":null,"goodsPositionCode":null,"goodsPositionName":null,"receiverAddress":null,"provinceId":null,"provinceCode":null,"provinceName":null,"cityId":null,"cityCode":null,"cityName":null,"countyId":null,"countyCode":null,"countyName":null,"townId":null,"townCode":null,"townName":null,"detailAddr":null,"receiver":null,"receiverPhone":null,"receiverPhoneSpare":null,"isClose":0,"sourceId":null,"sourceLineNum":null,"sourceType":null,"ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null,"goodsVersion":"1","goodsSelection":null,"isMotherPiece":null,"customerId":null,"customerCode":null,"customerName":null,"supplierId":null,"supplierCode":null,"supplierName":null,"projectId":null,"projectCode":null,"projectName":null,"batchCodeId":null,"batchCodeCode":null,"stockStateId":null,"stockStateCode":null,"stockStateName":null,"enableBatchNoManage":null,"enableInvStatusManage":null,"originalGoodsId":null,"goodsSelectionDescription":null,"outStorageId":"1001ZZ100000000DPAP4","outStorageCode":"test030201","outStorageName":"测试仓库030201","outIfSlotManage":null,"inStorageId":"1001ZZ100000000DPAP6","inStorageCode":"test030202","inStorageName":"test030202","inIfSlotManage":null,"outPositionId":null,"outPositionCode":null,"outPositionName":null}],"transferBillItemBoms":[{"id":"06NAx8X65U6lDo4qq2oJ","dr":0,"ts":1585301487000,"creator":"smq","creationTime":1585301487000,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":null,"rowNum":"10","goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","goodsCode":"301020000049","goodsName":"小雅AI音箱旗舰版_石墨绿","goodsFullName":null,"goodsBasicUnitName":"个","goodsAssistUnitName":"个","goodsConversionRate":1.000000,"enableBatchNumberManage":null,"productId":null,"productLineId":null,"unitId":"UNIT-12","unitCode":"EA","unitName":"个","transferNum":5.00000000,"onwayNum":null,"totalOutNum":null,"totalInNum":null,"unitPrice":null,"amountMoney":0E-8,"remark":null,"batchNumId":null,"batchNumCode":null,"batchNumName":null,"goodsPositionId":null,"goodsPositionCode":null,"goodsPositionName":null,"receiverAddress":null,"provinceId":null,"provinceCode":null,"provinceName":null,"cityId":null,"cityCode":null,"cityName":null,"countyId":null,"countyCode":null,"countyName":null,"townId":null,"townCode":null,"townName":null,"detailAddr":null,"receiver":null,"receiverPhone":null,"receiverPhoneSpare":null,"isClose":0,"sourceId":null,"sourceLineNum":null,"sourceType":null,"ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null,"goodsVersion":"1","goodsSelection":null,"customerId":null,"customerCode":null,"customerName":null,"supplierId":null,"supplierCode":null,"supplierName":null,"projectId":null,"projectCode":null,"projectName":null,"batchCodeId":null,"batchCodeCode":null,"stockStateId":null,"stockStateCode":null,"stockStateName":null,"originalGoodsId":null,"goodsSelectionDescription":null,"itemId":"0nDo9IaykpX0aSOxITRr","billId":"0cVwUbuRXnzAhyFKRyaq","parentGoodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","parentGoodsCode":"301020000049","parentGoodsName":"小雅AI音箱旗舰版_石墨绿","parentGoodsdisplayName":null,"parentRowNum":"10","childGoodsQty":null,"firstBillBomCode":null,"srcBillBomCode":null,"outStorageId":"1001ZZ100000000DPAP4","outStorageCode":"test030201","outStorageName":"测试仓库030201","outIfSlotManage":null,"inStorageId":"1001ZZ100000000DPAP6","inStorageCode":"test030202","inStorageName":"test030202","inIfSlotManage":null,"outPositionId":null,"outPositionCode":null,"outPositionName":null}],"ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null,"isDistribution":null,"isReturned":null}',
        'User': 'Manager', 'DependCase': 'create_allocation_bill', 'RelevanceList': '{"id":"id"}', 'IsDepend': ''}


