# -*- coding: utf-8 -*-
# !/bin/bash
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
                    log.info("json格式校验，校验关键字%s:预期%s与返回%s类型不一致" % (this_key, src_data[this_key], res_data[this_key]))
                    flag = False
                    # return flag
                    # raise Exception("json格式校验，校验关键字%s与返回关键字%s类型不一致"%(src_data[this_key],res_data[this_key]))
                else:
                    # print('%s校验通过'%this_key)
                    flag = True

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
    check_type = case['CheckType']

    if check_type == 'no_check':
        with allure.step('接口无需校验'):
            return True
    elif check_type == 'only_check_status':
        with allure.step('接口仅校验HTTP状态码'):
            allure.attach(str(case['ExpectedCode']), '预期code是')
            allure.attach(str(code), '实际code是')
        if code == case['ExpectedCode']:
            log.info("HTTP状态码校验通过！")
            return True
        else:
            log.info("HTTP返回状态码与预期不一致")
            return False

    elif check_type == 'check_json':
        with allure.step("校验返回json数据结构"):
            allure.attach(str(case['ExpectedCode']), '预期code')
            allure.attach(str(code), '实际code是')
            allure.attach(str(case['ExpectedData']), '预期data')
            allure.attach(str(res_data), '实际data')
            if code == case['ExpectedCode']:
                if not res_data:  # 判断res_data为None,  False, 空字符串"", 0, 空列表[], 空字典{}, 空元组()
                    res_data = '{}'
                else:
                    expected_data_dict = case['ExpectedData']
                    result = check_json(expected_data_dict, res_data)

                    if result is False:
                        log.info('JSON格式校验失败！')
                        log.debug('预期结果是%s'%expected_data_dict)
                        log.debug('实际结果是：%s'%res_data)
                        log.debug('预期类型是%s'%type(expected_data_dict))
                        log.debug('实际类型是%s' % type(res_data))
                        return False
                    else:
                        log.info('JSON格式校验成功！')
                        log.debug('预期结果是%s' % expected_data_dict)
                        log.debug('实际结果是：%s' % res_data)
                        log.debug('预期类型是%s' % type(expected_data_dict))
                        log.debug('实际类型是%s' % type(res_data))
                        return True
            else:
                log.info("HTTP返回状态码%s与预期%s不一致" % (str(code), str(case['ExpectedCode'])))
                return False
    else:
        log.error('校验类型不存在！')


