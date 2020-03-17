import json
import setupMain
from log import Log
log=Log()
json_path=setupMain.json_result_path

def write_result(fileName,result):
    code=result[0]
    response=result[1]
    if code==0:
        with open(json_path+fileName+'_result.', "w") as f:
            json.dump(response, f)
            print("加载入文件完成...")
    else:
        log.error('HTTP状态码错误，无需保留测试结果')
# data= {'id': '0o5cTyda4WixroJr61XE', 'dr': 0, 'ts': 1584349803336, 'creator': None, 'creationTime': 1584349803336, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm', 'promptMessage': None, 'state': 0, 'approver': None, 'approveTime': None, 'approveOpinion': None, 'sycnNCStatus': None, 'sycnOutStatus': None, 'saleOrgId': 'e53fc87e-1a16-4a2b-978c-63bfd14fd88b', 'saleOrgCode': '1101', 'saleOrgName': '上海证大喜马拉雅网络科技有限公司', 'supplierId': None, 'supplierCode': None, 'supplierName': None, 'receiveCustomerId': 'a3456c3b-edaa-4cf8-8dff-29ddc68d0749', 'receiveCustomerCode': '10001621', 'receiveCustomerName': '贵州喜马拉雅网络科技有限公司', 'contractId': None, 'contractCode': None, 'contractName': None, 'settleFinancialOrgId': None, 'settleFinancialOrgCode': None, 'settleFinancialOrgName': None, 'sameFinancialOrg': False, 'orderTypeId': '0yDZwkYyas4KNNKM4RNF', 'orderTypeCode': '30-Cxx-02', 'orderTypeName': '先货后款', 'billTypeId': 'SaleOrder', 'billTypeCode': 'SaleOrder', 'billTypeName': '销售订单', 'costTypeId': None, 'costTypeCode': None, 'costTypeName': None, 'saleModel': '01', 'orderCode': 'SOO20200316000009', 'orderDate': 1584186535007, 'orderStatusId': '42c874d4-a9f0-4104-9342-4a2cd8c4a600', 'orderStatusCode': '01', 'orderStatusName': '待处理', 'customerId': 'a3456c3b-edaa-4cf8-8dff-29ddc68d0749', 'customerCode': '10001621', 'customerName': '贵州喜马拉雅网络科技有限公司', 'marketAreaId': None, 'marketAreaCode': None, 'marketAreaName': None, 'salesManagerId': '8e73d0b7-5d0e-4c9d-bcdb-1db337b0b971', 'salesManagerCode': '3527', 'salesManagerName': '诸佳艺', 'salesDeptId': '1d5f2aff-5455-4e40-8818-d0e2bbc7e37a', 'salesDeptCode': '01010101', 'salesDeptName': '区域招商', 'transportModeId': None, 'transportModeCode': None, 'transportModeName': None, 'settleModeId': None, 'settleModeCode': None, 'settleModeName': None, 'deliveryDate': 1584186535002, 'totalNum': 5.0, 'currencyId': '7cbc1420-737d-4206-97e3-140ebdbe841f', 'currencyCode': 'CNY', 'currencyName': '人民币', 'currencyPriceScale': None, 'currencyAmountScale': None, 'totalDealAmount': 13445.0, 'totalAmount': 13445.0, 'promAmount': None, 'offsetAmount': None, 'totalWeight': 0.0, 'totalNetWeight': 0.0, 'totalVolume': 0.0, 'orderSource': '02', 'isClose': 0, 'closer': None, 'closeTime': None, 'isDeClose': 0, 'deCloser': None, 'deCloseTime': None, 'closeReason': None, 'remark': None, 'rejecter': None, 'rejectTime': None, 'rejectReason': None, 'srcOrderCode': None, 'srcOrderId': None, 'srcReqOrderCode': None, 'srcReqOrderId': None, 'orderReceiveAddress': {'id': '09xrge8O9XlDsbu1T8v3', 'dr': 0, 'ts': 1584349803342, 'creator': None, 'creationTime': 1584349803342, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm', 'promptMessage': None, 'orderId': '0o5cTyda4WixroJr61XE', 'receiveAddressId': 'a8188818-435b-4f9b-bc26-ff98a5bca778', 'receiver': '黎阳', 'receiverTel': '', 'receiverPhone': '19979010823', 'country': '中国', 'countryId': 'COUNTRY-01', 'receiverProvince': '贵州省', 'receiverProvinceId': '52', 'receiverCity': '贵阳市', 'receiverCityId': '520100000000', 'receiverCounty': '观山湖区', 'receiverCountyId': '520115000000', 'receiverTown': '世纪城社区服务中心', 'receiverTownId': '520115400000', 'receiverAddress': '长岭南路33号天一国际10栋902', 'receiverZipcode': None}, 'orderInvoice': {'id': '085fL89FWdE4ZGVtUMTB', 'dr': 0, 'ts': 1584349803342, 'creator': None, 'creationTime': 1584349803342, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm', 'promptMessage': None, 'orderId': '0o5cTyda4WixroJr61XE', 'invoiceId': 'f0d8b999-8614-464a-8e50-32e2e69fbfe5', 'invoiceType': '增值税发票', 'invoiceContent': None, 'invoiceTitle': '贵州喜马拉雅网络科技有限公司', 'invoiceTaxId': None, 'invoiceBank': '中国建设银行股份有限公司贵阳城北支行', 'invoiceAccount': None, 'invoiceSubBank': None}, 'orderReceiveAddressStr': None, 'orderInvoiceStr': None, 'orderItems': [{'id': '08POT1aOmukoo42nJ0Ez', 'dr': 0, 'ts': 1584349803341, 'creator': None, 'creationTime': 1584349803341, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm', 'promptMessage': None, 'orderId': '0o5cTyda4WixroJr61XE', 'orderCode': 'SOO20200316000009', 'orderBillType': 'SaleOrder', 'customerId': 'a3456c3b-edaa-4cf8-8dff-29ddc68d0749', 'customerName': None, 'rowNum': '20', 'productId': '996cc839-60e8-4500-82c6-9a7c7b95646d', 'goodsCategoryId': None, 'goodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'goodsCode': '301020000049', 'goodsName': '小雅AI音箱旗舰版_石墨绿', 'goodsDisplayName': '小雅AI音箱旗舰版_石墨绿', 'goodsImg': '/group1/M00/00/00/rBFAIV0wmbyASJn2AAE4-1jmRp4811.jpg', 'productLineId': '13c512df-ad18-48e5-b75d-166a534cc410', 'rowWeight': 0, 'weight': None, 'rowNetWeight': 0, 'netWeight': None, 'weightUnitId': None, 'weightUnitCode': None, 'weightUnitName': None, 'rowVolume': 0, 'volume': None, 'volumeUnitId': None, 'volumeUnitCode': None, 'volumeUnitName': None, 'orderNum': 5.0, 'orderNumUnitId': 'UNIT-12', 'orderNumUnitCode': 'EA', 'orderNumUnitName': '个', 'mainNum': 5, 'mainNumUnitId': 'UNIT-12', 'mainNumUnitCode': 'EA', 'mainNumUnitName': '个', 'conversionRate': 1.0, 'basePrice': 2789.0, 'supplierPrice': None, 'salePrice': 2689.0, 'promPrice': 2689.0, 'dealPrice': 2689.0, 'amount': 13445.0, 'promAmount': None, 'offsetAmount': None, 'dealAmount': 13445.0, 'currencyId': '7cbc1420-737d-4206-97e3-140ebdbe841f', 'currencyCode': 'CNY', 'currencyName': '人民币', 'currencySign': None, 'currencyAmountScale': None, 'currencyPriceScale': None, 'isGift': 0, 'logisticsId': None, 'logisticsCode': None, 'logisticsName': None, 'promotinId': None, 'promotinCode': None, 'promotinName': None, 'planDeliveryDate': 1584187053281, 'deliveryInvOrgId': 'ebcd635d-237e-4a15-819c-3983ac49436f', 'deliveryInvOrgCode': '1302', 'deliveryInvOrgName': '上海喜日电子科技有限公司', 'deliveryWarehouseId': None, 'deliveryWarehouseCode': None, 'deliveryWarehouseName': None, 'isClose': 0, 'isDeClose': 0, 'remark': None, 'deliveryNum': 0, 'stockInNum': 0, 'stockOutNum': 0, 'returnNum': 0, 'refundNum': 0, 'signNum': 0, 'replenishNum': 0, 'coordinateNum': 0, 'srcOrderCode': None, 'srcOrderId': None, 'srcOrderItemId': None, 'srcOrderTrantypeId': None, 'srcOrderBilltypeId': None, 'srcReqOrderCode': None, 'srcReqOrderId': None, 'srcReqOrderItemId': None, 'totalReturnAmount': None, 'returnReasonId': None, 'returnReasonCode': None, 'returnReasonName': None, 'returnTypeId': None, 'returnTypeCode': None, 'returnTypeName': None, 'orderPromRels': [], 'orderAttachments': [], 'version': 1, 'originalGoodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'settleFinancialOrgId': 'e53fc87e-1a16-4a2b-978c-63bfd14fd88b', 'settleFinancialOrgCode': '1101', 'settleFinancialOrgName': '上海证大喜马拉雅网络科技有限公司', 'projectId': None, 'projectCode': None, 'projectName': None, 'baseGoodsOptId': None, 'baseGoodsOptValue': None, 'supplierId': None, 'supplierCode': None, 'supplierName': None, 'batchCodeId': None, 'batchCodeCode': None, 'batchCodeName': None, 'goodsSupplement': 0, 'srcContractId': None, 'srcContractCode': None, 'srcContractType': None, 'srcQuoteId': None, 'goodsSupplementPrice': None, 'offsetDetailsDtoList': [], 'existingNum': None, 'availableNum': None, 'closeReason': None, 'orderCorrelationMoney': None, 'ext01': None, 'ext02': None, 'ext03': None, 'ext04': None, 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None, 'bomSplit': None}], 'orderItemBoms': [{'id': '0muX2y3SkvIXeCRFi7XA', 'dr': 0, 'ts': 1584349803342, 'creator': None, 'creationTime': 1584349803342, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm', 'promptMessage': None, 'orderId': '0o5cTyda4WixroJr61XE', 'orderItemId': '08POT1aOmukoo42nJ0Ez', 'parentRowNum': '20', 'parentGoodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'parentGoodsCode': '301020000049', 'parentGoodsName': '小雅AI音箱旗舰版_石墨绿', 'rowNum': '20', 'goodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'goodsCode': '301020000049', 'goodsName': '小雅AI音箱旗舰版_石墨绿', 'goodsImg': '/group1/M00/00/00/rBFAIV0wmbyASJn2AAE4-1jmRp4811.jpg', 'isGift': 0, 'productLineId': '13c512df-ad18-48e5-b75d-166a534cc410', 'rowWeight': 0, 'weight': None, 'rowNetWeight': 0, 'netWeight': None, 'weightUnitId': None, 'weightUnitCode': None, 'weightUnitName': None, 'rowVolume': 0, 'volume': None, 'volumeUnitId': None, 'volumeUnitCode': None, 'volumeUnitName': None, 'orderNum': 5.0, 'orderNumUnitId': 'UNIT-12', 'orderNumUnitCode': 'EA', 'orderNumUnitName': '个', 'mainNum': 5.0, 'mainNumUnitId': 'UNIT-12', 'mainNumUnitCode': 'EA', 'mainNumUnitName': '个', 'conversionRate': 1.0, 'basePrice': None, 'salePrice': 2689.0, 'amount': 13445.0, 'dealPrice': 2689.0, 'dealAmount': 13445.0, 'currency': None, 'planDeliveryDate': 1584187053000, 'deliveryInvOrgId': 'ebcd635d-237e-4a15-819c-3983ac49436f', 'deliveryWarehouseId': None, 'baseGoodsOptId': None, 'baseGoodsOptVals': None, 'baseGoodsOptValue': None, 'version': 1, 'originalGoodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'childGoodsQty': 1, 'projectId': None, 'supplierId': None, 'srcOrderCode': None, 'srcOrderId': None, 'srcOrderItemId': None, 'srcOrderItemBomId': None, 'srcReqOrderCode': None, 'goodsSupplement': 0, 'srcReqOrderId': None, 'srcReqOrderItemId': None, 'srcReqOrderItemBomId': None, 'existingNum': None, 'ext01': None, 'ext02': None, 'ext03': None, 'ext04': None, 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None, 'deliveryInvOrgCode': None, 'deliveryInvOrgName': None, 'deliveryWarehouseCode': None, 'deliveryWarehouseName': None, 'goodsSupplementPrice': None, 'costPrice': None, 'supplierPrice': None, 'supplierCode': None, 'supplierName': None, 'logisticsId': None, 'logisticsCode': None, 'logisticsName': None, 'deliveryNum': None, 'stockInNum': None, 'stockOutNum': None, 'returnNum': None, 'refundNum': None, 'signNum': None, 'replenishNum': None, 'coordinateNum': None, 'isClose': 0, 'closeReason': None, 'isDeClose': 0, 'isOutClose': None, 'offsetAmount': None, 'settleFinancialOrgId': 'e53fc87e-1a16-4a2b-978c-63bfd14fd88b', 'settleFinancialOrgCode': '1101', 'settleFinancialOrgName': '上海证大喜马拉雅网络科技有限公司', 'remark': None}], 'orderPromRels': [], 'orderAttachments': [], 'logisticsId': None, 'logisticsCode': None, 'logisticsName': None, 'logisticsBillCode': None, 'originalOrderCode': None, 'totalReturnAmount': None, 'returnReasonId': None, 'returnReasonCode': None, 'returnReasonName': None, 'accountPeriodId': 'a1ee592c-4412-42dc-8cee-94d2ac8aa355', 'accountPeriodCode': '001', 'accountPeriodName': '001', 'superiorCustomerId': None, 'superiorCustomerCode': None, 'superiorCustomerName': None, 'totalGoodsSuppleAmount': 0.0, 'orderCorrelationMoney': None, 'flushSelected': [], 'contractTypeId': None, 'ext01Id': None, 'ext01Code': None, 'ext01Name': None, 'ext02Id': None, 'ext02Code': None, 'ext02Name': None, 'ext03': None, 'ext04': None, 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None, 'goodsOutStyleId': None, 'goodsOutStyleCode': None, 'goodsOutStyleName': None, 'isBomCalcPrice': None, 'underPaymentModeId': None, 'underPaymentModeCode': None, 'underPaymentModeName': None}
# name='create_sales_order_result.json'
# write_result(name,data)