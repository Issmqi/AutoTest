# -*- coding: utf-8 -*-
# !/bin/bash

import allure
import requests
import json
from jsonpath import jsonpath
import simplejson
import setupMain
from business import initializeCookie
from util import apiMethod
from util.log import Log
from util.readExcel import ReadExcel
from util.readConfig import ReadConfig
from util import writeResult

readConfig = ReadConfig()
log = Log()


class HttpClient():
    def __init__(self, full_dict):
        self.full_dict = full_dict

    def send_requests(self, request_data):
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
            # parameter = self.ini_parameter(depend_case, relevance, parameter)
            parameter = self.init_request(depend_case, relevance, parameter)

        log.info("=" * 100)
        log.info('用例名称:%s' % case_name)
        log.info('请求头:%s' % header)
        log.info('请求地址:%s' % url)
        log.info('请求参数:%s' % parameter)
        log.info('测试用户：%s' % user)

        with allure.step("开始请求接口"):
            allure.attach("请求类型", method)
            allure.attach("用例名称:", case_name)
            allure.attach("请求地址:", url)
            allure.attach("请求头", header)
            allure.attach("请求参数类型", parameter_type)
            allure.attach("请求参数", parameter)

        result = self.api_send(method, url, parameter, cookie, header, parameter_type)
        log.info("返回状态码:%s" % str(result[0]))
        log.info("返回response:\n %s" % result[1])

        return result

    def api_send(self, method, url, param, cookie, header=None, param_type=None):
        '''

        :param method: 请求类型 str post/put/get
        :param url: 请求路径 str
        :param param: 请求参数 str
        :param cookie:
        :param header:
        :param param_type: 请求参数类型 str json/form_data/parameter
        :return:
        '''
        if header:
            header = eval(header)
        if not param:
            param_dict = None
        else:
            param_dict = json.loads(param)
        response = {}

        if method == 'post':
            if param_type == 'json':
                params = json.dumps(param_dict)
                response = requests.post(url=url, headers=header, data=params, cookies=cookie)
            elif param_type == 'form_data':
                response = requests.post(url=url, headers=header, data=param_dict, cookies=cookie)
            elif param_type == 'parameter':
                response = requests.post(url=url, headers=header, params=param_dict, cookies=cookie)
            else:
                response = None
                log.error('post参数类型不存在')

        elif method == 'put':
            if param_type == 'json':
                params = json.dumps(param_dict)
                response = requests.put(url=url, headers=header, data=params, cookies=cookie)
            elif param_type == 'form_data':
                response = requests.put(url=url, headers=header, data=param_dict, cookies=cookie)
            elif param_type == 'parameter':
                response = requests.put(url=url, headers=header, params=param_dict, cookies=cookie)
            else:
                response = None
                log.error('参数类型不存在')

        elif method == 'get':
            response = requests.get(url=url, headers=header, params=param_dict)
            if response.status_code == 301:
                response = requests.get(url=response.headers['location'])

        else:
            log.error('请求类型不存在！')

        times = response.elapsed.total_seconds()
        log.info('响应时间为%ss' % times)
        try:
            if response.status_code != 200:
                return response.status_code, response.text
            else:
                return response.status_code, response.json()

        except json.decoder.JSONDecodeError:
            return response.status_code, {}
        except simplejson.errors.JSONDecodeError:
            return response.status_code, {}
        except Exception as e:
            log.war('ERROR')
            log.error(e)

    def init_request(self, dependCase, relevance, parameter):
        '''
        请求前执行依赖接口，处理依赖参数
        :param dependCase:dict 关联接口casename
        :param relevance:dict 关联键值对
        :param parameter: str 接口请求参数
        :return: parameter: str
        '''
        relevance_response = self.read_relevance_data(dependCase)  # 执行依赖接口
        if not relevance_response:
            return parameter
        if not relevance:
            return parameter

        else:
            param_dict = json.loads(parameter)
            relevance_dict = json.loads(relevance)
            for key in relevance_dict:
                relevance_key = relevance_dict[key]
                try:
                    param_dict[key] = jsonpath(relevance_response, 'relevance_key')[0]
                    log.info('替换后参数是:%s' % param_dict)
                except Exception as e:
                    log.info('关联接口响应中找不到关键字%s' % relevance_key)
                    log.error(e)
            return json.dumps(param_dict)

    def ini_parameter(self, dependCase, relevance, parameter):
        '''
        初始化有依赖关系的参数
        :param dependCase:dict
        :param relevance:dict
        :param parameter: str
        :return: parameter: str
        '''
        relevance_response = self.read_relevance_data(dependCase)
        if relevance_response:  # 关联接口返回不为空
            param_dict = json.loads(parameter)
            relevance_dict = json.loads(relevance)
            for key in relevance_dict:
                relevance_key = relevance_dict[key]
                try:
                    param_dict[key] = jsonpath(relevance_response, '$..%s' % relevance_key)[0]
                    log.info('替换后参数是:%s' % param_dict)
                except Exception as e:
                    log.info('关联接口响应中找不到关键字%s' % relevance_key)
                    log.error(e)
                # if relevance_key in relevance_response:
                #     param_dict[key] = jsonpath(relevance_response, '$..%s' % relevance_key)[0]
                #     log.info('替换后参数是:%s'%param_dict)
                # else:
                #     log.info('关联接口响应中找不到关键字%s' % relevance_key)
            # print('替换后参数是', param_dict)
            return json.dumps(param_dict)
        else:
            log.info('关联接口响应为空！')
            return parameter

    def read_relevance_data(self, case_name):

        '''
        读取关联case请求参数
        :param case_name: str 被依赖case名称
        :return:关联测试用例
        '''

        response = {}

        for i in self.full_dict:
            if i['CaseName'] == case_name:
                case_data = i

                result = self.send_requests(case_data)
                response = result[1]
                break
        if isinstance(response, dict):
            log.info('关联接口返回结果%s' % response)
            return response
        else:
            log.info('关联接口未返回dict响应')
            return None


