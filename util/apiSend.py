# -*- coding: utf-8 -*-

import allure
from business import initializeCookie
from util import apiMethod
from util.log import Log
from util.readConfig import ReadConfig
from business import initializeParameter
from util import writeResult

readConfig = ReadConfig()
log = Log()


def send_request(request_data):
    '''

    :param request_data: 单条用例数据
    :return:
    '''

    host = ReadConfig().get_config("HTTP", "host")
    casename = request_data['CaseName']
    print(casename)
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
        relevance = request_data['RelevanceList']
        parameter = initializeParameter.ini_parameter(depend_case, relevance, parameter)

    log.info("=" * 100)
    log.info('用例名称:%s' % (casename))
    log.info('请求头:%s' % header)
    log.info('请求地址:%s' % (url))
    log.info('请求参数:%s' % (parameter))
    log.info('测试用户：%s' % (user))

    if method == 'post':
        with allure.step("POST请求接口"):
            allure.attach("请求接口:", casename)
            allure.attach("请求地址:", url)
            allure.attach("请求头", header)
            allure.attach("请求参数类型", parameter_type)
            allure.attach("请求参数", parameter)
        result = apiMethod.post(url=url, param_type=parameter_type, param=parameter, cookie=cookie, header=header)

    elif method == 'put':
        with allure.step("PUT请求接口"):
            allure.attach("请求接口：", casename)
            allure.attach("请求地址", url)
            allure.attach("请求头", header)
            allure.attach("请求参数类型", parameter_type)
            allure.attach("请求参数", parameter)
        result = apiMethod.put(url=url, param_type=parameter_type, param=parameter, cookie=cookie, header=header)

    elif method == 'get':
        with allure.step("GET请求接口"):
            allure.attach("请求接口：", casename)
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
        writeResult.write_result(casename, result)

    return result
