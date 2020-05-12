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
            log.info("HTTP返回状态码与预期不一致")
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

                    if result is False:
                        log.info('JSON格式校验失败！')
                        return False
                    else:
                        log.info('JSON格式校验成功！')
                        return True
            else:
                log.info("HTTP返回状态码%s与预期%s不一致" % (str(code), int(case['ExpectedCode'])))
                return False
    else:
        log.error('校验类型不存在！')

if __name__ == '__main__':
    casedata={'CaseId': 14.0, 'CaseName': 'create_transfer-in-bills', 'APIName': '新增调拨入库单', 'Headers': "{'Content-Type':'application/json','charset': 'UTF-8'}", 'Path': '/occ-stock/stock/transfer-in-bills', 'Method': 'post', 'ParameterType': 'json', 'Params': '{"id":null,"stockOrgInId":"abd7cf79-511d-4307-9bbd-d288b18d0ef9","stockOrgInCode":"1210","stockOrgInName":"西安喜马拉雅网络科技有限公司","billCode":null,"billDate":1588953600000,"billType":"AllocationIn","billTranTypeId":"AllocationIn","billTranTypeCode":null,"billTranTypeName":null,"storageId":"1001ZZ100000000DPAP6","storageCode":"test030202","storageName":"test030202","ifSlotManage":null,"storekeeperId":null,"storekeeperCode":null,"storekeeperName":null,"inDate":"","planSendDate":"","planArriveDate":"","currencyId":null,"currencyCode":null,"currencyName":null,"totalShouldInNum":"5.00","totalFactInNum":"3.00","billStatusId":null,"billStatusName":"自由","billStatusCode":"01","stockBillBelong":"0DKeeV9TPwv3UZiad8EH","customerId":null,"customerCode":null,"customerName":null,"bizPersonId":null,"bizPersonCode":null,"bizPersonName":null,"deparmentId":"ae96b9ed-82dc-4aa7-bf97-cdd18a18c1a9","deparmentCode":"01010102","deparmentName":"城市经理","logisticsId":null,"logisticsCode":null,"logisticsName":null,"siger":null,"signTime":"","cancelReason":null,"remark":"自动化测试参照调拨出库单新增调拨入库单","realLogisticsCompanyCode":null,"realLogisticsCompanyId":null,"realLogisticsCompanyName":null,"logisticsBillCode":null,"outStorageId":"1001ZZ100000000DPAP4","outStorageCode":"test030201","outStorageName":"测试仓库030201","dr":0,"ts":null,"creator":null,"creationTime":null,"modifier":null,"modifiedTime":null,"persistStatus":"upd","promptMessage":null,"stockOrgId":"abd7cf79-511d-4307-9bbd-d288b18d0ef9","stockOrgCode":"1210","stockOrgName":"西安喜马拉雅网络科技有限公司","outIfSlotManage":null,"transferInBillItems":[{"transferOutBillId":null,"rowNum":10,"goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","goodsCode":"301020000049","goodsName":"小雅AI音箱旗舰版_石墨绿","goodsFullName":null,"goodsBasicUnitName":null,"goodsAssistUnitName":null,"unitId":"UNIT-12","unitCode":"EA","unitName":"个","goodsConversionRate":null,"shouldInNum":"5.000000","factInNum":"3.000000","unitPrice":"","amountMoney":"0.00","batchNumId":null,"batchNumCode":null,"batchNumName":null,"goodsPositionId":null,"goodsPositionName":null,"stockInPersonId":null,"stockInPersonCode":null,"stockInPersonName":null,"stockInDate":"","firstBillCode":"DBO20200508000034","firstBillBcode":"0Tr6HVsgvmzwBQYy2d6i","firstBillType":null,"srcBillCode":"TDN2020050900003","srcBillBcode":"0RVbhbtQZhT5PZkp19zW","srcBillType":"AllocationOut","remark":null,"goodsVersion":"1","batchCodeId":null,"batchCodeCode":null,"batchCodeName":null,"supplierId":null,"supplierName":null,"supplierCode":null,"projectId":null,"projectCode":null,"projectName":null,"stockStateId":null,"stockStateCode":null,"stockStateName":null,"customerId":null,"customerCode":null,"customerName":null,"originalGoodsId":null,"goodsSelection":null,"goodsSelectionDescription":null,"id":null,"dr":0,"ts":null,"creator":null,"creationTime":null,"modifier":null,"modifiedTime":null,"persistStatus":"new","promptMessage":null,"transferInBillId":null,"enableBatchNumberManage":null,"productId":null,"productLineId":null,"isOptional":null,"goodsPositionCode":null,"isMotherPiece":null,"enableBatchNoManage":null,"enableInvStatusManage":null,"ext01":null,"ext02":null,"ext03":"AllocationOut","ext04":"Allocation","ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":"0TszFCIVqcbJkmpWHQhq","ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null}],"transferInBillItemBoms":[{"transferOutBillId":null,"rowNum":"10","goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","goodsCode":"301020000049","goodsName":"小雅AI音箱旗舰版_石墨绿","goodsFullName":null,"goodsBasicUnitName":null,"goodsAssistUnitName":null,"unitId":"UNIT-12","unitCode":"EA","unitName":"个","goodsConversionRate":null,"shouldInNum":"5.000000","factInNum":"3.000000","unitPrice":"","amountMoney":"0.00","batchNumId":null,"batchNumCode":null,"batchNumName":null,"goodsPositionId":null,"goodsPositionName":null,"stockInPersonId":null,"stockInPersonCode":null,"stockInPersonName":null,"stockInDate":"","firstBillCode":"0DKeeV9TPwv3UZiad8EH","firstBillBcode":"0Tr6HVsgvmzwBQYy2d6i","firstBillType":null,"srcBillCode":"TDN2020050900003","srcBillBcode":"0RVbhbtQZhT5PZkp19zW","srcBillType":null,"remark":null,"goodsVersion":"1","goodsSelection":null,"goodsNum":null,"parentGoodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","parentGoodsCode":"301020000049","parentGoodsName":"小雅AI音箱旗舰版_石墨绿","parentRowNum":"10","childGoodsQty":"","batchCodeId":null,"batchCodeCode":null,"batchCodeName":null,"supplierId":null,"supplierName":null,"supplierCode":null,"projectId":null,"projectCode":null,"projectName":null,"stockStateId":null,"stockStateCode":null,"stockStateName":null,"customerId":null,"customerCode":null,"customerName":null,"originalGoodsId":null,"goodsSelectionDescription":null,"id":null,"dr":0,"ts":null,"creator":null,"creationTime":null,"modifier":null,"modifiedTime":null,"persistStatus":"new","promptMessage":null,"enableBatchNumberManage":null,"productId":null,"productLineId":null,"goodsPositionCode":null,"itemId":null,"billId":null,"parentGoodsdisplayName":null,"firstBillBomCode":"0CrhvlIZ5uIVEXmYN9Hq","srcBillBomCode":"0K1xchlRSFmYGxaooi2J","ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":"0TszFCIVqcbJkmpWHQhq","ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null}],"srcSystem":null,"srcSystemId":null,"srcSystemCode":null,"srcSystemName":null,"ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null,"sycnOutStatus":null,"sycnNCStatus":null}', 'CheckTpye': 'check_json', 'ExpectedCode': 200.0, 'ExpectedData': '{"id":"0aCwS5YrnRm6S7RHlOXZ","dr":0,"ts":1589012705000,"creator":"smq","creationTime":1589012705000,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":"","stockOrgId":"abd7cf79-511d-4307-9bbd-d288b18d0ef9","stockOrgCode":"1210","stockOrgName":"西安喜马拉雅网络科技有限公司","stockOrgInId":"abd7cf79-511d-4307-9bbd-d288b18d0ef9","stockOrgInCode":"1210","stockOrgInName":"西安喜马拉雅网络科技有限公司","billCode":"TRN2020050900013","billDate":1588953600000,"billType":"AllocationIn","billTranTypeId":"AllocationIn","billTranTypeCode":"AllocationIn","billTranTypeName":"调拨入库","storageId":"1001ZZ100000000DPAP6","storageCode":"test030202","storageName":"test030202","ifSlotManage":null,"outStorageId":"1001ZZ100000000DPAP4","outStorageCode":"test030201","outStorageName":"测试仓库030201","outIfSlotManage":null,"storekeeperId":null,"storekeeperCode":null,"storekeeperName":null,"inDate":null,"planArriveDate":null,"currencyId":null,"currencyCode":null,"currencyName":null,"totalShouldInNum":5.00000000,"totalFactInNum":3.00000000,"billStatusId":"099aj5df-4y42-4700-d8d6-3714fdb43e68","billStatusCode":"01","billStatusName":"自由","stockBillBelong":"0DKeeV9TPwv3UZiad8EH","customerId":null,"customerCode":null,"customerName":null,"bizPersonId":null,"bizPersonCode":null,"bizPersonName":null,"deparmentId":"ae96b9ed-82dc-4aa7-bf97-cdd18a18c1a9","deparmentCode":"01010102","deparmentName":"城市经理","logisticsId":null,"logisticsCode":null,"logisticsName":null,"realLogisticsCompanyId":null,"realLogisticsCompanyCode":null,"realLogisticsCompanyName":null,"logisticsBillCode":null,"siger":null,"signTime":null,"cancelReason":null,"remark":"自动化测试参照调拨出库单新增调拨入库单","transferInBillItems":[{"id":"0Z8SQSmZtDN7o4b5u7I8","dr":0,"ts":1589012723000,"creator":"smq","creationTime":1589012723000,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":null,"transferInBillId":null,"rowNum":10,"goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","goodsCode":"301020000049","goodsName":"小雅AI音箱旗舰版_石墨绿","goodsFullName":null,"goodsBasicUnitName":"个","goodsAssistUnitName":"个","goodsConversionRate":1.000000,"enableBatchNumberManage":null,"productId":null,"productLineId":null,"isOptional":null,"unitId":"UNIT-12","unitCode":"EA","unitName":"个","shouldInNum":5.00000000,"factInNum":3.00000000,"unitPrice":null,"amountMoney":0E-8,"batchNumId":null,"batchNumCode":null,"batchNumName":null,"goodsPositionId":null,"goodsPositionCode":null,"goodsPositionName":null,"stockInPersonId":null,"stockInPersonCode":null,"stockInPersonName":null,"stockInDate":null,"firstBillCode":"DBO20200508000034","firstBillBcode":"0Tr6HVsgvmzwBQYy2d6i","firstBillType":null,"srcBillCode":"TDN2020050900003","srcBillBcode":"0RVbhbtQZhT5PZkp19zW","srcBillType":"AllocationOut","remark":null,"goodsVersion":"1","goodsSelection":null,"isMotherPiece":null,"customerId":null,"customerCode":null,"customerName":null,"supplierId":null,"supplierCode":null,"supplierName":null,"projectId":null,"projectCode":null,"projectName":null,"batchCodeId":null,"batchCodeCode":null,"stockStateId":null,"stockStateCode":null,"stockStateName":null,"enableBatchNoManage":null,"enableInvStatusManage":null,"originalGoodsId":null,"goodsSelectionDescription":null,"ext01":null,"ext02":null,"ext03":"AllocationOut","ext04":"Allocation","ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":"0TszFCIVqcbJkmpWHQhq","ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null}],"transferInBillItemBoms":[{"id":"0P13ZigHlYHvTIuUCTj1","dr":0,"ts":1589012723000,"creator":"smq","creationTime":1589012723000,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":null,"rowNum":"10","goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","goodsCode":"301020000049","goodsName":"小雅AI音箱旗舰版_石墨绿","goodsFullName":null,"goodsBasicUnitName":"个","goodsAssistUnitName":"个","goodsConversionRate":1.000000,"enableBatchNumberManage":null,"productId":null,"productLineId":null,"unitId":"UNIT-12","unitCode":"EA","unitName":"个","shouldInNum":5.00000000,"factInNum":3.00000000,"unitPrice":null,"amountMoney":0E-8,"batchNumId":null,"batchNumCode":null,"batchNumName":null,"goodsPositionId":null,"goodsPositionCode":null,"goodsPositionName":null,"stockInPersonId":null,"stockInPersonCode":null,"stockInPersonName":null,"stockInDate":null,"firstBillCode":"0DKeeV9TPwv3UZiad8EH","firstBillBcode":"0Tr6HVsgvmzwBQYy2d6i","firstBillType":null,"srcBillCode":"TDN2020050900003","srcBillBcode":"0RVbhbtQZhT5PZkp19zW","srcBillType":null,"remark":null,"goodsVersion":"1","goodsSelection":null,"customerId":null,"customerCode":null,"customerName":null,"supplierId":null,"supplierCode":null,"supplierName":null,"projectId":null,"projectCode":null,"projectName":null,"batchCodeId":null,"batchCodeCode":null,"stockStateId":null,"stockStateCode":null,"stockStateName":null,"originalGoodsId":null,"goodsSelectionDescription":null,"itemId":"0Z8SQSmZtDN7o4b5u7I8","billId":null,"parentGoodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","parentGoodsCode":"301020000049","parentGoodsName":"小雅AI音箱旗舰版_石墨绿","parentGoodsdisplayName":null,"parentRowNum":"10","childGoodsQty":null,"firstBillBomCode":"0CrhvlIZ5uIVEXmYN9Hq","srcBillBomCode":"0K1xchlRSFmYGxaooi2J","ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":"0TszFCIVqcbJkmpWHQhq","ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null}],"srcSystem":null,"srcSystemId":null,"srcSystemCode":null,"srcSystemName":null,"ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null,"sycnOutStatus":null,"sycnNCStatus":null}', 'User': 'Manager', 'DependCase': '', 'RelevanceList': '', 'Sql': '', 'IsDepend': 'Yes'}
    code=200
    response= {'id': '0cjdm7rc2DCJpzCGnyBl', 'dr': 0, 'ts': 1589168834000, 'creator': 'smq', 'creationTime': 1589168834000, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm', 'promptMessage': '', 'stockOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9', 'stockOrgCode': '1210', 'stockOrgName': '西安喜马拉雅网络科技有限公司', 'stockOrgInId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9', 'stockOrgInCode': '1210', 'stockOrgInName': '西安喜马拉雅网络科技有限公司', 'billCode': 'TRN2020051100001', 'billDate': 1588953600000, 'billType': 'AllocationIn', 'billTranTypeId': 'AllocationIn', 'billTranTypeCode': 'AllocationIn', 'billTranTypeName': '调拨入库', 'storageId': '1001ZZ100000000DPAP6', 'storageCode': 'test030202', 'storageName': 'test030202', 'ifSlotManage': None, 'outStorageId': '1001ZZ100000000DPAP4', 'outStorageCode': 'test030201', 'outStorageName': '测试仓库030201', 'outIfSlotManage': None, 'storekeeperId': None, 'storekeeperCode': None, 'storekeeperName': None, 'inDate': None, 'planArriveDate': None, 'currencyId': None, 'currencyCode': None, 'currencyName': None, 'totalShouldInNum': 5.0, 'totalFactInNum': 3.0, 'billStatusId': '099aj5df-4y42-4700-d8d6-3714fdb43e68', 'billStatusCode': '01', 'billStatusName': '自由', 'stockBillBelong': '0DKeeV9TPwv3UZiad8EH', 'customerId': None, 'customerCode': None, 'customerName': None, 'bizPersonId': None, 'bizPersonCode': None, 'bizPersonName': None, 'deparmentId': 'ae96b9ed-82dc-4aa7-bf97-cdd18a18c1a9', 'deparmentCode': '01010102', 'deparmentName': '城市经理', 'logisticsId': None, 'logisticsCode': None, 'logisticsName': None, 'realLogisticsCompanyId': None, 'realLogisticsCompanyCode': None, 'realLogisticsCompanyName': None, 'logisticsBillCode': None, 'siger': None, 'signTime': None, 'cancelReason': None, 'remark': '自动化测试参照调拨出库单新增调拨入库单', 'transferInBillItems': [{'id': '0b3rotjZ5h24dy7GDM1F', 'dr': 0, 'ts': 1589168836000, 'creator': 'smq', 'creationTime': 1589168836000, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm', 'promptMessage': None, 'transferInBillId': None, 'rowNum': 10, 'goodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'goodsCode': '301020000049', 'goodsName': '小雅AI音箱旗舰版_石墨绿', 'goodsFullName': None, 'goodsBasicUnitName': '个', 'goodsAssistUnitName': '个', 'goodsConversionRate': 1.0, 'enableBatchNumberManage': None, 'productId': None, 'productLineId': None, 'isOptional': None, 'unitId': 'UNIT-12', 'unitCode': 'EA', 'unitName': '个', 'shouldInNum': 5.0, 'factInNum': 3.0, 'unitPrice': None, 'amountMoney': 0.0, 'batchNumId': None, 'batchNumCode': None, 'batchNumName': None, 'goodsPositionId': None, 'goodsPositionCode': None, 'goodsPositionName': None, 'stockInPersonId': None, 'stockInPersonCode': None, 'stockInPersonName': None, 'stockInDate': None, 'firstBillCode': 'DBO20200508000034', 'firstBillBcode': '0Tr6HVsgvmzwBQYy2d6i', 'firstBillType': None, 'srcBillCode': 'TDN2020050900003', 'srcBillBcode': '0RVbhbtQZhT5PZkp19zW', 'srcBillType': 'AllocationOut', 'remark': None, 'goodsVersion': '1', 'goodsSelection': None, 'isMotherPiece': None, 'customerId': None, 'customerCode': None, 'customerName': None, 'supplierId': None, 'supplierCode': None, 'supplierName': None, 'projectId': None, 'projectCode': None, 'projectName': None, 'batchCodeId': None, 'batchCodeCode': None, 'stockStateId': None, 'stockStateCode': None, 'stockStateName': None, 'enableBatchNoManage': None, 'enableInvStatusManage': None, 'originalGoodsId': None, 'goodsSelectionDescription': None, 'ext01': None, 'ext02': None, 'ext03': 'AllocationOut', 'ext04': 'Allocation', 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': '0TszFCIVqcbJkmpWHQhq', 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None}], 'transferInBillItemBoms': [{'id': '0SGl6SIsXZ647Za44Jvl', 'dr': 0, 'ts': 1589168836000, 'creator': 'smq', 'creationTime': 1589168836000, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm', 'promptMessage': None, 'rowNum': '10', 'goodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'goodsCode': '301020000049', 'goodsName': '小雅AI音箱旗舰版_石墨绿', 'goodsFullName': None, 'goodsBasicUnitName': '个', 'goodsAssistUnitName': '个', 'goodsConversionRate': 1.0, 'enableBatchNumberManage': None, 'productId': None, 'productLineId': None, 'unitId': 'UNIT-12', 'unitCode': 'EA', 'unitName': '个', 'shouldInNum': 5.0, 'factInNum': 3.0, 'unitPrice': None, 'amountMoney': 0.0, 'batchNumId': None, 'batchNumCode': None, 'batchNumName': None, 'goodsPositionId': None, 'goodsPositionCode': None, 'goodsPositionName': None, 'stockInPersonId': None, 'stockInPersonCode': None, 'stockInPersonName': None, 'stockInDate': None, 'firstBillCode': '0DKeeV9TPwv3UZiad8EH', 'firstBillBcode': '0Tr6HVsgvmzwBQYy2d6i', 'firstBillType': None, 'srcBillCode': 'TDN2020050900003', 'srcBillBcode': '0RVbhbtQZhT5PZkp19zW', 'srcBillType': None, 'remark': None, 'goodsVersion': '1', 'goodsSelection': None, 'customerId': None, 'customerCode': None, 'customerName': None, 'supplierId': None, 'supplierCode': None, 'supplierName': None, 'projectId': None, 'projectCode': None, 'projectName': None, 'batchCodeId': None, 'batchCodeCode': None, 'stockStateId': None, 'stockStateCode': None, 'stockStateName': None, 'originalGoodsId': None, 'goodsSelectionDescription': None, 'itemId': '0b3rotjZ5h24dy7GDM1F', 'billId': None, 'parentGoodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'parentGoodsCode': '301020000049', 'parentGoodsName': '小雅AI音箱旗舰版_石墨绿', 'parentGoodsdisplayName': None, 'parentRowNum': '10', 'childGoodsQty': None, 'firstBillBomCode': '0CrhvlIZ5uIVEXmYN9Hq', 'srcBillBomCode': '0K1xchlRSFmYGxaooi2J', 'ext01': None, 'ext02': None, 'ext03': None, 'ext04': None, 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': '0TszFCIVqcbJkmpWHQhq', 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None}], 'srcSystem': None, 'srcSystemId': None, 'srcSystemCode': None, 'srcSystemName': None, 'ext01': None, 'ext02': None, 'ext03': None, 'ext04': None, 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None, 'sycnOutStatus': None, 'sycnNCStatus': None}

    check_result(casedata,code,response)