if __name__ == '__main__':
    case_data ={'CaseId': 6, 'CaseName': 'approve_allocation_bill', 'APIName': '审批调拨订单', 'Headers': {'Content-Type': 'application/json', 'charset': 'UTF-8'}, 'Path': '/occ-stock/stock/allocation-bill/approveWithoutBpm', 'Method': 'post', 'ParameterType': 'parameter', 'Params': {'billId': 'allocation-create-and-submit2'}, 'CheckType': 'check_json', 'ExpectedCode': 200, 'ExpectedData': {'success': 'success', 'message': '&#23457;&#25209;&#36890;&#36807;&#25104;&#21151;', 'detailMsg': {'data': [{'id': '0xtxaRhbIHPaZOkUgTlO', 'dr': 0, 'ts': 1589447391772, 'creator': 'smq', 'creationTime': 1589447386000, 'modifier': 'smq', 'modifiedTime': 1589447391772, 'persistStatus': 'upd', 'promptMessage': None, 'state': 3, 'approver': 'smq', 'approveTime': 1589447391772, 'approveOpinion': None, 'sycnNCStatus': None, 'sycnOutStatus': None, 'pkOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9', 'pkOrgCode': '1210', 'pkOrgName': '西安喜马拉雅网络科技有限公司', 'pkOrgInId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9', 'pkOrgInCode': '1210', 'pkOrgInName': '西安喜马拉雅网络科技有限公司', 'code': 'DBO20200514000037', 'billDate': 1589212800000, 'billType': 'Allocation', 'billTranTypeId': 'Allocation', 'billTranTypeCode': 'Allocation', 'billTranTypeName': '调拨单', 'outStorageId': '1001ZZ100000000DPAP4', 'outStorageCode': 'test030201', 'outStorageName': '测试仓库030201', 'outIfSlotManage': 0, 'inStorageId': '1001ZZ100000000DPAP6', 'inStorageCode': 'test030202', 'inStorageName': 'test030202', 'inIfSlotManage': 0, 'outBizPersonId': None, 'outBizPersonCode': None, 'outBizPersonName': None, 'inBizPersonId': '0mWG6nOSCxjsi1zoKEYs', 'inBizPersonCode': '007', 'inBizPersonName': '师孟奇', 'outDeptId': '0K1ovYvAl1Pk00oCRPjV', 'outDeptCode': '01010102', 'outDeptName': '城市经理', 'inDeptId': None, 'inDeptCode': None, 'inDeptName': None, 'planSendDate': None, 'planArriveDate': None, 'currencyId': 'CURRENCY-01', 'currencyCode': 'RMB', 'currencyName': '人民币', 'totalFactOutNum': None, 'totalFactInNum': None, 'billStatusId': None, 'billStatusCode': None, 'billStatusName': None, 'transferStatusId': '0s21f51c-4d42-4100-dkd0-3254fbq33e6k', 'transferStatusCode': '2', 'transferStatusName': '已提交审批', 'stockBillBelong': None, 'customerId': None, 'customerName': None, 'customerCode': None, 'isClose': 0, 'closer': None, 'closeDate': None, 'closeReason': None, 'remark': '自动化测试新增调拨单', 'transferBillItems': [{'id': '0bf4cJbB8hoao89ctKzG', 'dr': 0, 'ts': 1589447389000, 'creator': 'smq', 'creationTime': 1589447389000, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm', 'promptMessage': None, 'rowNum': 10, 'transferBillId': '0xtxaRhbIHPaZOkUgTlO', 'goodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'goodsCode': '301020000049', 'goodsName': '小雅AI音箱旗舰版_石墨绿', 'goodsFullName': None, 'goodsBasicUnitName': '个', 'goodsAssistUnitName': '个', 'goodsConversionRate': 1.0, 'enableBatchNumberManage': 0, 'productId': '996cc839-60e8-4500-82c6-9a7c7b95646d', 'productLineId': '13c512df-ad18-48e5-b75d-166a534cc410', 'isOptional': 0, 'unitId': 'UNIT-12', 'unitCode': 'EA', 'unitName': '个', 'transferNum': 30.0, 'onwayNum': None, 'totalOutNum': None, 'totalInNum': None, 'unitPrice': None, 'amountMoney': 0.0, 'remark': None, 'batchNumId': None, 'batchNumCode': None, 'batchNumName': None, 'goodsPositionId': None, 'goodsPositionCode': None, 'goodsPositionName': None, 'receiverAddress': None, 'provinceId': None, 'provinceCode': None, 'provinceName': None, 'cityId': None, 'cityCode': None, 'cityName': None, 'countyId': None, 'countyCode': None, 'countyName': None, 'townId': None, 'townCode': None, 'townName': None, 'detailAddr': None, 'receiver': None, 'receiverPhone': None, 'receiverPhoneSpare': None, 'isClose': 0, 'sourceId': None, 'sourceLineNum': None, 'sourceType': None, 'ext01': None, 'ext02': None, 'ext03': None, 'ext04': None, 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None, 'goodsVersion': '1', 'goodsSelection': None, 'isMotherPiece': None, 'customerId': None, 'customerCode': None, 'customerName': None, 'supplierId': None, 'supplierCode': None, 'supplierName': None, 'projectId': None, 'projectCode': None, 'projectName': None, 'batchCodeId': None, 'batchCodeCode': None, 'stockStateId': None, 'stockStateCode': None, 'stockStateName': None, 'enableBatchNoManage': 0, 'enableInvStatusManage': 0, 'originalGoodsId': None, 'goodsSelectionDescription': None, 'outStorageId': '1001ZZ100000000DPAP4', 'outStorageCode': 'test030201', 'outStorageName': '测试仓库030201', 'outIfSlotManage': 0, 'inStorageId': '1001ZZ100000000DPAP6', 'inStorageCode': 'test030202', 'inStorageName': 'test030202', 'inIfSlotManage': None, 'outPositionId': None, 'outPositionCode': None, 'outPositionName': None}], 'transferBillItemBoms': [{'id': '0wQlvLXAd3FT4TBew4gi', 'dr': 0, 'ts': 1589447389000, 'creator': 'smq', 'creationTime': 1589447389000, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm', 'promptMessage': None, 'rowNum': '10', 'goodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'goodsCode': '301020000049', 'goodsName': '小雅AI音箱旗舰版_石墨绿', 'goodsFullName': None, 'goodsBasicUnitName': '个', 'goodsAssistUnitName': '个', 'goodsConversionRate': 1.0, 'enableBatchNumberManage': 0, 'productId': '996cc839-60e8-4500-82c6-9a7c7b95646d', 'productLineId': '13c512df-ad18-48e5-b75d-166a534cc410', 'unitId': 'UNIT-12', 'unitCode': 'EA', 'unitName': '个', 'transferNum': 30.0, 'onwayNum': None, 'totalOutNum': None, 'totalInNum': None, 'unitPrice': None, 'amountMoney': 0.0, 'remark': None, 'batchNumId': None, 'batchNumCode': None, 'batchNumName': None, 'goodsPositionId': None, 'goodsPositionCode': None, 'goodsPositionName': None, 'receiverAddress': None, 'provinceId': None, 'provinceCode': None, 'provinceName': None, 'cityId': None, 'cityCode': None, 'cityName': None, 'countyId': None, 'countyCode': None, 'countyName': None, 'townId': None, 'townCode': None, 'townName': None, 'detailAddr': None, 'receiver': None, 'receiverPhone': None, 'receiverPhoneSpare': None, 'isClose': 0, 'sourceId': None, 'sourceLineNum': None, 'sourceType': None, 'ext01': None, 'ext02': None, 'ext03': None, 'ext04': None, 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None, 'goodsVersion': '1', 'goodsSelection': None, 'customerId': None, 'customerCode': None, 'customerName': None, 'supplierId': None, 'supplierCode': None, 'supplierName': None, 'projectId': None, 'projectCode': None, 'projectName': None, 'batchCodeId': None, 'batchCodeCode': None, 'stockStateId': None, 'stockStateCode': None, 'stockStateName': None, 'originalGoodsId': None, 'goodsSelectionDescription': None, 'itemId': '0bf4cJbB8hoao89ctKzG', 'billId': '0xtxaRhbIHPaZOkUgTlO', 'parentGoodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'parentGoodsCode': '301020000049', 'parentGoodsName': '小雅AI音箱旗舰版_石墨绿', 'parentGoodsdisplayName': None, 'parentRowNum': '10', 'childGoodsQty': None, 'firstBillBomCode': None, 'srcBillBomCode': None, 'outStorageId': '1001ZZ100000000DPAP4', 'outStorageCode': 'test030201', 'outStorageName': '测试仓库030201', 'outIfSlotManage': 0, 'inStorageId': '1001ZZ100000000DPAP6', 'inStorageCode': 'test030202', 'inStorageName': 'test030202', 'inIfSlotManage': None, 'outPositionId': None, 'outPositionCode': None, 'outPositionName': None}], 'ext01': None, 'ext02': None, 'ext03': None, 'ext04': None, 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None, 'isDistribution': None, 'isReturned': None}]}}, 'User': 'Manager', 'DependCase': 'submit_allocation_bill', 'RelevanceList': {'billId': '$..id'}}

    code = 200
    response =  {'success': 'success', 'message': '&#23457;&#25209;&#36890;&#36807;&#25104;&#21151;', 'detailMsg': {'data': [{'id': '06MwWrq4k4UuyjQEJpAz', 'dr': 0, 'ts': 1589452159115, 'creator': 'smq', 'creationTime': 1589452152000, 'modifier': 'smq', 'modifiedTime': 1589452159115, 'persistStatus': 'upd', 'promptMessage': None, 'state': 3, 'approver': 'smq', 'approveTime': 1589452159115, 'approveOpinion': None, 'sycnNCStatus': None, 'sycnOutStatus': None, 'pkOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9', 'pkOrgCode': '1210', 'pkOrgName': '西安喜马拉雅网络科技有限公司', 'pkOrgInId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9', 'pkOrgInCode': '1210', 'pkOrgInName': '西安喜马拉雅网络科技有限公司', 'code': 'DBO20200514000063', 'billDate': 1589212800000, 'billType': 'Allocation', 'billTranTypeId': 'Allocation', 'billTranTypeCode': 'Allocation', 'billTranTypeName': '调拨单', 'outStorageId': '1001ZZ100000000DPAP4', 'outStorageCode': 'test030201', 'outStorageName': '测试仓库030201', 'outIfSlotManage': 0, 'inStorageId': '1001ZZ100000000DPAP6', 'inStorageCode': 'test030202', 'inStorageName': 'test030202', 'inIfSlotManage': 0, 'outBizPersonId': None, 'outBizPersonCode': None, 'outBizPersonName': None, 'inBizPersonId': '0mWG6nOSCxjsi1zoKEYs', 'inBizPersonCode': '007', 'inBizPersonName': '师孟奇', 'outDeptId': '0K1ovYvAl1Pk00oCRPjV', 'outDeptCode': '01010102', 'outDeptName': '城市经理', 'inDeptId': None, 'inDeptCode': None, 'inDeptName': None, 'planSendDate': None, 'planArriveDate': None, 'currencyId': 'CURRENCY-01', 'currencyCode': 'RMB', 'currencyName': '人民币', 'totalFactOutNum': None, 'totalFactInNum': None, 'billStatusId': None, 'billStatusCode': None, 'billStatusName': None, 'transferStatusId': '0s21f51c-4d42-4100-dkd0-3254fbq33e6k', 'transferStatusCode': '2', 'transferStatusName': '已提交审批', 'stockBillBelong': None, 'customerId': None, 'customerName': None, 'customerCode': None, 'isClose': 0, 'closer': None, 'closeDate': None, 'closeReason': None, 'remark': '自动化测试新增调拨单', 'transferBillItems': [{'id': '0GwdQA5KNiXMMRPCSv59', 'dr': 0, 'ts': 1589452156000, 'creator': 'smq', 'creationTime': 1589452156000, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm', 'promptMessage': None, 'rowNum': 10, 'transferBillId': '06MwWrq4k4UuyjQEJpAz', 'goodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'goodsCode': '301020000049', 'goodsName': '小雅AI音箱旗舰版_石墨绿', 'goodsFullName': None, 'goodsBasicUnitName': '个', 'goodsAssistUnitName': '个', 'goodsConversionRate': 1.0, 'enableBatchNumberManage': 0, 'productId': '996cc839-60e8-4500-82c6-9a7c7b95646d', 'productLineId': '13c512df-ad18-48e5-b75d-166a534cc410', 'isOptional': 0, 'unitId': 'UNIT-12', 'unitCode': 'EA', 'unitName': '个', 'transferNum': 30.0, 'onwayNum': None, 'totalOutNum': None, 'totalInNum': None, 'unitPrice': None, 'amountMoney': 0.0, 'remark': None, 'batchNumId': None, 'batchNumCode': None, 'batchNumName': None, 'goodsPositionId': None, 'goodsPositionCode': None, 'goodsPositionName': None, 'receiverAddress': None, 'provinceId': None, 'provinceCode': None, 'provinceName': None, 'cityId': None, 'cityCode': None, 'cityName': None, 'countyId': None, 'countyCode': None, 'countyName': None, 'townId': None, 'townCode': None, 'townName': None, 'detailAddr': None, 'receiver': None, 'receiverPhone': None, 'receiverPhoneSpare': None, 'isClose': 0, 'sourceId': None, 'sourceLineNum': None, 'sourceType': None, 'ext01': None, 'ext02': None, 'ext03': None, 'ext04': None, 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None, 'goodsVersion': '1', 'goodsSelection': None, 'isMotherPiece': None, 'customerId': None, 'customerCode': None, 'customerName': None, 'supplierId': None, 'supplierCode': None, 'supplierName': None, 'projectId': None, 'projectCode': None, 'projectName': None, 'batchCodeId': None, 'batchCodeCode': None, 'stockStateId': None, 'stockStateCode': None, 'stockStateName': None, 'enableBatchNoManage': 0, 'enableInvStatusManage': 0, 'originalGoodsId': None, 'goodsSelectionDescription': None, 'outStorageId': '1001ZZ100000000DPAP4', 'outStorageCode': 'test030201', 'outStorageName': '测试仓库030201', 'outIfSlotManage': 0, 'inStorageId': '1001ZZ100000000DPAP6', 'inStorageCode': 'test030202', 'inStorageName': 'test030202', 'inIfSlotManage': None, 'outPositionId': None, 'outPositionCode': None, 'outPositionName': None}], 'transferBillItemBoms': [{'id': '048SYwdIn8hCuu2RFXFr', 'dr': 0, 'ts': 1589452156000, 'creator': 'smq', 'creationTime': 1589452156000, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm', 'promptMessage': None, 'rowNum': '10', 'goodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'goodsCode': '301020000049', 'goodsName': '小雅AI音箱旗舰版_石墨绿', 'goodsFullName': None, 'goodsBasicUnitName': '个', 'goodsAssistUnitName': '个', 'goodsConversionRate': 1.0, 'enableBatchNumberManage': 0, 'productId': '996cc839-60e8-4500-82c6-9a7c7b95646d', 'productLineId': '13c512df-ad18-48e5-b75d-166a534cc410', 'unitId': 'UNIT-12', 'unitCode': 'EA', 'unitName': '个', 'transferNum': 30.0, 'onwayNum': None, 'totalOutNum': None, 'totalInNum': None, 'unitPrice': None, 'amountMoney': 0.0, 'remark': None, 'batchNumId': None, 'batchNumCode': None, 'batchNumName': None, 'goodsPositionId': None, 'goodsPositionCode': None, 'goodsPositionName': None, 'receiverAddress': None, 'provinceId': None, 'provinceCode': None, 'provinceName': None, 'cityId': None, 'cityCode': None, 'cityName': None, 'countyId': None, 'countyCode': None, 'countyName': None, 'townId': None, 'townCode': None, 'townName': None, 'detailAddr': None, 'receiver': None, 'receiverPhone': None, 'receiverPhoneSpare': None, 'isClose': 0, 'sourceId': None, 'sourceLineNum': None, 'sourceType': None, 'ext01': None, 'ext02': None, 'ext03': None, 'ext04': None, 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None, 'goodsVersion': '1', 'goodsSelection': None, 'customerId': None, 'customerCode': None, 'customerName': None, 'supplierId': None, 'supplierCode': None, 'supplierName': None, 'projectId': None, 'projectCode': None, 'projectName': None, 'batchCodeId': None, 'batchCodeCode': None, 'stockStateId': None, 'stockStateCode': None, 'stockStateName': None, 'originalGoodsId': None, 'goodsSelectionDescription': None, 'itemId': '0GwdQA5KNiXMMRPCSv59', 'billId': '06MwWrq4k4UuyjQEJpAz', 'parentGoodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'parentGoodsCode': '301020000049', 'parentGoodsName': '小雅AI音箱旗舰版_石墨绿', 'parentGoodsdisplayName': None, 'parentRowNum': '10', 'childGoodsQty': None, 'firstBillBomCode': None, 'srcBillBomCode': None, 'outStorageId': '1001ZZ100000000DPAP4', 'outStorageCode': 'test030201', 'outStorageName': '测试仓库030201', 'outIfSlotManage': 0, 'inStorageId': '1001ZZ100000000DPAP6', 'inStorageCode': 'test030202', 'inStorageName': 'test030202', 'inIfSlotManage': None, 'outPositionId': None, 'outPositionCode': None, 'outPositionName': None}], 'ext01': None, 'ext02': None, 'ext03': None, 'ext04': None, 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None, 'isDistribution': None, 'isReturned': None}]}}


    check_result(case_data, code, response)