if __name__ == '__main__':
    address = setupMain.PATH + '/data/allocation/allocation_data.xlsx'
    # data={'CaseId': 8.0, 'CaseName': 'create_transfer-out-bills', 'APIName': '新增调拨出库单', 'Headers': "{'Content-Type':'application/json','charset': 'UTF-8'}", 'Path': '/occ-stock/stock/transfer-out-bills', 'Method': 'post', 'ParameterType': 'json', 'Params': '{"id":null,"stockOrgId":"abd7cf79-511d-4307-9bbd-d288b18d0ef9","stockOrgCode":"1210","stockOrgName":"西安喜马拉雅网络科技有限公司","billCode":null,"billDate":1588953600000,"billType":"AllocationOut","billTranTypeId":"AllocationOut","billTranTypeCode":null,"billTranTypeName":null,"storageId":"1001ZZ100000000DPAP4","storageCode":"test030201","storageName":"测试仓库030201","ifSlotManage":null,"storekeeperId":null,"storekeeperCode":null,"storekeeperName":null,"planSendDate":"","planArriveDate":"","currencyId":null,"currencyCode":null,"currencyName":null,"totalShouldOutNum":"5.00","totalFactOutNum":"5.00","billStatusId":null,"billStatusName":"自由","billStatusCode":"01","stockBillBelong":"0DKeeV9TPwv3UZiad8EH","customerId":null,"customerCode":null,"customerName":null,"bizPersonId":"0mWG6nOSCxjsi1zoKEYs","bizPersonCode":"007","bizPersonName":"师孟奇","deparmentId":"ae96b9ed-82dc-4aa7-bf97-cdd18a18c1a9","deparmentCode":"01010102","deparmentName":"城市经理","logisticsId":null,"logisticsCode":null,"logisticsName":null,"siger":null,"signTime":"","cancelReason":null,"remark":"自动化测试新增调拨出库单","realLogisticsCompanyId":null,"realLogisticsCompanyCode":null,"realLogisticsCompanyName":null,"logisticsBillCode":null,"inStorageId":"1001ZZ100000000DPAP6","inStorageCode":"test030202","inStorageName":"test030202","dr":0,"ts":null,"creator":null,"creationTime":null,"modifier":null,"modifiedTime":null,"persistStatus":"upd","promptMessage":null,"stockOrgInId":"abd7cf79-511d-4307-9bbd-d288b18d0ef9","stockOrgInCode":"1210","stockOrgInName":"西安喜马拉雅网络科技有限公司","inIfSlotManage":null,"transferBillOutItems":[{"transferOutBill":null,"rowNum":10,"goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","goodsCode":"301020000049","goodsName":"小雅AI音箱旗舰版_石墨绿","goodsFullName":null,"goodsBasicUnitName":null,"goodsAssistUnitName":null,"goodsConversionRate":null,"unitId":"UNIT-12","unitCode":"EA","unitName":"个","totalShouldOutNum":null,"factOutNum":"5.000000","unitPrice":"","amountMoney":"0.00","batchNumId":null,"batchNumCode":null,"batchNumName":null,"goodsPositionId":null,"goodsPositionCode":null,"goodsPositionName":null,"stockOutPersonId":null,"stockOutPersonCode":null,"stockOutPersonName":null,"stockOutDate":"","receiverAddress":null,"provinceId":null,"provinceCode":null,"provinceName":null,"cityId":null,"cityCode":null,"cityName":null,"countyId":null,"countyCode":null,"countyName":null,"townId":null,"townCode":null,"townName":null,"detailAddr":null,"receiver":null,"receiverPhone":null,"receiverPhoneSpare":null,"firstBillCode":"DBO20200508000034","firstBillBcode":"0Tr6HVsgvmzwBQYy2d6i","firstBillType":"Allocation","srcBillCode":"DBO20200508000034","srcBillBcode":"0Tr6HVsgvmzwBQYy2d6i","srcBillType":"Allocation","remark":null,"goodsVersion":"1","batchCodeId":null,"batchCodeCode":null,"batchCodeName":null,"supplierId":null,"supplierName":null,"supplierCode":null,"projectId":null,"projectCode":null,"projectName":null,"stockStateId":null,"stockStateCode":null,"stockStateName":null,"customerId":null,"customerCode":null,"customerName":null,"originalGoodsId":null,"goodsSelection":null,"goodsSelectionDescription":null,"id":null,"dr":0,"ts":null,"creator":null,"creationTime":null,"modifier":null,"modifiedTime":null,"persistStatus":"new","promptMessage":null,"transferOutBillId":null,"goodsDisplayName":null,"enableBatchNumberManage":null,"productId":null,"productCode":null,"productLineId":null,"isOptional":null,"shouldOutNum":5,"isMotherPiece":null,"enableBatchNoManage":null,"enableInvStatusManage":null,"ext01":null,"ext02":null,"ext03":"Allocation","ext04":"Allocation","ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null,"outStorageId":null,"outStorageCode":null,"outStorageName":null,"outIfSlotManage":null,"inStorageId":null,"inStorageCode":null,"inStorageName":null,"inIfSlotManage":null}],"transferOutBillItemBoms":[{"transferOutBill":null,"rowNum":"10","goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","goodsCode":"301020000049","goodsName":"小雅AI音箱旗舰版_石墨绿","goodsFullName":null,"goodsBasicUnitName":null,"goodsAssistUnitName":null,"goodsConversionRate":null,"unitId":"UNIT-12","unitCode":"EA","unitName":"个","totalShouldOutNum":null,"factOutNum":"5.000000","unitPrice":"","amountMoney":"0.00","batchNumId":null,"batchNumCode":null,"batchNumName":null,"goodsPositionId":null,"goodsPositionCode":null,"goodsPositionName":null,"stockOutPersonId":null,"stockOutPersonCode":null,"stockOutPersonName":null,"stockOutDate":"","receiverAddress":null,"provinceId":null,"provinceCode":null,"provinceName":null,"cityId":null,"cityCode":null,"cityName":null,"countyId":null,"countyCode":null,"countyName":null,"townId":null,"townCode":null,"townName":null,"detailAddr":null,"receiver":null,"receiverPhone":null,"receiverPhoneSpare":null,"firstBillCode":"0DKeeV9TPwv3UZiad8EH","firstBillBcode":"0Tr6HVsgvmzwBQYy2d6i","firstBillType":"Allocation","srcBillCode":"DBO20200508000034","srcBillBcode":"0Tr6HVsgvmzwBQYy2d6i","srcBillType":"Allocation","remark":null,"goodsVersion":"1","goodsSelection":null,"goodsNum":null,"parentGoodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","parentGoodsCode":"301020000049","parentGoodsName":"小雅AI音箱旗舰版_石墨绿","parentRowNum":"10","childGoodsQty":null,"batchCodeId":null,"batchCodeCode":null,"batchCodeName":null,"supplierId":null,"supplierName":null,"supplierCode":null,"projectId":null,"projectCode":null,"projectName":null,"stockStateId":null,"stockStateCode":null,"stockStateName":null,"customerId":null,"customerCode":null,"customerName":null,"originalGoodsId":null,"goodsSelectionDescription":null,"id":null,"dr":0,"ts":null,"creator":null,"creationTime":null,"modifier":null,"modifiedTime":null,"persistStatus":"new","promptMessage":null,"goodsDisplayName":null,"enableBatchNumberManage":null,"productId":null,"productLineId":null,"shouldOutNum":5,"itemId":null,"billId":null,"parentGoodsdisplayName":null,"firstBillBomCode":"0CrhvlIZ5uIVEXmYN9Hq","srcBillBomCode":"0CrhvlIZ5uIVEXmYN9Hq","ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null}],"srcSystem":null,"srcSystemId":null,"srcSystemCode":null,"srcSystemName":null,"ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null,"sycnOutStatus":null,"sycnNCStatus":null}', 'CheckTpye': 'check_json', 'ExpectedCode': 200.0, 'ExpectedData': '{"id":"0TszFCIVqcbJkmpWHQhq","dr":0,"ts":1589002318000,"creator":"smq","creationTime":1589002318000,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":"","stockOrgId":"abd7cf79-511d-4307-9bbd-d288b18d0ef9","stockOrgCode":"1210","stockOrgName":"西安喜马拉雅网络科技有限公司","stockOrgInId":"abd7cf79-511d-4307-9bbd-d288b18d0ef9","stockOrgInCode":"1210","stockOrgInName":"西安喜马拉雅网络科技有限公司","billCode":"TDN2020050900003","billDate":1588953600000,"billType":"AllocationOut","billTranTypeId":"AllocationOut","billTranTypeCode":"AllocationOut","billTranTypeName":"调拨出库","storageId":"1001ZZ100000000DPAP4","storageCode":"test030201","storageName":"测试仓库030201","ifSlotManage":null,"inStorageId":"1001ZZ100000000DPAP6","inStorageCode":"test030202","inStorageName":"test030202","inIfSlotManage":null,"storekeeperId":null,"storekeeperCode":null,"storekeeperName":null,"planSendDate":null,"planArriveDate":null,"currencyId":null,"currencyCode":null,"currencyName":null,"totalShouldOutNum":5.00000000,"totalFactOutNum":5.00000000,"billStatusId":"099aj5df-4y42-4700-d8d6-3714fdb43e68","billStatusCode":"01","billStatusName":"自由","stockBillBelong":"0DKeeV9TPwv3UZiad8EH","customerId":null,"customerCode":null,"customerName":null,"bizPersonId":"0mWG6nOSCxjsi1zoKEYs","bizPersonCode":"007","bizPersonName":"师孟奇","deparmentId":"ae96b9ed-82dc-4aa7-bf97-cdd18a18c1a9","deparmentCode":"01010102","deparmentName":"城市经理","logisticsId":null,"logisticsCode":null,"logisticsName":null,"realLogisticsCompanyId":null,"realLogisticsCompanyCode":null,"realLogisticsCompanyName":null,"logisticsBillCode":null,"siger":null,"signTime":null,"cancelReason":null,"remark":"自动化测试新增调拨出库单","transferBillOutItems":[{"id":"0RVbhbtQZhT5PZkp19zW","dr":0,"ts":1589002336000,"creator":"smq","creationTime":1589002336000,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":null,"transferOutBillId":"0TszFCIVqcbJkmpWHQhq","rowNum":10,"goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","goodsCode":"301020000049","goodsName":"小雅AI音箱旗舰版_石墨绿","goodsDisplayName":"小雅AI音箱旗舰版_石墨绿","goodsBasicUnitName":"个","goodsAssistUnitName":"个","goodsConversionRate":1.000000,"enableBatchNumberManage":null,"productId":null,"productCode":null,"productLineId":null,"isOptional":null,"unitId":"UNIT-12","unitCode":"EA","unitName":"个","shouldOutNum":5.00000000,"factOutNum":5.00000000,"unitPrice":null,"amountMoney":0E-8,"batchNumId":null,"batchNumCode":null,"batchNumName":null,"goodsPositionId":null,"goodsPositionCode":null,"goodsPositionName":null,"stockOutPersonId":null,"stockOutPersonCode":null,"stockOutPersonName":null,"stockOutDate":null,"receiverAddress":null,"provinceId":null,"provinceCode":null,"provinceName":null,"cityId":null,"cityCode":null,"cityName":null,"countyId":null,"countyCode":null,"countyName":null,"townId":null,"townCode":null,"townName":null,"detailAddr":null,"receiver":null,"receiverPhone":null,"receiverPhoneSpare":null,"firstBillCode":"DBO20200508000034","firstBillBcode":"0Tr6HVsgvmzwBQYy2d6i","firstBillType":"Allocation","srcBillCode":"DBO20200508000034","srcBillBcode":"0Tr6HVsgvmzwBQYy2d6i","srcBillType":"Allocation","remark":null,"goodsVersion":"1","goodsSelection":null,"isMotherPiece":null,"customerId":null,"customerCode":null,"customerName":null,"supplierId":null,"supplierCode":null,"supplierName":null,"projectId":null,"projectCode":null,"projectName":null,"batchCodeId":null,"batchCodeCode":null,"stockStateId":null,"stockStateCode":null,"stockStateName":null,"enableBatchNoManage":null,"enableInvStatusManage":null,"originalGoodsId":null,"goodsSelectionDescription":null,"ext01":null,"ext02":null,"ext03":"Allocation","ext04":"Allocation","ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null,"outStorageId":null,"outStorageCode":null,"outStorageName":null,"outIfSlotManage":null,"inStorageId":null,"inStorageCode":null,"inStorageName":null,"inIfSlotManage":null}],"transferOutBillItemBoms":[{"id":"0K1xchlRSFmYGxaooi2J","dr":0,"ts":1589002336000,"creator":"smq","creationTime":1589002336000,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":null,"rowNum":"10","goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","goodsCode":"301020000049","goodsName":"小雅AI音箱旗舰版_石墨绿","goodsDisplayName":"小雅AI音箱旗舰版_石墨绿","goodsBasicUnitName":"个","goodsAssistUnitName":"个","goodsConversionRate":1.000000,"enableBatchNumberManage":null,"productId":null,"productLineId":null,"unitId":"UNIT-12","unitCode":"EA","unitName":"个","shouldOutNum":5.00000000,"factOutNum":5.00000000,"unitPrice":null,"amountMoney":0E-8,"batchNumId":null,"batchNumCode":null,"batchNumName":null,"goodsPositionId":null,"goodsPositionCode":null,"goodsPositionName":null,"stockOutPersonId":null,"stockOutPersonCode":null,"stockOutPersonName":null,"stockOutDate":null,"receiverAddress":null,"provinceId":null,"provinceCode":null,"provinceName":null,"cityId":null,"cityCode":null,"cityName":null,"countyId":null,"countyCode":null,"countyName":null,"townId":null,"townCode":null,"townName":null,"detailAddr":null,"receiver":null,"receiverPhone":null,"receiverPhoneSpare":null,"firstBillCode":"0DKeeV9TPwv3UZiad8EH","firstBillBcode":"0Tr6HVsgvmzwBQYy2d6i","firstBillType":"Allocation","srcBillCode":"DBO20200508000034","srcBillBcode":"0Tr6HVsgvmzwBQYy2d6i","srcBillType":"Allocation","remark":null,"goodsVersion":"1","goodsSelection":null,"customerId":null,"customerCode":null,"customerName":null,"supplierId":null,"supplierCode":null,"supplierName":null,"projectId":null,"projectCode":null,"projectName":null,"batchCodeId":null,"batchCodeCode":null,"stockStateId":null,"stockStateCode":null,"stockStateName":null,"originalGoodsId":null,"goodsSelectionDescription":null,"itemId":"0RVbhbtQZhT5PZkp19zW","billId":null,"parentGoodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","parentGoodsCode":"301020000049","parentGoodsName":"小雅AI音箱旗舰版_石墨绿","parentGoodsdisplayName":null,"parentRowNum":"10","childGoodsQty":null,"firstBillBomCode":"0CrhvlIZ5uIVEXmYN9Hq","srcBillBomCode":"0CrhvlIZ5uIVEXmYN9Hq","ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null}],"srcSystem":null,"srcSystemId":null,"srcSystemCode":null,"srcSystemName":null,"ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null,"sycnOutStatus":null,"sycnNCStatus":null}', 'User': 'Manager', 'DependCase': 'approve_allocation_bill', 'RelevanceList': '', 'Sql': '', 'IsDepend': 'Yes'}
    #
    full_dict = ReadExcel(address).get_full_dict()
    h = HttpClient(full_dict)
    # h.send_requests(data)
    depend_Case='create_allocation_bill'
    relevance="{'billId':'id'}"
    parameter='{"billId": "allocation-create1"}'
    h.init_request(depend_Case,relevance,parameter)
