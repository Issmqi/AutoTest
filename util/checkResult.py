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
                        return False
                    else:
                        log.info('JSON格式校验成功！')
                        return True
            else:
                log.info("HTTP返回状态码%s与预期%s不一致" % (str(code), str(case['ExpectedCode'])))
                return False
    else:
        log.error('校验类型不存在！')


if __name__ == '__main__':
    data = {'CaseId': 1, 'CaseName': 'create_common_purchase_order', 'APIName': '新增普通外部采购订单',
            'Headers': {'Content-Type': 'application/json', 'charset': 'UTF-8'},
            'Path': '/occ-purchase/purchase/orders', 'Method': 'post', 'ParameterType': 'json',
            'Params': {'code': None, 'state': 0, 'displayName': None, 'version': None, 'id': None,
                       'purchaseOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9', 'purchaseOrgName': None,
                       'orderCode': None, 'otherOrderNum': None, 'orderDate': 1584115200000,
                       'purchaseType': 'OuterPurchase', 'tranTypeId': 'GeneralPurchase', 'tranTypeName': None,
                       'tranTypeCode': 'GeneralPurchase', 'supplierId': '1001A910000000007A4O', 'selfLifing': '02',
                       'supplierName': None, 'supplierCode': '10000352', 'purchasePersonId': None,
                       'purchasePersonCode': None, 'purchasePersonName': None, 'purchaseDeptId': '0K1ovYvAl1Pk00oCRPjV',
                       'purchaseDeptName': None, 'purchaseDeptCode': None, 'totalGoodsNum': 6,
                       'totalAmountMoney': '6.00', 'currencyId': None, 'currencyName': None, 'status': '01',
                       'operationCode': None, 'approveStatus': '01', 'isClosed': '0', 'approvalSummary': None,
                       'erpStatus': None, 'refusedReason': None, 'confirmPerson': None, 'remark': None,
                       'isReturned': '0', 'returnedOrder': None, 'creator': None, 'creationTime': '', 'modifier': None,
                       'modifiedTime': '', 'ext15': None, 'ext14': None, 'ext13': None, 'ext12': None, 'ext11': '0',
                       'planArrivalDate': '', 'demandStockOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9',
                       'arrivalBelongCode': '01', 'receiveStorageOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9',
                       'receiveStorageId': '0bxYF73VWxwqf6bb3ib4', 'customerId': None, 'receiveContact': None,
                       'receiveContactPhone': None, 'demandStockOrgName': None, 'arrivalBelongName': None,
                       'receiveStorageOrgName': None, 'receiveStorageName': None, 'customerName': None,
                       'persistStatus': 'new', 'orderItems': [
                    {'rowNum': 10, 'goodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'goodsName': '小雅AI音箱旗舰版_石墨绿',
                     'goodsCode': '301020000049', 'unitId': 'UNIT-12', 'unitCode': 'EA', 'unitName': '个',
                     'goodsNum': '6.000000', 'unitPrice': '1.00000000', 'amountMoney': '6.00', 'isGift': '0',
                     'goodsSelection': None, 'goodsVersion': '1', 'projectId': None, 'projectCode': None,
                     'projectName': None, 'sourceType': None, 'sourceId': None, 'sourceLineNum': None, 'isClosed': '0',
                     'stockStatus': '01', 'payStatus': None, 'arrivalBelongId': None, 'arrivalBelongName': None,
                     'arrivalBelongCode': '01', 'demandStockOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9',
                     'demandStockOrgName': None, 'demandStockOrgCode': None,
                     'receiveStorageOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9', 'receiveStorageOrgName': None,
                     'receiveStorageOrgCode': None, 'receiveStorageId': '0bxYF73VWxwqf6bb3ib4',
                     'receiveStorageName': None, 'receiveStorageCode': None, 'customerId': None, 'customerCode': None,
                     'customerName': None, 'countryId': None, 'countryName': None, 'countryCode': None,
                     'provinceId': None, 'provinceName': None, 'provinceCode': None, 'cityId': None, 'cityName': None,
                     'cityCode': None, 'districtId': None, 'districtName': None, 'districtCode': None, 'townId': None,
                     'townName': None, 'townCode': None, 'receiveContact': None, 'receiveContactPhone': None,
                     'receiveAddress': None, 'detailAddr': None, 'addStorageAmount': None, 'returnGoodsAmount': None,
                     'baseGoodsOptId': None, 'isOptional': None, 'name': None, 'productid': None, 'productidCode': None,
                     'productidName': None, 'productidStandardName': None, 'productidSaleSeriesId': None,
                     'productidSaleSeriesName': None, 'num': None, 'dr': None, 'creator': None, 'creationTime': '',
                     'modifier': None, 'modifiedTime': '', 'originalGoodsId': None, 'goodsSelectionDescription': None,
                     'batchCode': None, 'ext06': '0', 'ext07': None, 'ext08': None, 'outerStock': None,
                     'srcBillCode': None, 'srcBillBcode': None, 'srcBillType': None, 'ext01': '6.00000000',
                     'ext02': 'UNIT-12', 'ext03': 'EA', 'ext04': '个', 'ext05': '1.00', 'ext09': '1.00000000',
                     'ext13': None, 'ext12': None, 'ext10': None, 'persistStatus': 'new'}], 'orderItemBoms': [
                    {'rowNum': 10, 'goodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'goodsName': '小雅AI音箱旗舰版_石墨绿',
                     'goodsCode': '301020000049', 'unitId': 'UNIT-12', 'unitCode': 'EA', 'unitName': '个',
                     'goodsNum': '6.000000', 'unitPrice': '1.00000000', 'amount': None, 'amountMoney': '6.00',
                     'isGift': '0', 'sourceType': None, 'sourceId': None, 'sourceLineNum': None, 'isClosed': '0',
                     'stockStatus': None, 'payStatus': None, 'arrivalBelongId': None, 'arrivalBelongName': None,
                     'arrivalBelongCode': '01', 'demandStockOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9',
                     'demandStockOrgName': None, 'demandStockOrgCode': None,
                     'receiveStorageOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9', 'receiveStorageOrgName': None,
                     'receiveStorageOrgCode': None, 'receiveStorageId': '0bxYF73VWxwqf6bb3ib4',
                     'receiveStorageName': None, 'receiveStorageCode': None, 'customerId': None, 'customerCode': None,
                     'customerName': None, 'countryId': None, 'countryName': None, 'countryCode': None,
                     'provinceId': None, 'provinceName': None, 'provinceCode': None, 'cityId': None, 'cityName': None,
                     'cityCode': None, 'districtId': None, 'districtName': None, 'districtCode': None, 'townId': None,
                     'townName': None, 'townCode': None, 'receiveContact': None, 'receiveContactPhone': None,
                     'receiveAddress': None, 'detailAddr': None, 'addStorageAmount': None, 'returnGoodsAmount': None,
                     'name': None, 'productid': None, 'productidCode': None, 'productidName': None,
                     'productidStandardName': None, 'productidSaleSeriesId': None, 'productidSaleSeriesName': None,
                     'dr': None, 'creator': None, 'creationTime': '', 'modifier': None, 'modifiedTime': '',
                     'goodsVersion': '1', 'goodsSelection': None, 'projectId': None, 'projectCode': None,
                     'projectName': None, 'parentGoodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749',
                     'parentGoodsCode': None, 'parentGoodsName': '小雅AI音箱旗舰版_石墨绿', 'parentRowNum': 10,
                     'childGoodsQty': None, 'originalGoodsId': None, 'goodsSelectionDescription': None,
                     'baseGoodsOptId': None, 'batchCode': None, 'isOptional': None, 'num': None, 'ext06': '0',
                     'ext07': None, 'ext08': None, 'outerStock': None, 'srcBillCode': None, 'srcBillBcode': None,
                     'srcBillType': None, 'ext01': None, 'ext02': 'UNIT-12', 'ext03': 'EA', 'ext04': '个',
                     'ext05': '1.00', 'ext09': None, 'ext13': None, 'ext12': None, 'ext10': None,
                     'persistStatus': 'new'}]}, 'CheckTpye': 'check_json', 'ExpectedCode': 200,
            'ExpectedData': {'id': '0C6XPUcrn27sQ3BYTPyV', 'dr': 0, 'ts': 1585190756000, 'creator': 'smq',
                             'creationTime': 1585190756000, 'modifier': None, 'modifiedTime': None,
                             'persistStatus': 'nrm', 'promptMessage': None, 'state': 0, 'approver': None,
                             'approveTime': None, 'approveOpinion': None, 'sycnNCStatus': None, 'sycnOutStatus': None,
                             'purchaseOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9', 'purchaseOrgCode': '1210',
                             'purchaseOrgName': '西安喜马拉雅网络科技有限公司', 'orderType': 'PurchaseBill',
                             'orderCode': 'OPO20200326000004', 'otherOrderNum': None, 'orderDate': 1584115200000,
                             'planArrivalDate': None, 'purchaseType': 'OuterPurchase',
                             'supplierId': '1001A910000000007A4O', 'supplierCode': '10000352',
                             'supplierName': '上海艾臣营销策划有限公司', 'purchasePersonId': None, 'purchasePersonCode': None,
                             'purchasePersonName': None, 'purchaseDeptId': '0K1ovYvAl1Pk00oCRPjV',
                             'purchaseDeptCode': '01010102', 'purchaseDeptName': '城市经理', 'totalGoodsNum': 6.0,
                             'totalAmountMoney': 6.0, 'currencyId': None, 'currencyCode': None, 'currencyName': None,
                             'status': '01', 'erpStatus': None, 'refusedReason': None, 'confirmPerson': None,
                             'remark': None, 'isReturned': 0, 'returnedOrder': None, 'payStatus': None, 'isClosed': 0,
                             'tranTypeId': 'GeneralPurchase', 'tranTypeCode': 'GeneralPurchase', 'tranTypeName': '普通采购',
                             'orderItems': [
                                 {'id': '0UFWTex3OyVVnJq7bGQf', 'dr': 0, 'ts': 1585190756000, 'creator': 'smq',
                                  'creationTime': 1585190756000, 'modifier': None, 'modifiedTime': None,
                                  'persistStatus': 'nrm', 'promptMessage': None, 'orderId': None, 'purchaseOrg': None,
                                  'orderType': None, 'orderCode': None, 'otherOrderNum': None, 'orderDate': None,
                                  'purchaseType': None, 'supplier': '1001A910000000007A4O', 'purchasePerson': None,
                                  'purchaseDept': '0K1ovYvAl1Pk00oCRPjV', 'totalAmount': None, 'totalMoney': None,
                                  'status': None, 'remark': None, 'orderPayStatus': None, 'rowNum': '10',
                                  'goodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'goodsCode': '301020000049',
                                  'goodsDisplayName': '小雅AI音箱旗舰版_石墨绿', 'goodsName': '小雅AI音箱旗舰版_石墨绿', 'isOptional': None,
                                  'unitId': 'UNIT-12', 'unitCode': 'EA', 'unitName': '个', 'goodsNum': 6.0,
                                  'unitPrice': 1.0, 'amountMoney': 6.0, 'srcBillType': None, 'srcBillId': None,
                                  'srcBillCode': None, 'srcBillBcode': None,
                                  'arrivalBelongId': '512ef9a1-cbb6-4f45-801f-251fb883078c', 'arrivalBelongCode': '01',
                                  'arrivalBelongName': '自有',
                                  'receiveStorageOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9',
                                  'receiveStorageOrgCode': '1210', 'receiveStorageOrgName': '西安喜马拉雅网络科技有限公司',
                                  'receiveStorageId': '0bxYF73VWxwqf6bb3ib4', 'receiveStorageCode': '2123445',
                                  'receiveStorageName': '曲江书城店仓', 'customerId': None, 'customerCode': None,
                                  'customerName': None, 'receiveAddress': None, 'addStorageAmount': None,
                                  'returnGoodsAmount': None, 'isClosed': 0, 'payStatus': None, 'isGift': 0,
                                  'countryId': None, 'countryCode': None, 'countryName': None, 'provinceId': None,
                                  'provinceCode': None, 'provinceName': None, 'cityId': None, 'cityCode': None,
                                  'cityName': None, 'districtId': None, 'districtCode': None, 'districtName': None,
                                  'townId': None, 'townCode': None, 'townName': None, 'receiveContact': None,
                                  'receiveContactPhone': None, 'purchaseOrderId': '0C6XPUcrn27sQ3BYTPyV',
                                  'demandStockOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9',
                                  'demandStockOrgCode': '1210', 'demandStockOrgName': '西安喜马拉雅网络科技有限公司',
                                  'couldOutNum': None, 'stockStatus': '01', 'detailAddr': None, 'batchCode': None,
                                  'projectId': None, 'projectCode': None, 'projectName': None, 'applyReturnNum': None,
                                  'ext13': None, 'ext01': '6.00000000', 'ext04': '个', 'ext05': '1.00',
                                  'ext02': 'UNIT-12', 'ext03': 'EA', 'ext06': '0', 'ext07': None, 'ext08': None,
                                  'ext09': '1.00000000', 'ext10': None, 'ext11': None, 'ext12': None, 'ext14': None,
                                  'ext15': None, 'goodsVersion': '1', 'goodsSpec': None, 'goodsModelNum': None,
                                  'openCloseReason': None, 'goodsSelection': None, 'isMotherPiece': None,
                                  'arrangeConts': None, 'originalGoodsId': None, 'goodsSelectionDescription': None}],
                             'ext01': None, 'ext02': None, 'ext03': None, 'ext04': None, 'ext05': None, 'ext06': None,
                             'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': '0', 'ext12': None,
                             'ext13': None, 'ext14': None, 'ext15': None, 'settlementModeId': None,
                             'settlementModeCode': None, 'settlementModeName': None, 'selfLifing': '02',
                             'orderItemBoms': [
                                 {'id': '0V7MVCu2k1m0ehAcgUnI', 'dr': 0, 'ts': 1585190756000, 'creator': 'smq',
                                  'creationTime': 1585190756000, 'modifier': None, 'modifiedTime': None,
                                  'persistStatus': 'nrm', 'promptMessage': None, 'rowNum': '10',
                                  'goodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'goodsCode': '301020000049',
                                  'goodsName': '小雅AI音箱旗舰版_石墨绿', 'goodsDisplayName': '小雅AI音箱旗舰版_石墨绿',
                                  'goodsBasicUnitName': '个', 'goodsAssistUnitName': '个', 'goodsConversionRate': 1.0,
                                  'enableBatchNumberManage': None, 'productId': None, 'productLineId': None,
                                  'goodsVersion': '1', 'goodsSelection': None, 'goodsNum': 6.0, 'unitPrice': 1.0,
                                  'amountMoney': 6.0, 'itemId': '0UFWTex3OyVVnJq7bGQf',
                                  'billId': '0C6XPUcrn27sQ3BYTPyV', 'srcBillId': None, 'srcBillCode': None,
                                  'srcBillBcode': None, 'srcBillType': None, 'firstBillCode': None,
                                  'firstBillBcode': None, 'firstBillType': None, 'isGift': 0, 'countryId': None,
                                  'countryCode': None, 'countryName': None, 'provinceId': None, 'provinceCode': None,
                                  'provinceName': None, 'cityId': None, 'cityCode': None, 'cityName': None,
                                  'districtId': None, 'districtCode': None, 'districtName': None, 'townId': None,
                                  'townCode': None, 'townName': None, 'receiveContact': None,
                                  'receiveContactPhone': None,
                                  'demandStockOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9',
                                  'demandStockOrgCode': '1210', 'demandStockOrgName': '西安喜马拉雅网络科技有限公司',
                                  'stockStatus': None, 'detailAddr': None, 'goodsSpec': None, 'goodsModelNum': None,
                                  'openCloseReason': None, 'parentGoodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749',
                                  'parentGoodsCode': '301020000049', 'parentGoodsName': '小雅AI音箱旗舰版_石墨绿',
                                  'displayName': None, 'parentRowNum': '10',
                                  'arrivalBelongId': '512ef9a1-cbb6-4f45-801f-251fb883078c', 'arrivalBelongCode': '01',
                                  'arrivalBelongName': '自有',
                                  'receiveStorageOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9',
                                  'receiveStorageOrgCode': '1210', 'receiveStorageOrgName': '西安喜马拉雅网络科技有限公司',
                                  'receiveStorageId': '0bxYF73VWxwqf6bb3ib4', 'receiveStorageCode': '2123445',
                                  'receiveStorageName': '曲江书城店仓', 'customerId': None, 'customerCode': None,
                                  'customerName': None, 'addStorageAmount': None, 'returnGoodsAmount': None,
                                  'unitId': 'UNIT-12', 'unitCode': 'EA', 'unitName': '个', 'batchCode': None,
                                  'goodsSelectionDescription': None, 'projectId': None, 'projectCode': None,
                                  'projectName': None, 'isClosed': 0, 'applyReturnNum': None, 'childGoodsQty': None,
                                  'ext01': None, 'ext02': 'UNIT-12', 'ext03': 'EA', 'ext04': '个', 'ext05': '1.00',
                                  'ext06': '0', 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None,
                                  'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None,
                                  'originalGoodsId': None, 'firstBillBomCode': None, 'srcBillBomCode': None}],
                             'coordinationOrderCode': None, 'isEc': None, 'otherOrders': []}, 'User': 'Manager',
            'DependCase': '', 'RelevanceList': ''}

    code = 200
    response = {'id': '0K9SCTelihLE8TNmhOhz', 'dr': 0, 'ts': 1589361584000, 'creator': 'smq',
                'creationTime': 1589361584000, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm',
                'promptMessage': None, 'state': 0, 'approver': None, 'approveTime': None, 'approveOpinion': None,
                'sycnNCStatus': None, 'sycnOutStatus': None, 'purchaseOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9',
                'purchaseOrgCode': '1210', 'purchaseOrgName': '西安喜马拉雅网络科技有限公司', 'orderType': 'PurchaseBill',
                'orderCode': 'OPO20200513000001', 'otherOrderNum': None, 'orderDate': 1584115200000,
                'planArrivalDate': None, 'purchaseType': 'OuterPurchase', 'supplierId': '1001A910000000007A4O',
                'supplierCode': '10000352', 'supplierName': '上海艾臣营销策划有限公司', 'purchasePersonId': None,
                'purchasePersonCode': None, 'purchasePersonName': None, 'purchaseDeptId': '0K1ovYvAl1Pk00oCRPjV',
                'purchaseDeptCode': '01010102', 'purchaseDeptName': '城市经理', 'totalGoodsNum': 6.0,
                'totalAmountMoney': 6.0, 'currencyId': None, 'currencyCode': None, 'currencyName': None, 'status': '01',
                'erpStatus': None, 'refusedReason': None, 'confirmPerson': None, 'remark': None, 'isReturned': 0,
                'returnedOrder': None, 'payStatus': None, 'isClosed': 0, 'tranTypeId': 'GeneralPurchase',
                'tranTypeCode': 'GeneralPurchase', 'tranTypeName': '普通采购', 'orderItems': [
            {'id': '0oRq9hXv7ea2rE1S6WwF', 'dr': 0, 'ts': 1589361584000, 'creator': 'smq',
             'creationTime': 1589361584000, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm',
             'promptMessage': None, 'orderId': None, 'purchaseOrg': None, 'orderType': None,
             'orderCode': 'OPO20200513000001', 'otherOrderNum': None, 'orderDate': None, 'purchaseType': None,
             'supplier': '1001A910000000007A4O', 'purchasePerson': None, 'purchaseDept': '0K1ovYvAl1Pk00oCRPjV',
             'totalAmount': None, 'totalMoney': None, 'status': None, 'remark': None, 'orderPayStatus': None,
             'rowNum': '10', 'goodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'goodsCode': '301020000049',
             'goodsDisplayName': '小雅AI音箱旗舰版_石墨绿', 'goodsName': '小雅AI音箱旗舰版_石墨绿', 'isOptional': None, 'unitId': 'UNIT-12',
             'unitCode': 'EA', 'unitName': '个', 'goodsNum': 6.0, 'unitPrice': 1.0, 'amountMoney': 6.0,
             'srcBillType': None, 'srcBillId': None, 'srcBillCode': None, 'srcBillBcode': None,
             'arrivalBelongId': '512ef9a1-cbb6-4f45-801f-251fb883078c', 'arrivalBelongCode': '01',
             'arrivalBelongName': '自有', 'receiveStorageOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9',
             'receiveStorageOrgCode': '1210', 'receiveStorageOrgName': '西安喜马拉雅网络科技有限公司',
             'receiveStorageId': '0bxYF73VWxwqf6bb3ib4', 'receiveStorageCode': '2123445',
             'receiveStorageName': '曲江书城店仓', 'customerId': None, 'customerCode': None, 'customerName': None,
             'receiveAddress': None, 'addStorageAmount': None, 'returnGoodsAmount': None, 'isClosed': 0,
             'payStatus': None, 'isGift': 0, 'countryId': None, 'countryCode': None, 'countryName': None,
             'provinceId': None, 'provinceCode': None, 'provinceName': None, 'cityId': None, 'cityCode': None,
             'cityName': None, 'districtId': None, 'districtCode': None, 'districtName': None, 'townId': None,
             'townCode': None, 'townName': None, 'receiveContact': None, 'receiveContactPhone': None,
             'purchaseOrderId': '0K9SCTelihLE8TNmhOhz', 'demandStockOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9',
             'demandStockOrgCode': '1210', 'demandStockOrgName': '西安喜马拉雅网络科技有限公司', 'couldOutNum': None,
             'stockStatus': '01', 'detailAddr': None, 'batchCode': None, 'projectId': None, 'projectCode': None,
             'projectName': None, 'applyReturnNum': None, 'ext13': None, 'ext01': '6.00000000', 'ext04': '个',
             'ext05': '1.00', 'ext02': 'UNIT-12', 'ext03': 'EA', 'ext06': '0', 'ext07': None, 'ext08': None,
             'ext09': '1.00000000', 'ext10': None, 'ext11': None, 'ext12': None, 'ext14': None, 'ext15': None,
             'goodsVersion': '1', 'goodsSpec': None, 'goodsModelNum': None, 'openCloseReason': None,
             'goodsSelection': None, 'isMotherPiece': None, 'arrangeConts': None, 'originalGoodsId': None,
             'goodsSelectionDescription': None}], 'ext01': None, 'ext02': None, 'ext03': None, 'ext04': None,
                'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': '0',
                'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None, 'settlementModeId': None,
                'settlementModeCode': None, 'settlementModeName': None, 'selfLifing': '02', 'orderItemBoms': [
            {'id': '0kPX898o6LJns1IrUD6Q', 'dr': 0, 'ts': 1589361584000, 'creator': 'smq',
             'creationTime': 1589361584000, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm',
             'promptMessage': None, 'rowNum': '10', 'goodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749',
             'goodsCode': '301020000049', 'goodsName': '小雅AI音箱旗舰版_石墨绿', 'goodsDisplayName': '小雅AI音箱旗舰版_石墨绿',
             'goodsBasicUnitName': '个', 'goodsAssistUnitName': '个', 'goodsConversionRate': 1.0,
             'enableBatchNumberManage': None, 'productId': None, 'productLineId': None, 'goodsVersion': '1',
             'goodsSelection': None, 'goodsNum': 6.0, 'unitPrice': 1.0, 'amountMoney': 6.0,
             'itemId': '0oRq9hXv7ea2rE1S6WwF', 'billId': '0K9SCTelihLE8TNmhOhz', 'srcBillId': None, 'srcBillCode': None,
             'srcBillBcode': None, 'srcBillType': None, 'firstBillCode': None, 'firstBillBcode': None,
             'firstBillType': None, 'isGift': 0, 'countryId': None, 'countryCode': None, 'countryName': None,
             'provinceId': None, 'provinceCode': None, 'provinceName': None, 'cityId': None, 'cityCode': None,
             'cityName': None, 'districtId': None, 'districtCode': None, 'districtName': None, 'townId': None,
             'townCode': None, 'townName': None, 'receiveContact': None, 'receiveContactPhone': None,
             'demandStockOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9', 'demandStockOrgCode': '1210',
             'demandStockOrgName': '西安喜马拉雅网络科技有限公司', 'stockStatus': None, 'detailAddr': None, 'goodsSpec': None,
             'goodsModelNum': None, 'openCloseReason': None, 'parentGoodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749',
             'parentGoodsCode': '301020000049', 'parentGoodsName': '小雅AI音箱旗舰版_石墨绿', 'displayName': None,
             'parentRowNum': '10', 'arrivalBelongId': '512ef9a1-cbb6-4f45-801f-251fb883078c', 'arrivalBelongCode': '01',
             'arrivalBelongName': '自有', 'receiveStorageOrgId': 'abd7cf79-511d-4307-9bbd-d288b18d0ef9',
             'receiveStorageOrgCode': '1210', 'receiveStorageOrgName': '西安喜马拉雅网络科技有限公司',
             'receiveStorageId': '0bxYF73VWxwqf6bb3ib4', 'receiveStorageCode': '2123445',
             'receiveStorageName': '曲江书城店仓', 'customerId': None, 'customerCode': None, 'customerName': None,
             'addStorageAmount': None, 'returnGoodsAmount': None, 'unitId': 'UNIT-12', 'unitCode': 'EA',
             'unitName': '个', 'batchCode': None, 'goodsSelectionDescription': None, 'projectId': None,
             'projectCode': None, 'projectName': None, 'isClosed': 0, 'applyReturnNum': None, 'childGoodsQty': None,
             'ext01': None, 'ext02': 'UNIT-12', 'ext03': 'EA', 'ext04': '个', 'ext05': '1.00', 'ext06': '0',
             'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': None, 'ext12': None, 'ext13': None,
             'ext14': None, 'ext15': None, 'originalGoodsId': None, 'firstBillBomCode': None, 'srcBillBomCode': None}],
                'coordinationOrderCode': None, 'isEc': None, 'otherOrders': [], 'mailSendStatus': None,
                'mailSendStatusName': None, 'mailSendMsg': None}

    check_result(data, code, response)
