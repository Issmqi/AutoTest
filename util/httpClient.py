# -*- coding: utf-8 -*-
# !/bin/bash

import allure
import requests
import json
from jsonpath import jsonpath
import simplejson
import setupMain
from business import initializeCookie
from util.log import Log
from util.readExcel import ReadExcel
from util.readConfig import ReadConfig

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
        case_id = request_data['CaseId']
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
        log.info('用例id:%s' % case_id)
        log.info('用例名称:%s' % case_name)
        log.info('请求头:%s' % header)
        log.info('请求地址:%s' % url)
        log.info('请求参数:%s' % parameter)
        log.info('测试用户：%s' % user)


        with allure.step("开始请求接口"):
            allure.attach(method, "请求类型")
            allure.attach(case_name, "用例名称:")
            allure.attach(url, "请求地址:")
            allure.attach(str(header), "请求头")
            allure.attach(parameter_type, "请求参数类型")
            allure.attach(str(parameter), "请求参数")

        result = self.api_method(method, url, parameter, cookie, header, parameter_type)
        log.info("返回状态码:%s" % str(result[0]))
        log.info("返回response:\n %s" % result[1])
        return result

    def api_method(self, method, url, param, cookie, header=None, param_type=None):
        '''

        :param method: 请求类型 str post/put/get
        :param url: 请求路径 str
        :param param: 请求参数 str
        :param cookie:
        :param header:
        :param param_type: 请求参数类型 str json/form_data/parameter
        :return:
        '''
        # if header:
        #     header = header
        if not param:
            param_dict = None
        else:
            param_dict = param
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

    def init_request(self, dependCase, relevance, param_dict):
        '''
        请求前执行依赖接口，处理依赖参数
        :param dependCase:dict 关联接口casename
        :param relevance:dict 关联键值对
        :param param_dict: dict 接口请求参数
        :return: parameter: str
        '''
        relevance_response = self.read_relevance_data(dependCase)  # 执行依赖接口
        if not relevance_response:
            return param_dict
        if not relevance:
            return param_dict

        else:
            for param_key in relevance:
                relevance_key = relevance[param_key]  # 依赖关键字jsonpath
                try:
                    relevance_value = jsonpath(relevance_response, '%s' % relevance_key)[0]  # 依赖关键字的值
                    # param_dict[param_key] = jsonpath(relevance_response, '%s' % relevance_key)[0]  # 将依赖response中依赖关键字对应的值复制给请求参数的关键字
                    # log.info('替换后关键字%s是:%s' % (param_key, param_dict[param_key]))
                    self.update_json_value(param_dict, param_key, relevance_value)
                except Exception as e:
                    log.info('关联接口响应中找不到关键字%s' % relevance_key)
                    log.error(e)

            log.info('替换后参数是:%s' % param_dict)
            return param_dict

    def update_json_value(self, dic_json, k, v):
        '''
        将多层级dict中关键字k的值全部替换为v
        :param dic_json:
        :param k:
        :param v:
        :return:
        '''
        for key in dic_json:
            this_key = key
            this_value = dic_json[this_key]
            if isinstance(this_value, dict):
                self.update_json_value(this_value, k, v)
            if isinstance(this_value, list):
                for child in this_value:
                    if isinstance(child, dict):
                        self.update_json_value(child, k, v)
            else:
                if this_key == k:
                    dic_json[this_key] = v
        return dic_json

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
    with open(setupMain.PATH + '/data/allocation/allocation_order_case.json', 'r', encoding='utf-8') as f:
        full_dict = json.load(f)
    # address = setupMain.PATH + '/data/allocation/allocation_data.xlsx'
    # full_dict = ReadExcel(address).get_full_dict()
    h = HttpClient(full_dict)
    data={'CaseId': 8, 'CaseName': 'create_transfer-out-bills', 'APIName': '新增调拨出库单', 'Headers': {'Content-Type': 'application/json', 'charset': 'UTF-8'}, 'Path': '/occ-stock/stock/transfer-out-bills', 'Method': 'post', 'ParameterType': 'json', 'Params': {'id': None, 'stockOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9', 'stockOrgCode': '1210', 'stockOrgName': '西安喜马拉雅网络科技有限公司', 'billCode': None, 'billDate': 1589212800000, 'billType': 'AllocationOut', 'billTranTypeId': 'AllocationOut', 'billTranTypeCode': None, 'billTranTypeName': None, 'storageId': '1001ZZ100000000DPAP4', 'storageCode': 'test030201', 'storageName': '测试仓库030201', 'ifSlotManage': None, 'storekeeperId': None, 'storekeeperCode': None, 'storekeeperName': None, 'planSendDate': '', 'planArriveDate': '', 'currencyId': None, 'currencyCode': None, 'currencyName': None, 'totalShouldOutNum': '25.00', 'totalFactOutNum': '20.00', 'billStatusId': None, 'billStatusName': '自由', 'billStatusCode': '01', 'stockBillBelong': '0kxUvN0mm3QI7AhjYqSM', 'customerId': None, 'customerCode': None, 'customerName': None, 'bizPersonId': None, 'bizPersonCode': None, 'bizPersonName': None, 'deparmentId': '0K1ovYvAl1Pk00oCRPjV', 'deparmentCode': '01010102', 'deparmentName': '城市经理', 'logisticsId': None, 'logisticsCode': None, 'logisticsName': None, 'siger': None, 'signTime': '', 'cancelReason': None, 'remark': '自动化测试参照调拨单新增调拨出库单', 'realLogisticsCompanyId': None, 'realLogisticsCompanyCode': None, 'realLogisticsCompanyName': None, 'logisticsBillCode': None, 'inStorageId': '1001ZZ100000000DPAP6', 'inStorageCode': 'test030202', 'inStorageName': 'test030202', 'dr': 0, 'ts': None, 'creator': None, 'creationTime': None, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'upd', 'promptMessage': None, 'stockOrgInId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9', 'stockOrgInCode': '1210', 'stockOrgInName': '西安喜马拉雅网络科技有限公司', 'inIfSlotManage': None, 'transferBillOutItems': [{'transferOutBill': None, 'rowNum': 10, 'goodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'goodsCode': '301020000049', 'goodsName': '小雅AI音箱旗舰版_石墨绿', 'goodsFullName': None, 'goodsBasicUnitName': None, 'goodsAssistUnitName': None, 'goodsConversionRate': None, 'unitId': 'UNIT-12', 'unitCode': 'EA', 'unitName': '个', 'totalShouldOutNum': None, 'factOutNum': '20.000000', 'unitPrice': '', 'amountMoney': '0.00', 'batchNumId': None, 'batchNumCode': None, 'batchNumName': None, 'goodsPositionId': None, 'goodsPositionCode': None, 'goodsPositionName': None, 'stockOutPersonId': None, 'stockOutPersonCode': None, 'stockOutPersonName': None, 'stockOutDate': '', 'receiverAddress': None, 'provinceId': None, 'provinceCode': None, 'provinceName': None, 'cityId': None, 'cityCode': None, 'cityName': None, 'countyId': None, 'countyCode': None, 'countyName': None, 'townId': None, 'townCode': None, 'townName': None, 'detailAddr': None, 'receiver': None, 'receiverPhone': None, 'receiverPhoneSpare': None, 'firstBillCode': 'DBO20200512000019', 'firstBillBcode': '0Wfar8LVlCZOkFv2gos9', 'firstBillType': 'Allocation', 'srcBillCode': 'DBO20200512000019', 'srcBillBcode': '0Wfar8LVlCZOkFv2gos9', 'srcBillType': 'Allocation', 'remark': None, 'goodsVersion': '1', 'batchCodeId': None, 'batchCodeCode': None, 'batchCodeName': None, 'supplierId': None, 'supplierName': None, 'supplierCode': None, 'projectId': None, 'projectCode': None, 'projectName': None, 'stockStateId': None, 'stockStateCode': None, 'stockStateName': None, 'customerId': None, 'customerCode': None, 'customerName': None, 'originalGoodsId': None, 'goodsSelection': None, 'goodsSelectionDescription': None, 'id': None, 'dr': 0, 'ts': None, 'creator': None, 'creationTime': None, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'new', 'promptMessage': None, 'transferOutBillId': None, 'goodsDisplayName': None, 'enableBatchNumberManage': None, 'productId': None, 'productCode': None, 'productLineId': None, 'isOptional': None, 'shouldOutNum': 25, 'isMotherPiece': None, 'enableBatchNoManage': None, 'enableInvStatusManage': None, 'ext01': None, 'ext02': None, 'ext03': 'Allocation', 'ext04': 'Allocation', 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None, 'outStorageId': None, 'outStorageCode': None, 'outStorageName': None, 'outIfSlotManage': None, 'inStorageId': None, 'inStorageCode': None, 'inStorageName': None, 'inIfSlotManage': None}], 'transferOutBillItemBoms': [{'transferOutBill': None, 'rowNum': '10', 'goodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'goodsCode': '301020000049', 'goodsName': '小雅AI音箱旗舰版_石墨绿', 'goodsFullName': None, 'goodsBasicUnitName': None, 'goodsAssistUnitName': None, 'goodsConversionRate': None, 'unitId': 'UNIT-12', 'unitCode': 'EA', 'unitName': '个', 'totalShouldOutNum': None, 'factOutNum': 20, 'unitPrice': '', 'amountMoney': '0.00', 'batchNumId': None, 'batchNumCode': None, 'batchNumName': None, 'goodsPositionId': None, 'goodsPositionCode': None, 'goodsPositionName': None, 'stockOutPersonId': None, 'stockOutPersonCode': None, 'stockOutPersonName': None, 'stockOutDate': '', 'receiverAddress': None, 'provinceId': None, 'provinceCode': None, 'provinceName': None, 'cityId': None, 'cityCode': None, 'cityName': None, 'countyId': None, 'countyCode': None, 'countyName': None, 'townId': None, 'townCode': None, 'townName': None, 'detailAddr': None, 'receiver': None, 'receiverPhone': None, 'receiverPhoneSpare': None, 'firstBillCode': '0kxUvN0mm3QI7AhjYqSM', 'firstBillBcode': '0Wfar8LVlCZOkFv2gos9', 'firstBillType': 'Allocation', 'srcBillCode': 'DBO20200512000019', 'srcBillBcode': '0Wfar8LVlCZOkFv2gos9', 'srcBillType': 'Allocation', 'remark': None, 'goodsVersion': '1', 'goodsSelection': None, 'goodsNum': None, 'parentGoodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'parentGoodsCode': '301020000049', 'parentGoodsName': '小雅AI音箱旗舰版_石墨绿', 'parentRowNum': '10', 'childGoodsQty': None, 'batchCodeId': None, 'batchCodeCode': None, 'batchCodeName': None, 'supplierId': None, 'supplierName': None, 'supplierCode': None, 'projectId': None, 'projectCode': None, 'projectName': None, 'stockStateId': None, 'stockStateCode': None, 'stockStateName': None, 'customerId': None, 'customerCode': None, 'customerName': None, 'originalGoodsId': None, 'goodsSelectionDescription': None, 'id': None, 'dr': 0, 'ts': None, 'creator': None, 'creationTime': None, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'new', 'promptMessage': None, 'goodsDisplayName': None, 'enableBatchNumberManage': None, 'productId': None, 'productLineId': None, 'shouldOutNum': 25, 'itemId': None, 'billId': None, 'parentGoodsdisplayName': None, 'firstBillBomCode': '0rYlYTDrAqKnyukQYYWh', 'srcBillBomCode': '0rYlYTDrAqKnyukQYYWh', 'ext01': None, 'ext02': None, 'ext03': None, 'ext04': None, 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None}], 'srcSystem': None, 'srcSystemId': None, 'srcSystemCode': None, 'srcSystemName': None, 'ext01': None, 'ext02': None, 'ext03': None, 'ext04': None, 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None, 'sycnOutStatus': None, 'sycnNCStatus': None}, 'CheckType': 'check_json', 'ExpectedCode': 200, 'ExpectedData': {'id': '0QzEVVCjk0XWHmc8XW1e', 'dr': 0, 'ts': 1589274143000, 'creator': 'smq', 'creationTime': 1589274143000, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm', 'promptMessage': '', 'stockOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9', 'stockOrgCode': '1210', 'stockOrgName': '西安喜马拉雅网络科技有限公司', 'stockOrgInId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9', 'stockOrgInCode': '1210', 'stockOrgInName': '西安喜马拉雅网络科技有限公司', 'billCode': 'TDN2020051200009', 'billDate': 1589212800000, 'billType': 'AllocationOut', 'billTranTypeId': 'AllocationOut', 'billTranTypeCode': 'AllocationOut', 'billTranTypeName': '调拨出库', 'storageId': '1001ZZ100000000DPAP4', 'storageCode': 'test030201', 'storageName': '测试仓库030201', 'ifSlotManage': None, 'inStorageId': '1001ZZ100000000DPAP6', 'inStorageCode': 'test030202', 'inStorageName': 'test030202', 'inIfSlotManage': None, 'storekeeperId': None, 'storekeeperCode': None, 'storekeeperName': None, 'planSendDate': None, 'planArriveDate': None, 'currencyId': None, 'currencyCode': None, 'currencyName': None, 'totalShouldOutNum': 25.0, 'totalFactOutNum': 20.0, 'billStatusId': '099aj5df-4y42-4700-d8d6-3714fdb43e68', 'billStatusCode': '01', 'billStatusName': '自由', 'stockBillBelong': '0kxUvN0mm3QI7AhjYqSM', 'customerId': None, 'customerCode': None, 'customerName': None, 'bizPersonId': None, 'bizPersonCode': None, 'bizPersonName': None, 'deparmentId': '0K1ovYvAl1Pk00oCRPjV', 'deparmentCode': '01010102', 'deparmentName': '城市经理', 'logisticsId': None, 'logisticsCode': None, 'logisticsName': None, 'realLogisticsCompanyId': None, 'realLogisticsCompanyCode': None, 'realLogisticsCompanyName': None, 'logisticsBillCode': None, 'siger': None, 'signTime': None, 'cancelReason': None, 'remark': '自动化测试参照调拨单新增调拨出库单', 'transferBillOutItems': [{'id': '0P8IrZN6W1PNnqna2SLI', 'dr': 0, 'ts': 1589274152000, 'creator': 'smq', 'creationTime': 1589274152000, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm', 'promptMessage': None, 'transferOutBillId': '0QzEVVCjk0XWHmc8XW1e', 'rowNum': 10, 'goodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'goodsCode': '301020000049', 'goodsName': '小雅AI音箱旗舰版_石墨绿', 'goodsDisplayName': '小雅AI音箱旗舰版_石墨绿', 'goodsBasicUnitName': '个', 'goodsAssistUnitName': '个', 'goodsConversionRate': 1.0, 'enableBatchNumberManage': None, 'productId': None, 'productCode': None, 'productLineId': None, 'isOptional': None, 'unitId': 'UNIT-12', 'unitCode': 'EA', 'unitName': '个', 'shouldOutNum': 25.0, 'factOutNum': 20.0, 'unitPrice': None, 'amountMoney': 0.0, 'batchNumId': None, 'batchNumCode': None, 'batchNumName': None, 'goodsPositionId': None, 'goodsPositionCode': None, 'goodsPositionName': None, 'stockOutPersonId': None, 'stockOutPersonCode': None, 'stockOutPersonName': None, 'stockOutDate': None, 'receiverAddress': None, 'provinceId': None, 'provinceCode': None, 'provinceName': None, 'cityId': None, 'cityCode': None, 'cityName': None, 'countyId': None, 'countyCode': None, 'countyName': None, 'townId': None, 'townCode': None, 'townName': None, 'detailAddr': None, 'receiver': None, 'receiverPhone': None, 'receiverPhoneSpare': None, 'firstBillCode': 'DBO20200512000019', 'firstBillBcode': '0Wfar8LVlCZOkFv2gos9', 'firstBillType': 'Allocation', 'srcBillCode': 'DBO20200512000019', 'srcBillBcode': '0Wfar8LVlCZOkFv2gos9', 'srcBillType': 'Allocation', 'remark': None, 'goodsVersion': '1', 'goodsSelection': None, 'isMotherPiece': None, 'customerId': None, 'customerCode': None, 'customerName': None, 'supplierId': None, 'supplierCode': None, 'supplierName': None, 'projectId': None, 'projectCode': None, 'projectName': None, 'batchCodeId': None, 'batchCodeCode': None, 'stockStateId': None, 'stockStateCode': None, 'stockStateName': None, 'enableBatchNoManage': None, 'enableInvStatusManage': None, 'originalGoodsId': None, 'goodsSelectionDescription': None, 'ext01': None, 'ext02': None, 'ext03': 'Allocation', 'ext04': 'Allocation', 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None, 'outStorageId': None, 'outStorageCode': None, 'outStorageName': None, 'outIfSlotManage': None, 'inStorageId': None, 'inStorageCode': None, 'inStorageName': None, 'inIfSlotManage': None}], 'transferOutBillItemBoms': [{'id': '0Il4I5YzeSjivhdsEfOx', 'dr': 0, 'ts': 1589274152000, 'creator': 'smq', 'creationTime': 1589274152000, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm', 'promptMessage': None, 'rowNum': '10', 'goodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'goodsCode': '301020000049', 'goodsName': '小雅AI音箱旗舰版_石墨绿', 'goodsDisplayName': '小雅AI音箱旗舰版_石墨绿', 'goodsBasicUnitName': '个', 'goodsAssistUnitName': '个', 'goodsConversionRate': 1.0, 'enableBatchNumberManage': None, 'productId': None, 'productLineId': None, 'unitId': 'UNIT-12', 'unitCode': 'EA', 'unitName': '个', 'shouldOutNum': 25.0, 'factOutNum': 20.0, 'unitPrice': None, 'amountMoney': 0.0, 'batchNumId': None, 'batchNumCode': None, 'batchNumName': None, 'goodsPositionId': None, 'goodsPositionCode': None, 'goodsPositionName': None, 'stockOutPersonId': None, 'stockOutPersonCode': None, 'stockOutPersonName': None, 'stockOutDate': None, 'receiverAddress': None, 'provinceId': None, 'provinceCode': None, 'provinceName': None, 'cityId': None, 'cityCode': None, 'cityName': None, 'countyId': None, 'countyCode': None, 'countyName': None, 'townId': None, 'townCode': None, 'townName': None, 'detailAddr': None, 'receiver': None, 'receiverPhone': None, 'receiverPhoneSpare': None, 'firstBillCode': '0kxUvN0mm3QI7AhjYqSM', 'firstBillBcode': '0Wfar8LVlCZOkFv2gos9', 'firstBillType': 'Allocation', 'srcBillCode': 'DBO20200512000019', 'srcBillBcode': '0Wfar8LVlCZOkFv2gos9', 'srcBillType': 'Allocation', 'remark': None, 'goodsVersion': '1', 'goodsSelection': None, 'customerId': None, 'customerCode': None, 'customerName': None, 'supplierId': None, 'supplierCode': None, 'supplierName': None, 'projectId': None, 'projectCode': None, 'projectName': None, 'batchCodeId': None, 'batchCodeCode': None, 'stockStateId': None, 'stockStateCode': None, 'stockStateName': None, 'originalGoodsId': None, 'goodsSelectionDescription': None, 'itemId': '0P8IrZN6W1PNnqna2SLI', 'billId': None, 'parentGoodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'parentGoodsCode': '301020000049', 'parentGoodsName': '小雅AI音箱旗舰版_石墨绿', 'parentGoodsdisplayName': None, 'parentRowNum': '10', 'childGoodsQty': None, 'firstBillBomCode': '0rYlYTDrAqKnyukQYYWh', 'srcBillBomCode': '0rYlYTDrAqKnyukQYYWh', 'ext01': None, 'ext02': None, 'ext03': None, 'ext04': None, 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None}], 'srcSystem': None, 'srcSystemId': None, 'srcSystemCode': None, 'srcSystemName': None, 'ext01': None, 'ext02': None, 'ext03': None, 'ext04': None, 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None, 'sycnOutStatus': None, 'sycnNCStatus': None}, 'User': 'Manager', 'DependCase': 'approve_allocation_bill', 'RelevanceList': {'stockBillBelong': '$..billId', 'firstBillCode': '$..billId', 'firstBillBcode': '$..itemId', 'srcBillCode': '$..code', 'firstBillBomCode': '$.detailMsg.data[0].transferBillItemBoms[0].id', 'srcBillBomCode': '$.detailMsg.data[0].transferBillItemBoms[0].id'}}

    h.send_requests(data)
    # depend_Case='approve_allocation_bill'
    # relevance='{"stockBillBelong":"$..billId","firstBillCode":"$..billId","firstBillBcode":"$..itemId","srcBillCode":"$..code","firstBillBomCode":"$.detailMsg.data[0].transferBillItemBoms[0].id","srcBillBomCode":"$.detailMsg.data[0].transferBillItemBoms[0].id"}'
    # parameter='{"id": null, "stockOrgId": "abd7cf79-511d-4307-9bbd-d288b18d0ef9", "stockOrgCode": "1210", "stockOrgName": "\u897f\u5b89\u559c\u9a6c\u62c9\u96c5\u7f51\u7edc\u79d1\u6280\u6709\u9650\u516c\u53f8", "billCode": null, "billDate": 1589212800000, "billType": "AllocationOut", "billTranTypeId": "AllocationOut", "billTranTypeCode": null, "billTranTypeName": null, "storageId": "1001ZZ100000000DPAP4", "storageCode": "test030201", "storageName": "\u6d4b\u8bd5\u4ed3\u5e93030201", "ifSlotManage": null, "storekeeperId": null, "storekeeperCode": null, "storekeeperName": null, "planSendDate": "", "planArriveDate": "", "currencyId": null, "currencyCode": null, "currencyName": null, "totalShouldOutNum": "25.00", "totalFactOutNum": "20.00", "billStatusId": null, "billStatusName": "\u81ea\u7531", "billStatusCode": "01", "stockBillBelong": "0yCVoxXanglmpVJ1sFkr", "customerId": null, "customerCode": null, "customerName": null, "bizPersonId": null, "bizPersonCode": null, "bizPersonName": null, "deparmentId": "0K1ovYvAl1Pk00oCRPjV", "deparmentCode": "01010102", "deparmentName": "\u57ce\u5e02\u7ecf\u7406", "logisticsId": null, "logisticsCode": null, "logisticsName": null, "siger": null, "signTime": "", "cancelReason": null, "remark": "\u81ea\u52a8\u5316\u6d4b\u8bd5\u53c2\u7167\u8c03\u62e8\u5355\u65b0\u589e\u8c03\u62e8\u51fa\u5e93\u5355", "realLogisticsCompanyId": null, "realLogisticsCompanyCode": null, "realLogisticsCompanyName": null, "logisticsBillCode": null, "inStorageId": "1001ZZ100000000DPAP6", "inStorageCode": "test030202", "inStorageName": "test030202", "dr": 0, "ts": null, "creator": null, "creationTime": null, "modifier": null, "modifiedTime": null, "persistStatus": "upd", "promptMessage": null, "stockOrgInId": "abd7cf79-511d-4307-9bbd-d288b18d0ef9", "stockOrgInCode": "1210", "stockOrgInName": "\u897f\u5b89\u559c\u9a6c\u62c9\u96c5\u7f51\u7edc\u79d1\u6280\u6709\u9650\u516c\u53f8", "inIfSlotManage": null, "transferBillOutItems": [{"transferOutBill": null, "rowNum": 10, "goodsId": "03e77ae0-469d-4d8a-ba34-733c2ada3749", "goodsCode": "301020000049", "goodsName": "\u5c0f\u96c5AI\u97f3\u7bb1\u65d7\u8230\u7248_\u77f3\u58a8\u7eff", "goodsFullName": null, "goodsBasicUnitName": null, "goodsAssistUnitName": null, "goodsConversionRate": null, "unitId": "UNIT-12", "unitCode": "EA", "unitName": "\u4e2a", "totalShouldOutNum": null, "factOutNum": "20.000000", "unitPrice": "", "amountMoney": "0.00", "batchNumId": null, "batchNumCode": null, "batchNumName": null, "goodsPositionId": null, "goodsPositionCode": null, "goodsPositionName": null, "stockOutPersonId": null, "stockOutPersonCode": null, "stockOutPersonName": null, "stockOutDate": "", "receiverAddress": null, "provinceId": null, "provinceCode": null, "provinceName": null, "cityId": null, "cityCode": null, "cityName": null, "countyId": null, "countyCode": null, "countyName": null, "townId": null, "townCode": null, "townName": null, "detailAddr": null, "receiver": null, "receiverPhone": null, "receiverPhoneSpare": null, "firstBillCode": "DBO20200512000019", "firstBillBcode": "0Wfar8LVlCZOkFv2gos9", "firstBillType": "Allocation", "srcBillCode": "DBO20200512000019", "srcBillBcode": "0Wfar8LVlCZOkFv2gos9", "srcBillType": "Allocation", "remark": null, "goodsVersion": "1", "batchCodeId": null, "batchCodeCode": null, "batchCodeName": null, "supplierId": null, "supplierName": null, "supplierCode": null, "projectId": null, "projectCode": null, "projectName": null, "stockStateId": null, "stockStateCode": null, "stockStateName": null, "customerId": null, "customerCode": null, "customerName": null, "originalGoodsId": null, "goodsSelection": null, "goodsSelectionDescription": null, "id": null, "dr": 0, "ts": null, "creator": null, "creationTime": null, "modifier": null, "modifiedTime": null, "persistStatus": "new", "promptMessage": null, "transferOutBillId": null, "goodsDisplayName": null, "enableBatchNumberManage": null, "productId": null, "productCode": null, "productLineId": null, "isOptional": null, "shouldOutNum": 25, "isMotherPiece": null, "enableBatchNoManage": null, "enableInvStatusManage": null, "ext01": null, "ext02": null, "ext03": "Allocation", "ext04": "Allocation", "ext05": null, "ext06": null, "ext07": null, "ext08": null, "ext09": null, "ext10": null, "ext11": null, "ext12": null, "ext13": null, "ext14": null, "ext15": null, "outStorageId": null, "outStorageCode": null, "outStorageName": null, "outIfSlotManage": null, "inStorageId": null, "inStorageCode": null, "inStorageName": null, "inIfSlotManage": null}], "transferOutBillItemBoms": [{"transferOutBill": null, "rowNum": "10", "goodsId": "03e77ae0-469d-4d8a-ba34-733c2ada3749", "goodsCode": "301020000049", "goodsName": "\u5c0f\u96c5AI\u97f3\u7bb1\u65d7\u8230\u7248_\u77f3\u58a8\u7eff", "goodsFullName": null, "goodsBasicUnitName": null, "goodsAssistUnitName": null, "goodsConversionRate": null, "unitId": "UNIT-12", "unitCode": "EA", "unitName": "\u4e2a", "totalShouldOutNum": null, "factOutNum": 20, "unitPrice": "", "amountMoney": "0.00", "batchNumId": null, "batchNumCode": null, "batchNumName": null, "goodsPositionId": null, "goodsPositionCode": null, "goodsPositionName": null, "stockOutPersonId": null, "stockOutPersonCode": null, "stockOutPersonName": null, "stockOutDate": "", "receiverAddress": null, "provinceId": null, "provinceCode": null, "provinceName": null, "cityId": null, "cityCode": null, "cityName": null, "countyId": null, "countyCode": null, "countyName": null, "townId": null, "townCode": null, "townName": null, "detailAddr": null, "receiver": null, "receiverPhone": null, "receiverPhoneSpare": null, "firstBillCode": "0kxUvN0mm3QI7AhjYqSM", "firstBillBcode": "0Wfar8LVlCZOkFv2gos9", "firstBillType": "Allocation", "srcBillCode": "DBO20200512000019", "srcBillBcode": "0Wfar8LVlCZOkFv2gos9", "srcBillType": "Allocation", "remark": null, "goodsVersion": "1", "goodsSelection": null, "goodsNum": null, "parentGoodsId": "03e77ae0-469d-4d8a-ba34-733c2ada3749", "parentGoodsCode": "301020000049", "parentGoodsName": "\u5c0f\u96c5AI\u97f3\u7bb1\u65d7\u8230\u7248_\u77f3\u58a8\u7eff", "parentRowNum": "10", "childGoodsQty": null, "batchCodeId": null, "batchCodeCode": null, "batchCodeName": null, "supplierId": null, "supplierName": null, "supplierCode": null, "projectId": null, "projectCode": null, "projectName": null, "stockStateId": null, "stockStateCode": null, "stockStateName": null, "customerId": null, "customerCode": null, "customerName": null, "originalGoodsId": null, "goodsSelectionDescription": null, "id": null, "dr": 0, "ts": null, "creator": null, "creationTime": null, "modifier": null, "modifiedTime": null, "persistStatus": "new", "promptMessage": null, "goodsDisplayName": null, "enableBatchNumberManage": null, "productId": null, "productLineId": null, "shouldOutNum": 25, "itemId": null, "billId": null, "parentGoodsdisplayName": null, "firstBillBomCode": "0rYlYTDrAqKnyukQYYWh", "srcBillBomCode": "0rYlYTDrAqKnyukQYYWh", "ext01": null, "ext02": null, "ext03": null, "ext04": null, "ext05": null, "ext06": null, "ext07": null, "ext08": null, "ext09": null, "ext10": null, "ext11": null, "ext12": null, "ext13": null, "ext14": null, "ext15": null}], "srcSystem": null, "srcSystemId": null, "srcSystemCode": null, "srcSystemName": null, "ext01": null, "ext02": null, "ext03": null, "ext04": null, "ext05": null, "ext06": null, "ext07": null, "ext08": null, "ext09": null, "ext10": null, "ext11": null, "ext12": null, "ext13": null, "ext14": null, "ext15": null, "sycnOutStatus": null, "sycnNCStatus": null, "firstBillCode": "0yCVoxXanglmpVJ1sFkr", "firstBillBcode": "0K9jZr6uAy8TqfCVBZjY", "srcBillCode": "DBO20200512000020", "firstBillBomCode": {"success": "success", "message": "&#23457;&#25209;&#36890;&#36807;&#25104;&#21151;", "detailMsg": {"data": [{"id": "0yCVoxXanglmpVJ1sFkr", "dr": 0, "ts": 1589274243292, "creator": "smq", "creationTime": 1589274237000, "modifier": "smq", "modifiedTime": 1589274243292, "persistStatus": "upd", "promptMessage": null, "state": 3, "approver": "smq", "approveTime": 1589274243292, "approveOpinion": null, "sycnNCStatus": null, "sycnOutStatus": null, "pkOrgId": "abd7cf79-511d-4307-9bbd-d288b18d0ef9", "pkOrgCode": "1210", "pkOrgName": "\u897f\u5b89\u559c\u9a6c\u62c9\u96c5\u7f51\u7edc\u79d1\u6280\u6709\u9650\u516c\u53f8", "pkOrgInId": "abd7cf79-511d-4307-9bbd-d288b18d0ef9", "pkOrgInCode": "1210", "pkOrgInName": "\u897f\u5b89\u559c\u9a6c\u62c9\u96c5\u7f51\u7edc\u79d1\u6280\u6709\u9650\u516c\u53f8", "code": "DBO20200512000020", "billDate": 1589212800000, "billType": "Allocation", "billTranTypeId": "Allocation", "billTranTypeCode": "Allocation", "billTranTypeName": "\u8c03\u62e8\u5355", "outStorageId": "1001ZZ100000000DPAP4", "outStorageCode": "test030201", "outStorageName": "\u6d4b\u8bd5\u4ed3\u5e93030201", "outIfSlotManage": null, "inStorageId": "1001ZZ100000000DPAP6", "inStorageCode": "test030202", "inStorageName": "test030202", "inIfSlotManage": null, "outBizPersonId": null, "outBizPersonCode": null, "outBizPersonName": null, "inBizPersonId": "0mWG6nOSCxjsi1zoKEYs", "inBizPersonCode": "007", "inBizPersonName": "\u5e08\u5b5f\u5947", "outDeptId": "0K1ovYvAl1Pk00oCRPjV", "outDeptCode": "01010102", "outDeptName": "\u57ce\u5e02\u7ecf\u7406", "inDeptId": null, "inDeptCode": null, "inDeptName": null, "planSendDate": null, "planArriveDate": null, "currencyId": "CURRENCY-01", "currencyCode": "RMB", "currencyName": "\u4eba\u6c11\u5e01", "totalFactOutNum": null, "totalFactInNum": null, "billStatusId": null, "billStatusCode": null, "billStatusName": null, "transferStatusId": "0s21f51c-4d42-4100-dkd0-3254fbq33e6k", "transferStatusCode": "2", "transferStatusName": "\u5df2\u63d0\u4ea4\u5ba1\u6279", "stockBillBelong": null, "customerId": null, "customerName": null, "customerCode": null, "isClose": 0, "closer": null, "closeDate": null, "closeReason": null, "remark": "\u81ea\u52a8\u5316\u6d4b\u8bd5\u65b0\u589e\u8c03\u62e8\u5355", "transferBillItems": [{"id": "0K9jZr6uAy8TqfCVBZjY", "dr": 0, "ts": 1589274240000, "creator": "smq", "creationTime": 1589274240000, "modifier": null, "modifiedTime": null, "persistStatus": "nrm", "promptMessage": null, "rowNum": 10, "transferBillId": "0yCVoxXanglmpVJ1sFkr", "goodsId": "03e77ae0-469d-4d8a-ba34-733c2ada3749", "goodsCode": "301020000049", "goodsName": "\u5c0f\u96c5AI\u97f3\u7bb1\u65d7\u8230\u7248_\u77f3\u58a8\u7eff", "goodsFullName": null, "goodsBasicUnitName": "\u4e2a", "goodsAssistUnitName": "\u4e2a", "goodsConversionRate": 1.0, "enableBatchNumberManage": null, "productId": null, "productLineId": null, "isOptional": null, "unitId": "UNIT-12", "unitCode": "EA", "unitName": "\u4e2a", "transferNum": 30.0, "onwayNum": null, "totalOutNum": null, "totalInNum": null, "unitPrice": null, "amountMoney": 0.0, "remark": null, "batchNumId": null, "batchNumCode": null, "batchNumName": null, "goodsPositionId": null, "goodsPositionCode": null, "goodsPositionName": null, "receiverAddress": null, "provinceId": null, "provinceCode": null, "provinceName": null, "cityId": null, "cityCode": null, "cityName": null, "countyId": null, "countyCode": null, "countyName": null, "townId": null, "townCode": null, "townName": null, "detailAddr": null, "receiver": null, "receiverPhone": null, "receiverPhoneSpare": null, "isClose": 0, "sourceId": null, "sourceLineNum": null, "sourceType": null, "ext01": null, "ext02": null, "ext03": null, "ext04": null, "ext05": null, "ext06": null, "ext07": null, "ext08": null, "ext09": null, "ext10": null, "ext11": null, "ext12": null, "ext13": null, "ext14": null, "ext15": null, "goodsVersion": "1", "goodsSelection": null, "isMotherPiece": null, "customerId": null, "customerCode": null, "customerName": null, "supplierId": null, "supplierCode": null, "supplierName": null, "projectId": null, "projectCode": null, "projectName": null, "batchCodeId": null, "batchCodeCode": null, "stockStateId": null, "stockStateCode": null, "stockStateName": null, "enableBatchNoManage": null, "enableInvStatusManage": null, "originalGoodsId": null, "goodsSelectionDescription": null, "outStorageId": "1001ZZ100000000DPAP4", "outStorageCode": "test030201", "outStorageName": "\u6d4b\u8bd5\u4ed3\u5e93030201", "outIfSlotManage": null, "inStorageId": "1001ZZ100000000DPAP6", "inStorageCode": "test030202", "inStorageName": "test030202", "inIfSlotManage": null, "outPositionId": null, "outPositionCode": null, "outPositionName": null}], "transferBillItemBoms": [{"id": "03wRnTbGkbNYY9T8PYmf", "dr": 0, "ts": 1589274240000, "creator": "smq", "creationTime": 1589274240000, "modifier": null, "modifiedTime": null, "persistStatus": "nrm", "promptMessage": null, "rowNum": "10", "goodsId": "03e77ae0-469d-4d8a-ba34-733c2ada3749", "goodsCode": "301020000049", "goodsName": "\u5c0f\u96c5AI\u97f3\u7bb1\u65d7\u8230\u7248_\u77f3\u58a8\u7eff", "goodsFullName": null, "goodsBasicUnitName": "\u4e2a", "goodsAssistUnitName": "\u4e2a", "goodsConversionRate": 1.0, "enableBatchNumberManage": null, "productId": null, "productLineId": null, "unitId": "UNIT-12", "unitCode": "EA", "unitName": "\u4e2a", "transferNum": 30.0, "onwayNum": null, "totalOutNum": null, "totalInNum": null, "unitPrice": null, "amountMoney": 0.0, "remark": null, "batchNumId": null, "batchNumCode": null, "batchNumName": null, "goodsPositionId": null, "goodsPositionCode": null, "goodsPositionName": null, "receiverAddress": null, "provinceId": null, "provinceCode": null, "provinceName": null, "cityId": null, "cityCode": null, "cityName": null, "countyId": null, "countyCode": null, "countyName": null, "townId": null, "townCode": null, "townName": null, "detailAddr": null, "receiver": null, "receiverPhone": null, "receiverPhoneSpare": null, "isClose": 0, "sourceId": null, "sourceLineNum": null, "sourceType": null, "ext01": null, "ext02": null, "ext03": null, "ext04": null, "ext05": null, "ext06": null, "ext07": null, "ext08": null, "ext09": null, "ext10": null, "ext11": null, "ext12": null, "ext13": null, "ext14": null, "ext15": null, "goodsVersion": "1", "goodsSelection": null, "customerId": null, "customerCode": null, "customerName": null, "supplierId": null, "supplierCode": null, "supplierName": null, "projectId": null, "projectCode": null, "projectName": null, "batchCodeId": null, "batchCodeCode": null, "stockStateId": null, "stockStateCode": null, "stockStateName": null, "originalGoodsId": null, "goodsSelectionDescription": null, "itemId": "0K9jZr6uAy8TqfCVBZjY", "billId": "0yCVoxXanglmpVJ1sFkr", "parentGoodsId": "03e77ae0-469d-4d8a-ba34-733c2ada3749", "parentGoodsCode": "301020000049", "parentGoodsName": "\u5c0f\u96c5AI\u97f3\u7bb1\u65d7\u8230\u7248_\u77f3\u58a8\u7eff", "parentGoodsdisplayName": null, "parentRowNum": "10", "childGoodsQty": null, "firstBillBomCode": null, "srcBillBomCode": null, "outStorageId": "1001ZZ100000000DPAP4", "outStorageCode": "test030201", "outStorageName": "\u6d4b\u8bd5\u4ed3\u5e93030201", "outIfSlotManage": null, "inStorageId": "1001ZZ100000000DPAP6", "inStorageCode": "test030202", "inStorageName": "test030202", "inIfSlotManage": null, "outPositionId": null, "outPositionCode": null, "outPositionName": null}], "ext01": null, "ext02": null, "ext03": null, "ext04": null, "ext05": null, "ext06": null, "ext07": null, "ext08": null, "ext09": null, "ext10": null, "ext11": null, "ext12": null, "ext13": null, "ext14": null, "ext15": null, "isDistribution": null, "isReturned": null}]}}, "srcBillBomCode": {"success": "success", "message": "&#23457;&#25209;&#36890;&#36807;&#25104;&#21151;", "detailMsg": {"data": [{"id": "0yCVoxXanglmpVJ1sFkr", "dr": 0, "ts": 1589274243292, "creator": "smq", "creationTime": 1589274237000, "modifier": "smq", "modifiedTime": 1589274243292, "persistStatus": "upd", "promptMessage": null, "state": 3, "approver": "smq", "approveTime": 1589274243292, "approveOpinion": null, "sycnNCStatus": null, "sycnOutStatus": null, "pkOrgId": "abd7cf79-511d-4307-9bbd-d288b18d0ef9", "pkOrgCode": "1210", "pkOrgName": "\u897f\u5b89\u559c\u9a6c\u62c9\u96c5\u7f51\u7edc\u79d1\u6280\u6709\u9650\u516c\u53f8", "pkOrgInId": "abd7cf79-511d-4307-9bbd-d288b18d0ef9", "pkOrgInCode": "1210", "pkOrgInName": "\u897f\u5b89\u559c\u9a6c\u62c9\u96c5\u7f51\u7edc\u79d1\u6280\u6709\u9650\u516c\u53f8", "code": "DBO20200512000020", "billDate": 1589212800000, "billType": "Allocation", "billTranTypeId": "Allocation", "billTranTypeCode": "Allocation", "billTranTypeName": "\u8c03\u62e8\u5355", "outStorageId": "1001ZZ100000000DPAP4", "outStorageCode": "test030201", "outStorageName": "\u6d4b\u8bd5\u4ed3\u5e93030201", "outIfSlotManage": null, "inStorageId": "1001ZZ100000000DPAP6", "inStorageCode": "test030202", "inStorageName": "test030202", "inIfSlotManage": null, "outBizPersonId": null, "outBizPersonCode": null, "outBizPersonName": null, "inBizPersonId": "0mWG6nOSCxjsi1zoKEYs", "inBizPersonCode": "007", "inBizPersonName": "\u5e08\u5b5f\u5947", "outDeptId": "0K1ovYvAl1Pk00oCRPjV", "outDeptCode": "01010102", "outDeptName": "\u57ce\u5e02\u7ecf\u7406", "inDeptId": null, "inDeptCode": null, "inDeptName": null, "planSendDate": null, "planArriveDate": null, "currencyId": "CURRENCY-01", "currencyCode": "RMB", "currencyName": "\u4eba\u6c11\u5e01", "totalFactOutNum": null, "totalFactInNum": null, "billStatusId": null, "billStatusCode": null, "billStatusName": null, "transferStatusId": "0s21f51c-4d42-4100-dkd0-3254fbq33e6k", "transferStatusCode": "2", "transferStatusName": "\u5df2\u63d0\u4ea4\u5ba1\u6279", "stockBillBelong": null, "customerId": null, "customerName": null, "customerCode": null, "isClose": 0, "closer": null, "closeDate": null, "closeReason": null, "remark": "\u81ea\u52a8\u5316\u6d4b\u8bd5\u65b0\u589e\u8c03\u62e8\u5355", "transferBillItems": [{"id": "0K9jZr6uAy8TqfCVBZjY", "dr": 0, "ts": 1589274240000, "creator": "smq", "creationTime": 1589274240000, "modifier": null, "modifiedTime": null, "persistStatus": "nrm", "promptMessage": null, "rowNum": 10, "transferBillId": "0yCVoxXanglmpVJ1sFkr", "goodsId": "03e77ae0-469d-4d8a-ba34-733c2ada3749", "goodsCode": "301020000049", "goodsName": "\u5c0f\u96c5AI\u97f3\u7bb1\u65d7\u8230\u7248_\u77f3\u58a8\u7eff", "goodsFullName": null, "goodsBasicUnitName": "\u4e2a", "goodsAssistUnitName": "\u4e2a", "goodsConversionRate": 1.0, "enableBatchNumberManage": null, "productId": null, "productLineId": null, "isOptional": null, "unitId": "UNIT-12", "unitCode": "EA", "unitName": "\u4e2a", "transferNum": 30.0, "onwayNum": null, "totalOutNum": null, "totalInNum": null, "unitPrice": null, "amountMoney": 0.0, "remark": null, "batchNumId": null, "batchNumCode": null, "batchNumName": null, "goodsPositionId": null, "goodsPositionCode": null, "goodsPositionName": null, "receiverAddress": null, "provinceId": null, "provinceCode": null, "provinceName": null, "cityId": null, "cityCode": null, "cityName": null, "countyId": null, "countyCode": null, "countyName": null, "townId": null, "townCode": null, "townName": null, "detailAddr": null, "receiver": null, "receiverPhone": null, "receiverPhoneSpare": null, "isClose": 0, "sourceId": null, "sourceLineNum": null, "sourceType": null, "ext01": null, "ext02": null, "ext03": null, "ext04": null, "ext05": null, "ext06": null, "ext07": null, "ext08": null, "ext09": null, "ext10": null, "ext11": null, "ext12": null, "ext13": null, "ext14": null, "ext15": null, "goodsVersion": "1", "goodsSelection": null, "isMotherPiece": null, "customerId": null, "customerCode": null, "customerName": null, "supplierId": null, "supplierCode": null, "supplierName": null, "projectId": null, "projectCode": null, "projectName": null, "batchCodeId": null, "batchCodeCode": null, "stockStateId": null, "stockStateCode": null, "stockStateName": null, "enableBatchNoManage": null, "enableInvStatusManage": null, "originalGoodsId": null, "goodsSelectionDescription": null, "outStorageId": "1001ZZ100000000DPAP4", "outStorageCode": "test030201", "outStorageName": "\u6d4b\u8bd5\u4ed3\u5e93030201", "outIfSlotManage": null, "inStorageId": "1001ZZ100000000DPAP6", "inStorageCode": "test030202", "inStorageName": "test030202", "inIfSlotManage": null, "outPositionId": null, "outPositionCode": null, "outPositionName": null}], "transferBillItemBoms": [{"id": "03wRnTbGkbNYY9T8PYmf", "dr": 0, "ts": 1589274240000, "creator": "smq", "creationTime": 1589274240000, "modifier": null, "modifiedTime": null, "persistStatus": "nrm", "promptMessage": null, "rowNum": "10", "goodsId": "03e77ae0-469d-4d8a-ba34-733c2ada3749", "goodsCode": "301020000049", "goodsName": "\u5c0f\u96c5AI\u97f3\u7bb1\u65d7\u8230\u7248_\u77f3\u58a8\u7eff", "goodsFullName": null, "goodsBasicUnitName": "\u4e2a", "goodsAssistUnitName": "\u4e2a", "goodsConversionRate": 1.0, "enableBatchNumberManage": null, "productId": null, "productLineId": null, "unitId": "UNIT-12", "unitCode": "EA", "unitName": "\u4e2a", "transferNum": 30.0, "onwayNum": null, "totalOutNum": null, "totalInNum": null, "unitPrice": null, "amountMoney": 0.0, "remark": null, "batchNumId": null, "batchNumCode": null, "batchNumName": null, "goodsPositionId": null, "goodsPositionCode": null, "goodsPositionName": null, "receiverAddress": null, "provinceId": null, "provinceCode": null, "provinceName": null, "cityId": null, "cityCode": null, "cityName": null, "countyId": null, "countyCode": null, "countyName": null, "townId": null, "townCode": null, "townName": null, "detailAddr": null, "receiver": null, "receiverPhone": null, "receiverPhoneSpare": null, "isClose": 0, "sourceId": null, "sourceLineNum": null, "sourceType": null, "ext01": null, "ext02": null, "ext03": null, "ext04": null, "ext05": null, "ext06": null, "ext07": null, "ext08": null, "ext09": null, "ext10": null, "ext11": null, "ext12": null, "ext13": null, "ext14": null, "ext15": null, "goodsVersion": "1", "goodsSelection": null, "customerId": null, "customerCode": null, "customerName": null, "supplierId": null, "supplierCode": null, "supplierName": null, "projectId": null, "projectCode": null, "projectName": null, "batchCodeId": null, "batchCodeCode": null, "stockStateId": null, "stockStateCode": null, "stockStateName": null, "originalGoodsId": null, "goodsSelectionDescription": null, "itemId": "0K9jZr6uAy8TqfCVBZjY", "billId": "0yCVoxXanglmpVJ1sFkr", "parentGoodsId": "03e77ae0-469d-4d8a-ba34-733c2ada3749", "parentGoodsCode": "301020000049", "parentGoodsName": "\u5c0f\u96c5AI\u97f3\u7bb1\u65d7\u8230\u7248_\u77f3\u58a8\u7eff", "parentGoodsdisplayName": null, "parentRowNum": "10", "childGoodsQty": null, "firstBillBomCode": null, "srcBillBomCode": null, "outStorageId": "1001ZZ100000000DPAP4", "outStorageCode": "test030201", "outStorageName": "\u6d4b\u8bd5\u4ed3\u5e93030201", "outIfSlotManage": null, "inStorageId": "1001ZZ100000000DPAP6", "inStorageCode": "test030202", "inStorageName": "test030202", "inIfSlotManage": null, "outPositionId": null, "outPositionCode": null, "outPositionName": null}], "ext01": null, "ext02": null, "ext03": null, "ext04": null, "ext05": null, "ext06": null, "ext07": null, "ext08": null, "ext09": null, "ext10": null, "ext11": null, "ext12": null, "ext13": null, "ext14": null, "ext15": null, "isDistribution": null, "isReturned": null}]}}}'
    # h.init_request(depend_Case,relevance,parameter)