#
# data={'CaseId': 18.0, 'CaseName': 'create_other_out_stock', 'APIName': '新增其他出库', 'Headers': '{"Content-Type":"application/json","charset": "UTF-8"}', 'Path': '/occ-stock/stock/other-out-bills', 'Method': 'post', 'ParameterType': 'json', 'Params': '{"id":null,"stockOrgId":"abd7cf79-511d-4307-9bbd-d288b18d0ef9","stockOrgCode":null,"stockOrgName":null,"stockOutCode":null,"billType":"OtherOut","stockOutStorageId":"0bxYF73VWxwqf6bb3ib4","stockOutStorageCode":null,"stockOutStorageName":null,"ifSlotManage":"0","tranTypeId":"OtherOut","tranTypeCode":null,"tranTypeName":null,"storageAdminId":null,"storageAdminCode":null,"storageAdminName":null,"bizPersonId":null,"bizPersonCode":null,"bizPersonName":null,"deptId":"0K1ovYvAl1Pk00oCRPjV","deptCode":null,"deptName":null,"totalFactOutNum":"5.00","remark":"自动化测试其他出库，小雅石墨绿*5","statusId":null,"statusCode":"01","statusName":null,"isOwner":null,"stockInDate":null,"stockInPerson":null,"signDate":"","signPerson":null,"billDate":1584979200000,"currencyId":null,"currencyCode":null,"currencyName":null,"ext13":null,"ext12":null,"ext11":null,"ext10":null,"ext09":null,"ext08":null,"ext07":null,"lingLiaoOrgId":null,"lingLiaoOrgCode":null,"lingLiaoOrgName":null,"lingLiaoDeptId":null,"lingLiaoDeptCode":null,"lingLiaoDeptName":null,"lingLiaoPersionId":null,"lingLiaoPersionCode":null,"lingLiaoPersionName":null,"logisticsBillCode":null,"realLogisticsCompanyId":null,"realLogisticsCompanyCode":null,"realLogisticsCompanyName":null,"ext05":null,"ext04":null,"ext03":null,"ext02":null,"signPersonName":null,"persistStatus":"new","otherOutBillItems":[{"id":null,"otherOutId":null,"rowNum":10,"goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","goodsCode":"301020000049","goodsName":"小雅AI音箱旗舰版_石墨绿","enableBatchNumberManage":"0","enableBatchNoManage":"0","enableInvStatusManage":"0","isOptional":null,"productId":"996cc839-60e8-4500-82c6-9a7c7b95646d","productLineId":"13c512df-ad18-48e5-b75d-166a534cc410","shouldOutNum":"5.000000","unitPrice":"1.000000","amountMoney":"5.00","factOutNum":"5.000000","remark":null,"stockOutDate":"","stockOutPersonId":null,"stockOutPersonCode":null,"stockOutPersonName":null,"srcBillCode":null,"srcBillBcode":null,"srcBillType":null,"batchNumId":null,"batchNumCode":null,"batchNumName":null,"goodsPositionId":null,"goodsPositionCode":null,"goodsPositionName":null,"unitId":"UNIT-12","unitCode":"EA","unitName":"个","dr":null,"goodsVersion":"1","batchCodeId":null,"batchCodeCode":null,"batchCodeName":null,"supplierId":null,"supplierName":null,"supplierCode":null,"projectId":null,"projectCode":null,"projectName":null,"stockStateId":null,"stockStateCode":null,"stockStateName":null,"customerId":null,"customerCode":null,"customerName":null,"originalGoodsId":null,"goodsSelection":null,"goodsSelectionDescription":null,"persistStatus":"new"}],"otherOutBillItemBoms":[{"id":null,"otherOutId":null,"rowNum":10,"goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","goodsCode":"301020000049","goodsName":"小雅AI音箱旗舰版_石墨绿","enableBatchNumberManage":"0","enableBatchNoManage":"0","enableInvStatusManage":"0","productId":"996cc839-60e8-4500-82c6-9a7c7b95646d","productLineId":"13c512df-ad18-48e5-b75d-166a534cc410","shouldOutNum":"5.000000","unitPrice":"1.000000","amountMoney":"0.00","factOutNum":"5.000000","remark":null,"stockOutDate":"","stockOutPersonId":null,"stockOutPersonCode":null,"stockOutPersonName":null,"srcBillCode":null,"srcBillBcode":null,"srcBillType":null,"batchNumId":null,"batchNumCode":null,"batchNumName":null,"goodsPositionId":null,"goodsPositionCode":null,"goodsPositionName":null,"unitId":"UNIT-12","unitCode":"EA","unitName":"个","dr":null,"goodsVersion":"1","goodsSelection":null,"goodsNum":null,"parentGoodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","parentGoodsCode":null,"parentGoodsName":null,"childGoodsQty":null,"parentRowNum":10,"batchCodeId":null,"batchCodeCode":null,"batchCodeName":null,"supplierId":null,"supplierName":null,"supplierCode":null,"projectId":null,"projectCode":null,"projectName":null,"stockStateId":null,"stockStateCode":null,"stockStateName":null,"customerId":null,"customerCode":null,"customerName":null,"originalGoodsId":null,"goodsSelectionDescription":null,"isOptional":null,"persistStatus":"new"}]}', 'CheckTpye': 'check_json', 'ExpectedCode': 200.0, 'ExpectedData': '{"id":"0iDSPPZdf975pHNp620g","dr":0,"ts":1585033571000,"creator":"gaojian","creationTime":1585033571000,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":"","stockOrgId":"abd7cf79-511d-4307-9bbd-d288b18d0ef9","stockOrgCode":"1210","stockOrgName":"西安喜马拉雅网络科技有限公司","stockOutStorageId":"0bxYF73VWxwqf6bb3ib4","stockOutStorageCode":"2123445","stockOutStorageName":"曲江书城店仓","ifSlotManage":null,"bizPersonId":null,"bizPersonCode":null,"bizPersonName":null,"deptId":"0K1ovYvAl1Pk00oCRPjV","deptCode":"01010102","deptName":"城市经理","storageAdminId":null,"storageAdminCode":null,"storageAdminName":null,"statusId":"099aj5df-4y42-4700-d8d6-3714fdb43e68","statusCode":"01","statusName":"自由","remark":"自动化测试其他出库，小雅石墨绿*5","tranTypeId":"OtherOut","tranTypeCode":"OtherOut","tranTypeName":"其他出库","code":null,"otherOutBillItemBoms":[{"id":"0d1Mf24YmIAsHomOGlET","dr":0,"ts":1585033579000,"creator":"gaojian","creationTime":1585033579000,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":null,"rowNum":"10","goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","goodsCode":"301020000049","goodsName":"小雅AI音箱旗舰版_石墨绿","shouldOutNum":5.00000000,"unitPrice":1.00000000,"amountMoney":0E-8,"factOutNum":5.00000000,"isGift":null,"remark":null,"stockOutDate":null,"stockOutPerson":null,"srcBillCode":null,"srcBillBcode":null,"srcBillType":null,"firstBillCode":null,"firstBillBcode":null,"firstBillType":null,"batchNumId":null,"batchNumName":null,"goodsPositionId":null,"goodsPositionCode":null,"goodsPositionName":null,"unitId":"UNIT-12","unitCode":"EA","unitName":"个","goodsVersion":"1","goodsSelection":null,"goodsSelectionDescription":null,"customerId":null,"customerCode":null,"customerName":null,"supplierId":null,"supplierCode":null,"supplierName":null,"projectId":null,"projectCode":null,"projectName":null,"batchCodeId":null,"batchCodeCode":null,"stockStateId":null,"stockStateCode":null,"stockStateName":null,"itemId":"0HuHDvXUGP3FERXQS9IR","billId":null,"parentGoodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","parentGoodsCode":"301020000049","parentGoodsName":"小雅AI音箱旗舰版_石墨绿","parentGoodsDisplayName":"小雅AI音箱旗舰版_石墨绿","parentRowNum":"10","childGoodsQty":null,"firstBillBomCode":null,"srcBillBomCode":null,"originalGoodsId":null,"ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null}],"srcBillId":null,"materialOutPersonId":null,"materialOutPersonCode":null,"materialOutPersonName":null,"applyCustomerId":null,"applyCustomerCode":null,"applyCustomerName":null,"srcSystem":null,"srcSystemId":null,"srcSystemCode":null,"srcSystemName":null,"abnormalSingleNum":null,"provinceAreaId":null,"provinceAreaCode":null,"provinceAreaName":null,"ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext15":null,"ext06":null,"ext13":null,"ext12":null,"ext11":null,"ext10":null,"ext09":null,"ext08":null,"ext07":null,"sycnOutStatus":null,"sycnNCStatus":null,"lingLiaoOrgId":null,"lingLiaoOrgCode":null,"lingLiaoOrgName":null,"lingLiaoDeptId":null,"lingLiaoDeptCode":null,"lingLiaoDeptName":null,"lingLiaoPersionId":null,"lingLiaoPersionCode":null,"lingLiaoPersionName":null,"stockOutCode":"ODN20200324000002","otherOutType":null,"billDate":1584979200000,"totalFactOutNum":5.00000000,"billType":"OtherOut","isOwner":null,"stockOutDate":1585033579000,"stockOutPersonId":null,"stockOutPersonCode":null,"stockOutPersonName":null,"signPersonId":null,"signPersonCode":null,"signPersonName":null,"signDate":null,"currencyId":null,"currencyCode":null,"currencyName":null,"ext14":null,"realLogisticsCompanyId":null,"realLogisticsCompanyCode":null,"realLogisticsCompanyName":null,"logisticsBillCode":null,"otherOutBillItems":[{"id":"0HuHDvXUGP3FERXQS9IR","dr":0,"ts":1585033579000,"creator":"gaojian","creationTime":1585033579000,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":null,"rowNum":"10","goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","goodsCode":"301020000049","goodsName":"小雅AI音箱旗舰版_石墨绿","enableBatchNumberManage":null,"productId":null,"productLineId":null,"isOptional":null,"shouldOutNum":5.00000000,"unitPrice":1.00000000,"amountMoney":5.00000000,"factOutNum":5.00000000,"isGift":null,"remark":null,"stockOutDate":1585033579000,"stockOutPersonId":null,"stockOutPersonCode":null,"stockOutPersonName":null,"srcBillCode":null,"srcBillBcode":null,"srcBillType":null,"firstBillCode":null,"firstBillBcode":null,"firstBillType":null,"batchNumId":null,"batchNumName":null,"goodsPositionId":null,"goodsPositionCode":null,"goodsPositionName":null,"unitId":"UNIT-12","unitCode":"EA","unitName":"个","goodsVersion":"1","goodsSelection":null,"isMotherPiece":null,"customerId":null,"customerCode":null,"customerName":null,"supplierId":null,"supplierCode":null,"supplierName":null,"projectId":null,"projectCode":null,"projectName":null,"batchCodeId":null,"batchCodeCode":null,"enableBatchNoManage":null,"stockStateId":null,"stockStateCode":null,"stockStateName":null,"enableInvStatusManage":null,"originalGoodsId":null,"goodsSelectionDescription":null,"signNumAmount":null,"ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null,"abnormalSingleNum":null}],"promotionalType":null}', 'User': 'Manager', 'DependCase': '', 'RelevanceList': '', 'IsDepend': 'Yes'}
# send_request(data)
