# -*- coding: utf-8 -*-
from log import Log
import allure
import json
import pytest

log=Log()


flag=True
def check_json(src_data,res_data):
    '''
    校验返回json格式是否和预期一致
    :param src_data: 校验数据
    :param res_data: 接口返回数据
    :return:
    '''

    global flag


    if isinstance(src_data,dict):

        for key in src_data:
            # print('flag是', flag)
            if not flag:
                return False
            if key not in res_data:
                log.info("JSON格式校验，关键字%s不在返回结果%s中" % (key, res_data))
                flag=False

                # raise Exception("JSON格式校验，关键字%s不在返回结果%s中" % (key, res_data))
            else:
                this_key=key
                if isinstance(src_data[this_key],dict) and isinstance(res_data[this_key],dict):
                    check_json(src_data[this_key],res_data[this_key])#递归执行check_json

                elif type(src_data[this_key]) !=type(res_data[this_key]):
                    log.info("json格式校验，校验关键字%s与返回关键字%s类型不一致"%(src_data[this_key],res_data[this_key]))
                    flag=False
                    # return flag
                    # raise Exception("json格式校验，校验关键字%s与返回关键字%s类型不一致"%(src_data[this_key],res_data[this_key]))
                else:
                    # print('%s校验通过'%this_key)
                    pass

    else:

        log.error("json校验数据不是dict类型")
        return False
        # raise Exception("json校验数据非dict类型")

def check_result(case,code,res_data):
    '''

    :param case: 用例数据
    :param code: 接口返回 HTTP状态码
    :param res_data: 接口返回数据
    :return:
    '''
    check_type=case['CheckTpye']

    if check_type=='no_check':
        with allure.step('接口无需校验'):
            return True
    elif check_type=='only_check_status':
        with allure.step('接口仅校验HTTP状态码'):
            allure.attach('预期code是', int(case['ExpectedCode']))
            allure.attach('实际code是', str(code))
            allure.attach('实际data是', str(res_data))
        if code==int(case['ExpectedCode']):
            log.info("HTTP状态码校验通过！")
            return True
        else:
            log.info(("HTTP返回状态码与预期不一致"))
            # raise Exception("HTTP返回状态码与预期不一致")
            return False

    elif check_type=='check_json':
        with allure.step("校验返回json数据结构"):
            allure.attach('预期code是', int(case['ExpectedCode']))
            allure.attach('实际code是', str(code))
            allure.attach('预期data是', str(case['ExpectedData']))
            allure.attach('实际data是', str(res_data))
            if code==int(case['ExpectedCode']):
                if not res_data:#判断res_data为None,  False, 空字符串"", 0, 空列表[], 空字典{}, 空元组()
                    res_data='{}'
                else:
                    expected_data_dict=json.loads(case['ExpectedData'])
                    result=check_json(expected_data_dict,res_data)
                    if result==False:
                        log.info('JSON格式校验失败！')
                        return False
                    else:
                        log.info('JSON格式校验成功！')
                        return True
            else:
                # raise Exception("HTTP返回状态码与预期不一致")
                log.info("HTTP返回状态码%s与预期%s不一致" %(str(code),int(case['ExpectedCode'])))
                return False
    else:
        log.error('校验类型不存在！')


# case={'CaseId': 1.0, 'Designer': '师孟奇', 'CaseName': '新增销售订单', 'APIName': '2B订单', 'Headers': "{'Content-Type':'application/json','charset': 'UTF-8'}", 'Path': '/occ-b2b-order/b2b/order/create-order', 'Method': 'post', 'Params': '{"id":"","creator":null,"createTime":"","modifier":null,"modifiedTime":"","dr":null,"ts":null,"serialnum":null,"orderReceiveAddress":{"orderId":null,"id":null,"creator":null,"dr":"0","receiveAddressId":"a8188818-435b-4f9b-bc26-ff98a5bca778","receiveAddressName":null,"receiver":"黎阳","receiverTel":"","receiverPhone":"19979010823","country":"中国","countryId":"COUNTRY-01","receiverProvince":"贵州省","receiverProvinceId":"52","receiverCity":"贵阳市","receiverCityId":"520100000000","receiverCounty":"观山湖区","receiverCountyId":"520115000000","receiverTown":"世纪城社区服务中心","receiverTownId":"520115400000","receiverAddress":"长岭南路33号天一国际10栋902","receiverZipcode":null,"persistStatus":"new"},"orderInvoice":{"orderId":null,"id":null,"creator":null,"dr":null,"invoiceId":"f0d8b999-8614-464a-8e50-32e2e69fbfe5","invoiceType":"增值税发票","invoiceContent":null,"invoiceTitle":"贵州喜马拉雅网络科技有限公司","invoiceTaxId":null,"invoiceBank":"中国建设银行股份有限公司贵阳城北支行","invoiceAccount":null,"invoiceSubBank":null,"persistStatus":"new"},"ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null,"closer":null,"remark":null,"isClose":null,"rejecter":null,"totalNum":"5.00","closeTime":"","isDeClose":null,"orderCode":null,"orderDate":1584186535007,"saleModel":"01","saleOrgId":"e53fc87e-1a16-4a2b-978c-63bfd14fd88b","billTypeId":"SaleOrder","contractId":null,"costTypeId":null,"currencyId":"7cbc1420-737d-4206-97e3-140ebdbe841f","customerId":"a3456c3b-edaa-4cf8-8dff-29ddc68d0749","promAmount":null,"rejectTime":"","srcOrderId":null,"supplierId":null,"closeReason":null,"logisticsId":null,"orderSource":"02","orderTypeId":"0yDZwkYyas4KNNKM4RNF","salesDeptId":"1d5f2aff-5455-4e40-8818-d0e2bbc7e37a","totalAmount":"13445.00","totalVolume":"0.0000","totalWeight":"0.0000","creationTime":"","deliveryDate":1584186535002,"marketAreaId":null,"offsetAmount":null,"rejectReason":null,"settleModeId":null,"srcOrderCode":null,"sycnNCStatus":null,"approveStatus":null,"orderStatusId":"01","srcReqOrderId":null,"sycnOutStatus":null,"approveOpinion":null,"isBomCalcPrice":null,"returnReasonId":null,"salesManagerId":"8e73d0b7-5d0e-4c9d-bcdb-1db337b0b971","totalNetWeight":"0.0000","accountPeriodId":"a1ee592c-4412-42dc-8cee-94d2ac8aa355","goodsOutStyleId":null,"orderStatusCode":null,"orderStatusName":null,"srcReqOrderCode":null,"totalDealAmount":"13445.00","transportModeId":null,"logisticsBillCode":null,"originalOrderCode":null,"receiveCustomerId":"a3456c3b-edaa-4cf8-8dff-29ddc68d0749","totalReturnAmount":null,"superiorCustomerId":null,"underPaymentModeId":null,"maxPreferentialMoney":null,"settleFinancialOrgId":null,"totalGoodsSuppleAmount":"0.00","persistStatus":"new","orderReceiveAddressName":"中国贵州省贵阳市观山湖区世纪城社区服务中心长岭南路33号天一国际10栋902","orderReceiveAddressFirstReceiver":"黎阳","orderReceiveAddressFirstReceiverTel":"19979010823","orderInvoiceName":"贵州喜马拉雅网络科技有限公司","ext01Code":null,"ext01Name":null,"ext02Name":null,"saleOrgName":null,"currencyName":"人民币","customerName":null,"supplierName":null,"logisticsName":null,"orderTypeName":null,"salesDeptName":null,"marketAreaName":null,"settleModeName":null,"salesManagerName":null,"accountPeriodName":"001","transportModeName":null,"receiveCustomerName":null,"superiorCustomerName":null,"settleFinancialOrgName":null,"flushSelected":[],"currencyCode":"CNY","orderItems":[{"id":null,"creator":null,"createTime":"","modifier":null,"modifiedTime":"","dr":null,"ts":"","serialnum":null,"ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null,"amount":"13445.00","isGift":0,"remark":null,"rowNum":20,"volume":null,"weight":null,"goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","isClose":0,"mainNum":"5","signNum":null,"version":"1","bomSplit":null,"goodsImg":"/group1/M00/00/00/rBFAIV0wmbyASJn2AAE4-1jmRp4811.jpg","orderNum":"5.00000000","basePrice":"2789.000000","dealPrice":"2689.000000","goodsCode":"301020000049","goodsName":"小雅AI音箱旗舰版_石墨绿","isDeClose":0,"netWeight":null,"productId":"996cc839-60e8-4500-82c6-9a7c7b95646d","projectId":null,"promPrice":"2689.000000","refundNum":null,"returnNum":null,"rowVolume":0,"rowWeight":0,"salePrice":"2689.000000","batchNumId":null,"currencyId":"7cbc1420-737d-4206-97e3-140ebdbe841f","dealAmount":"13445.00","isOptional":"0","isPromGift":null,"promAmount":null,"promotinId":"","srcOrderId":null,"stockInNum":null,"supplierId":null,"batchCodeId":null,"deliveryNum":null,"existingNum":null,"isDiscounts":null,"logisticsId":null,"priceTypeId":null,"stockOutNum":null,"availableNum":null,"batchNumCode":null,"batchNumName":null,"offsetAmount":null,"replenishNum":null,"returnTypeId":null,"rowNetWeight":0,"srcOrderCode":null,"volumeUnitId":null,"weightUnitId":null,"coordinateNum":null,"isServiceType":null,"mainNumUnitId":"UNIT-12","priceTypeCode":null,"priceTypeName":null,"productLineId":"13c512df-ad18-48e5-b75d-166a534cc410","srcReqOrderId":null,"supplierPrice":null,"baseGoodsOptId":null,"conversionRate":"1.000000","orderNumUnitId":"UNIT-12","returnReasonId":null,"srcOrderItemId":null,"goodsCategoryId":null,"goodsSupplement":0,"originalGoodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","srcReqOrderCode":null,"deliveryInvOrgId":"ebcd635d-237e-4a15-819c-3983ac49436f","goodsDisplayName":"小雅AI音箱旗舰版_石墨绿","planDeliveryDate":1584187053281,"baseGoodsOptValue":null,"srcReqOrderItemId":null,"totalReturnAmount":null,"srcOrderBilltypeId":null,"srcOrderTrantypeId":null,"deliveryWarehouseId":null,"supplementAccountId":null,"goodsSupplementPrice":null,"settleFinancialOrgId":"e53fc87e-1a16-4a2b-978c-63bfd14fd88b","persistStatus":"new","productName":null,"projectName":null,"currencyName":"人民币","promotinName":"","supplierName":null,"logisticsName":null,"volumeUnitName":null,"weightUnitName":null,"mainNumUnitName":"个","productLineName":"喜日","orderNumUnitName":"个","goodsCategoryName":null,"deliveryInvOrgName":"上海喜日电子科技有限公司","deliveryWarehouseName":null,"settleFinancialOrgName":"上海证大喜马拉雅网络科技有限公司","currencyCode":"CNY","creationTime":"","description":""}],"orderItemBoms":[{"id":null,"creator":null,"createTime":"","modifier":null,"modifiedTime":"","dr":null,"ts":"","serialnum":null,"settleFinancialOrgId":"e53fc87e-1a16-4a2b-978c-63bfd14fd88b","ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null,"amount":"13445.00","isGift":0,"remark":null,"rowNum":20,"volume":null,"weight":null,"goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","isClose":0,"mainNum":"5.000000","signNum":"","version":"1","currency":null,"goodsImg":"/group1/M00/00/00/rBFAIV0wmbyASJn2AAE4-1jmRp4811.jpg","orderNum":"5.000000","parentRowNum":20,"basePrice":"","costPrice":null,"dealPrice":"2689.000000","goodsCode":"301020000049","goodsName":"小雅AI音箱旗舰版_石墨绿","isDeClose":0,"netWeight":null,"projectId":null,"refundNum":"","returnNum":"","rowVolume":0,"rowWeight":0,"salePrice":"2689.000000","dealAmount":"13445.00","isOutClose":null,"srcOrderId":null,"stockInNum":"","supplierId":null,"closeReason":null,"deliveryNum":"","existingNum":"","logisticsId":null,"stockOutNum":"","offsetAmount":"","replenishNum":"","rowNetWeight":0,"srcOrderCode":null,"volumeUnitId":null,"weightUnitId":null,"childGoodsQty":1,"coordinateNum":"","goodsSupplementPrice":"","mainNumUnitId":"UNIT-12","parentGoodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","productLineId":"13c512df-ad18-48e5-b75d-166a534cc410","srcReqOrderId":null,"baseGoodsOptId":null,"conversionRate":"1.000000","orderNumUnitId":"UNIT-12","srcOrderItemId":null,"goodsSupplement":0,"originalGoodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","parentGoodsCode":"301020000049","parentGoodsName":"小雅AI音箱旗舰版_石墨绿","srcReqOrderCode":null,"deliveryInvOrgId":"ebcd635d-237e-4a15-819c-3983ac49436f","planDeliveryDate":1584187053000,"baseGoodsOptValue":null,"deliveryWarehouseId":null,"srcOrderItemBomId":null,"srcReqOrderItemBomId":null,"srcReqOrderItemId":null,"bomSplit":null,"productId":"996cc839-60e8-4500-82c6-9a7c7b95646d","promPrice":"2689.000000","batchNumId":null,"currencyId":null,"isOptional":"0","isPromGift":null,"promAmount":null,"promotinId":null,"batchCodeId":null,"isDiscounts":null,"priceTypeId":null,"availableNum":null,"batchNumCode":null,"batchNumName":null,"returnTypeId":null,"isServiceType":null,"priceTypeCode":null,"priceTypeName":null,"supplierPrice":null,"returnReasonId":null,"goodsCategoryId":null,"goodsDisplayName":"小雅AI音箱旗舰版_石墨绿","totalReturnAmount":null,"srcOrderBilltypeId":null,"srcOrderTrantypeId":null,"supplementAccountId":null,"persistStatus":"new","settleFinancialOrgName":"上海证大喜马拉雅网络科技有限公司","currencyName":null,"projectName":null,"supplierName":null,"logisticsName":null,"volumeUnitName":null,"weightUnitName":null,"mainNumUnitName":"个","productLineName":"喜日","orderNumUnitName":"个","deliveryInvOrgName":"上海喜日电子科技有限公司","deliveryWarehouseName":null,"productName":null,"promotinName":null,"goodsCategoryName":null,"creationTime":"","description":""}]}', 'CheckTpye': 'check_json', 'ExpectedCode': 200.0, 'ExpectedData': '{"id":"f4ea927b-24e3-4196-8b20-dc6c9245c90b","dr":0,"ts":1584186948862,"creator":"gaojian","creationTime":1584186948862,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":null,"state":0,"approver":null,"approveTime":null,"approveOpinion":null,"sycnNCStatus":null,"sycnOutStatus":null,"saleOrgId":"e53fc87e-1a16-4a2b-978c-63bfd14fd88b","saleOrgCode":"1101","saleOrgName":"上海证大喜马拉雅网络科技有限公司","supplierId":null,"supplierCode":null,"supplierName":null,"receiveCustomerId":"a3456c3b-edaa-4cf8-8dff-29ddc68d0749","receiveCustomerCode":"10001621","receiveCustomerName":"贵州喜马拉雅网络科技有限公司","contractId":null,"contractCode":null,"contractName":null,"settleFinancialOrgId":null,"settleFinancialOrgCode":null,"settleFinancialOrgName":null,"sameFinancialOrg":false,"orderTypeId":"0yDZwkYyas4KNNKM4RNF","orderTypeCode":"30-Cxx-02","orderTypeName":"先货后款","billTypeId":"SaleOrder","billTypeCode":"SaleOrder","billTypeName":"销售订单","costTypeId":null,"costTypeCode":null,"costTypeName":null,"saleModel":"01","orderCode":"SOO20200314000028","orderDate":1584186535007,"orderStatusId":"42c874d4-a9f0-4104-9342-4a2cd8c4a600","orderStatusCode":"01","orderStatusName":"待处理","customerId":"a3456c3b-edaa-4cf8-8dff-29ddc68d0749","customerCode":"10001621","customerName":"贵州喜马拉雅网络科技有限公司","marketAreaId":null,"marketAreaCode":null,"marketAreaName":null,"salesManagerId":"8e73d0b7-5d0e-4c9d-bcdb-1db337b0b971","salesManagerCode":"3527","salesManagerName":"诸佳艺","salesDeptId":"1d5f2aff-5455-4e40-8818-d0e2bbc7e37a","salesDeptCode":"01010101","salesDeptName":"区域招商","transportModeId":null,"transportModeCode":null,"transportModeName":null,"settleModeId":null,"settleModeCode":null,"settleModeName":null,"deliveryDate":1584186535002,"totalNum":5.00,"currencyId":"7cbc1420-737d-4206-97e3-140ebdbe841f","currencyCode":"CNY","currencyName":"人民币","currencyPriceScale":null,"currencyAmountScale":null,"totalDealAmount":13445.00,"totalAmount":13445.00,"promAmount":null,"offsetAmount":null,"totalWeight":0.0000,"totalNetWeight":0.0000,"totalVolume":0.0000,"orderSource":"02","isClose":0,"closer":null,"closeTime":null,"isDeClose":0,"deCloser":null,"deCloseTime":null,"closeReason":null,"remark":null,"rejecter":null,"rejectTime":null,"rejectReason":null,"srcOrderCode":null,"srcOrderId":null,"srcReqOrderCode":null,"srcReqOrderId":null,"orderReceiveAddress":{"id":"000wWeLVRL6fl2QafwQC","dr":0,"ts":1584186948863,"creator":"gaojian","creationTime":1584186948863,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":null,"orderId":"f4ea927b-24e3-4196-8b20-dc6c9245c90b","receiveAddressId":"a8188818-435b-4f9b-bc26-ff98a5bca778","receiver":"黎阳","receiverTel":"","receiverPhone":"19979010823","country":"中国","countryId":"COUNTRY-01","receiverProvince":"贵州省","receiverProvinceId":"52","receiverCity":"贵阳市","receiverCityId":"520100000000","receiverCounty":"观山湖区","receiverCountyId":"520115000000","receiverTown":"世纪城社区服务中心","receiverTownId":"520115400000","receiverAddress":"长岭南路33号天一国际10栋902","receiverZipcode":null},"orderInvoice":{"id":"04nTcpOTUvPzffsxgk3j","dr":0,"ts":1584186948863,"creator":"gaojian","creationTime":1584186948863,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":null,"orderId":"f4ea927b-24e3-4196-8b20-dc6c9245c90b","invoiceId":"f0d8b999-8614-464a-8e50-32e2e69fbfe5","invoiceType":"增值税发票","invoiceContent":null,"invoiceTitle":"贵州喜马拉雅网络科技有限公司","invoiceTaxId":null,"invoiceBank":"中国建设银行股份有限公司贵阳城北支行","invoiceAccount":null,"invoiceSubBank":null},"orderReceiveAddressStr":null,"orderInvoiceStr":null,"orderItems":[{"id":"0vdY8dBmG8pI0urdFb7T","dr":0,"ts":1584186948862,"creator":"gaojian","creationTime":1584186948862,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":null,"orderId":"f4ea927b-24e3-4196-8b20-dc6c9245c90b","orderCode":"SOO20200314000028","orderBillType":"SaleOrder","customerId":"a3456c3b-edaa-4cf8-8dff-29ddc68d0749","customerName":null,"rowNum":"20","productId":"996cc839-60e8-4500-82c6-9a7c7b95646d","goodsCategoryId":null,"goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","goodsCode":"301020000049","goodsName":"小雅AI音箱旗舰版_石墨绿","goodsDisplayName":"小雅AI音箱旗舰版_石墨绿","goodsImg":"/group1/M00/00/00/rBFAIV0wmbyASJn2AAE4-1jmRp4811.jpg","productLineId":"13c512df-ad18-48e5-b75d-166a534cc410","rowWeight":0,"weight":null,"rowNetWeight":0,"netWeight":null,"weightUnitId":null,"weightUnitCode":null,"weightUnitName":null,"rowVolume":0,"volume":null,"volumeUnitId":null,"volumeUnitCode":null,"volumeUnitName":null,"orderNum":5.00000000,"orderNumUnitId":"UNIT-12","orderNumUnitCode":"EA","orderNumUnitName":"个","mainNum":5,"mainNumUnitId":"UNIT-12","mainNumUnitCode":"EA","mainNumUnitName":"个","conversionRate":1.000000,"basePrice":2789.000000,"supplierPrice":null,"salePrice":2689.000000,"promPrice":2689.000000,"dealPrice":2689.000000,"amount":13445.00,"promAmount":null,"offsetAmount":null,"dealAmount":13445.00,"currencyId":"7cbc1420-737d-4206-97e3-140ebdbe841f","currencyCode":"CNY","currencyName":"人民币","currencySign":null,"currencyAmountScale":null,"currencyPriceScale":null,"isGift":0,"logisticsId":null,"logisticsCode":null,"logisticsName":null,"promotinId":null,"promotinCode":null,"promotinName":null,"planDeliveryDate":1584187053281,"deliveryInvOrgId":"ebcd635d-237e-4a15-819c-3983ac49436f","deliveryInvOrgCode":"1302","deliveryInvOrgName":"上海喜日电子科技有限公司","deliveryWarehouseId":null,"deliveryWarehouseCode":null,"deliveryWarehouseName":null,"isClose":0,"isDeClose":0,"remark":null,"deliveryNum":0,"stockInNum":0,"stockOutNum":0,"returnNum":0,"refundNum":0,"signNum":0,"replenishNum":0,"coordinateNum":0,"srcOrderCode":null,"srcOrderId":null,"srcOrderItemId":null,"srcOrderTrantypeId":null,"srcOrderBilltypeId":null,"srcReqOrderCode":null,"srcReqOrderId":null,"srcReqOrderItemId":null,"totalReturnAmount":null,"returnReasonId":null,"returnReasonCode":null,"returnReasonName":null,"returnTypeId":null,"returnTypeCode":null,"returnTypeName":null,"orderPromRels":[],"orderAttachments":[],"version":1,"originalGoodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","settleFinancialOrgId":"e53fc87e-1a16-4a2b-978c-63bfd14fd88b","settleFinancialOrgCode":"1101","settleFinancialOrgName":"上海证大喜马拉雅网络科技有限公司","projectId":null,"projectCode":null,"projectName":null,"baseGoodsOptId":null,"baseGoodsOptValue":null,"supplierId":null,"supplierCode":null,"supplierName":null,"batchCodeId":null,"batchCodeCode":null,"batchCodeName":null,"goodsSupplement":0,"srcContractId":null,"srcContractCode":null,"srcContractType":null,"srcQuoteId":null,"goodsSupplementPrice":null,"offsetDetailsDtoList":[],"existingNum":null,"availableNum":null,"closeReason":null,"orderCorrelationMoney":null,"ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null,"bomSplit":null}],"orderItemBoms":[{"id":"09Dgs68Pu1H2zPadDyi2","dr":0,"ts":1584186948863,"creator":"gaojian","creationTime":1584186948863,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":null,"orderId":"f4ea927b-24e3-4196-8b20-dc6c9245c90b","orderItemId":"0vdY8dBmG8pI0urdFb7T","parentRowNum":"20","parentGoodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","parentGoodsCode":"301020000049","parentGoodsName":"小雅AI音箱旗舰版_石墨绿","rowNum":"20","goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","goodsCode":"301020000049","goodsName":"小雅AI音箱旗舰版_石墨绿","goodsImg":"/group1/M00/00/00/rBFAIV0wmbyASJn2AAE4-1jmRp4811.jpg","isGift":0,"productLineId":"13c512df-ad18-48e5-b75d-166a534cc410","rowWeight":0,"weight":null,"rowNetWeight":0,"netWeight":null,"weightUnitId":null,"weightUnitCode":null,"weightUnitName":null,"rowVolume":0,"volume":null,"volumeUnitId":null,"volumeUnitCode":null,"volumeUnitName":null,"orderNum":5.000000,"orderNumUnitId":"UNIT-12","orderNumUnitCode":"EA","orderNumUnitName":"个","mainNum":5.000000,"mainNumUnitId":"UNIT-12","mainNumUnitCode":"EA","mainNumUnitName":"个","conversionRate":1.000000,"basePrice":null,"salePrice":2689.000000,"amount":13445.00,"dealPrice":2689.000000,"dealAmount":13445.00,"currency":null,"planDeliveryDate":1584187053000,"deliveryInvOrgId":"ebcd635d-237e-4a15-819c-3983ac49436f","deliveryWarehouseId":null,"baseGoodsOptId":null,"baseGoodsOptVals":null,"baseGoodsOptValue":null,"version":1,"originalGoodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","childGoodsQty":1,"projectId":null,"supplierId":null,"srcOrderCode":null,"srcOrderId":null,"srcOrderItemId":null,"srcOrderItemBomId":null,"srcReqOrderCode":null,"goodsSupplement":0,"srcReqOrderId":null,"srcReqOrderItemId":null,"srcReqOrderItemBomId":null,"existingNum":null,"ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null,"deliveryInvOrgCode":null,"deliveryInvOrgName":null,"deliveryWarehouseCode":null,"deliveryWarehouseName":null,"goodsSupplementPrice":null,"costPrice":null,"supplierPrice":null,"supplierCode":null,"supplierName":null,"logisticsId":null,"logisticsCode":null,"logisticsName":null,"deliveryNum":null,"stockInNum":null,"stockOutNum":null,"returnNum":null,"refundNum":null,"signNum":null,"replenishNum":null,"coordinateNum":null,"isClose":0,"closeReason":null,"isDeClose":0,"isOutClose":null,"offsetAmount":null,"settleFinancialOrgId":"e53fc87e-1a16-4a2b-978c-63bfd14fd88b","settleFinancialOrgCode":"1101","settleFinancialOrgName":"上海证大喜马拉雅网络科技有限公司","remark":null}],"orderPromRels":[],"orderAttachments":[],"logisticsId":null,"logisticsCode":null,"logisticsName":null,"logisticsBillCode":null,"originalOrderCode":null,"totalReturnAmount":null,"returnReasonId":null,"returnReasonCode":null,"returnReasonName":null,"accountPeriodId":"a1ee592c-4412-42dc-8cee-94d2ac8aa355","accountPeriodCode":"001","accountPeriodName":"001","superiorCustomerId":null,"superiorCustomerCode":null,"superiorCustomerName":null,"totalGoodsSuppleAmount":0.00,"orderCorrelationMoney":null,"flushSelected":[],"contractTypeId":null,"ext01Id":null,"ext01Code":null,"ext01Name":null,"ext02Id":null,"ext02Code":null,"ext02Name":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null,"goodsOutStyleId":null,"goodsOutStyleCode":null,"goodsOutStyleName":null,"isBomCalcPrice":null,"underPaymentModeId":null,"underPaymentModeCode":null,"underPaymentModeName":null}', 'User': 'Manager', 'Correlation': '', 'Active': 'Yes', 'Sql': ''}
# code,resp_data= (200, {'id00000000': '0CGWTzKizt9bcGmCIa2A', 'dr': 0, 'ts': 1584325494730, 'creator': None, 'creationTime': 1584325494730, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm', 'promptMessage': None, 'state': 0, 'approver': None, 'approveTime': None, 'approveOpinion': None, 'sycnNCStatus': None, 'sycnOutStatus': None, 'saleOrgId': 'e53fc87e-1a16-4a2b-978c-63bfd14fd88b', 'saleOrgCode': '1101', 'saleOrgName': '上海证大喜马拉雅网络科技有限公司', 'supplierId': None, 'supplierCode': None, 'supplierName': None, 'receiveCustomerId': 'a3456c3b-edaa-4cf8-8dff-29ddc68d0749', 'receiveCustomerCode': '10001621', 'receiveCustomerName': '贵州喜马拉雅网络科技有限公司', 'contractId': None, 'contractCode': None, 'contractName': None, 'settleFinancialOrgId': None, 'settleFinancialOrgCode': None, 'settleFinancialOrgName': None, 'sameFinancialOrg': False, 'orderTypeId': '0yDZwkYyas4KNNKM4RNF', 'orderTypeCode': '30-Cxx-02', 'orderTypeName': '先货后款', 'billTypeId': 'SaleOrder', 'billTypeCode': 'SaleOrder', 'billTypeName': '销售订单', 'costTypeId': None, 'costTypeCode': None, 'costTypeName': None, 'saleModel': '01', 'orderCode': 'SOO20200316000002', 'orderDate': 1584186535007, 'orderStatusId': '42c874d4-a9f0-4104-9342-4a2cd8c4a600', 'orderStatusCode': '01', 'orderStatusName': '待处理', 'customerId': 'a3456c3b-edaa-4cf8-8dff-29ddc68d0749', 'customerCode': '10001621', 'customerName': '贵州喜马拉雅网络科技有限公司', 'marketAreaId': None, 'marketAreaCode': None, 'marketAreaName': None, 'salesManagerId': '8e73d0b7-5d0e-4c9d-bcdb-1db337b0b971', 'salesManagerCode': '3527', 'salesManagerName': '诸佳艺', 'salesDeptId': '1d5f2aff-5455-4e40-8818-d0e2bbc7e37a', 'salesDeptCode': '01010101', 'salesDeptName': '区域招商', 'transportModeId': None, 'transportModeCode': None, 'transportModeName': None, 'settleModeId': None, 'settleModeCode': None, 'settleModeName': None, 'deliveryDate': 1584186535002, 'totalNum': 5.0, 'currencyId': '7cbc1420-737d-4206-97e3-140ebdbe841f', 'currencyCode': 'CNY', 'currencyName': '人民币', 'currencyPriceScale': None, 'currencyAmountScale': None, 'totalDealAmount': 13445.0, 'totalAmount': 13445.0, 'promAmount': None, 'offsetAmount': None, 'totalWeight': 0.0, 'totalNetWeight': 0.0, 'totalVolume': 0.0, 'orderSource': '02', 'isClose': 0, 'closer': None, 'closeTime': None, 'isDeClose': 0, 'deCloser': None, 'deCloseTime': None, 'closeReason': None, 'remark': None, 'rejecter': None, 'rejectTime': None, 'rejectReason': None, 'srcOrderCode': None, 'srcOrderId': None, 'srcReqOrderCode': None, 'srcReqOrderId': None, 'orderReceiveAddress': {'id': '0nPzYUOjKEqLvaf8DLiH', 'dr': 0, 'ts': 1584325494735, 'creator': None, 'creationTime': 1584325494735, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm', 'promptMessage': None, 'orderId': '0CGWTzKizt9bcGmCIa2A', 'receiveAddressId': 'a8188818-435b-4f9b-bc26-ff98a5bca778', 'receiver': '黎阳', 'receiverTel': '', 'receiverPhone': '19979010823', 'country': '中国', 'countryId': 'COUNTRY-01', 'receiverProvince': '贵州省', 'receiverProvinceId': '52', 'receiverCity': '贵阳市', 'receiverCityId': '520100000000', 'receiverCounty': '观山湖区', 'receiverCountyId': '520115000000', 'receiverTown': '世纪城社区服务中心', 'receiverTownId': '520115400000', 'receiverAddress': '长岭南路33号天一国际10栋902', 'receiverZipcode': None}, 'orderInvoice': {'id': '02FTFbVWTN7AlOqhErYD', 'dr': 0, 'ts': 1584325494735, 'creator': None, 'creationTime': 1584325494735, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm', 'promptMessage': None, 'orderId': '0CGWTzKizt9bcGmCIa2A', 'invoiceId': 'f0d8b999-8614-464a-8e50-32e2e69fbfe5', 'invoiceType': '增值税发票', 'invoiceContent': None, 'invoiceTitle': '贵州喜马拉雅网络科技有限公司', 'invoiceTaxId': None, 'invoiceBank': '中国建设银行股份有限公司贵阳城北支行', 'invoiceAccount': None, 'invoiceSubBank': None}, 'orderReceiveAddressStr': None, 'orderInvoiceStr': None, 'orderItems': [{'id': '0lkTvXjiWQJ5jooSOahV', 'dr': 0, 'ts': 1584325494734, 'creator': None, 'creationTime': 1584325494734, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm', 'promptMessage': None, 'orderId': '0CGWTzKizt9bcGmCIa2A', 'orderCode': 'SOO20200316000002', 'orderBillType': 'SaleOrder', 'customerId': 'a3456c3b-edaa-4cf8-8dff-29ddc68d0749', 'customerName': None, 'rowNum': '20', 'productId': '996cc839-60e8-4500-82c6-9a7c7b95646d', 'goodsCategoryId': None, 'goodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'goodsCode': '301020000049', 'goodsName': '小雅AI音箱旗舰版_石墨绿', 'goodsDisplayName': '小雅AI音箱旗舰版_石墨绿', 'goodsImg': '/group1/M00/00/00/rBFAIV0wmbyASJn2AAE4-1jmRp4811.jpg', 'productLineId': '13c512df-ad18-48e5-b75d-166a534cc410', 'rowWeight': 0, 'weight': None, 'rowNetWeight': 0, 'netWeight': None, 'weightUnitId': None, 'weightUnitCode': None, 'weightUnitName': None, 'rowVolume': 0, 'volume': None, 'volumeUnitId': None, 'volumeUnitCode': None, 'volumeUnitName': None, 'orderNum': 5.0, 'orderNumUnitId': 'UNIT-12', 'orderNumUnitCode': 'EA', 'orderNumUnitName': '个', 'mainNum': 5, 'mainNumUnitId': 'UNIT-12', 'mainNumUnitCode': 'EA', 'mainNumUnitName': '个', 'conversionRate': 1.0, 'basePrice': 2789.0, 'supplierPrice': None, 'salePrice': 2689.0, 'promPrice': 2689.0, 'dealPrice': 2689.0, 'amount': 13445.0, 'promAmount': None, 'offsetAmount': None, 'dealAmount': 13445.0, 'currencyId': '7cbc1420-737d-4206-97e3-140ebdbe841f', 'currencyCode': 'CNY', 'currencyName': '人民币', 'currencySign': None, 'currencyAmountScale': None, 'currencyPriceScale': None, 'isGift': 0, 'logisticsId': None, 'logisticsCode': None, 'logisticsName': None, 'promotinId': None, 'promotinCode': None, 'promotinName': None, 'planDeliveryDate': 1584187053281, 'deliveryInvOrgId': 'ebcd635d-237e-4a15-819c-3983ac49436f', 'deliveryInvOrgCode': '1302', 'deliveryInvOrgName': '上海喜日电子科技有限公司', 'deliveryWarehouseId': None, 'deliveryWarehouseCode': None, 'deliveryWarehouseName': None, 'isClose': 0, 'isDeClose': 0, 'remark': None, 'deliveryNum': 0, 'stockInNum': 0, 'stockOutNum': 0, 'returnNum': 0, 'refundNum': 0, 'signNum': 0, 'replenishNum': 0, 'coordinateNum': 0, 'srcOrderCode': None, 'srcOrderId': None, 'srcOrderItemId': None, 'srcOrderTrantypeId': None, 'srcOrderBilltypeId': None, 'srcReqOrderCode': None, 'srcReqOrderId': None, 'srcReqOrderItemId': None, 'totalReturnAmount': None, 'returnReasonId': None, 'returnReasonCode': None, 'returnReasonName': None, 'returnTypeId': None, 'returnTypeCode': None, 'returnTypeName': None, 'orderPromRels': [], 'orderAttachments': [], 'version': 1, 'originalGoodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'settleFinancialOrgId': 'e53fc87e-1a16-4a2b-978c-63bfd14fd88b', 'settleFinancialOrgCode': '1101', 'settleFinancialOrgName': '上海证大喜马拉雅网络科技有限公司', 'projectId': None, 'projectCode': None, 'projectName': None, 'baseGoodsOptId': None, 'baseGoodsOptValue': None, 'supplierId': None, 'supplierCode': None, 'supplierName': None, 'batchCodeId': None, 'batchCodeCode': None, 'batchCodeName': None, 'goodsSupplement': 0, 'srcContractId': None, 'srcContractCode': None, 'srcContractType': None, 'srcQuoteId': None, 'goodsSupplementPrice': None, 'offsetDetailsDtoList': [], 'existingNum': None, 'availableNum': None, 'closeReason': None, 'orderCorrelationMoney': None, 'ext01': None, 'ext02': None, 'ext03': None, 'ext04': None, 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None, 'bomSplit': None}], 'orderItemBoms': [{'id': '0oOzhUILq3VrVO02Tanl', 'dr': 0, 'ts': 1584325494735, 'creator': None, 'creationTime': 1584325494735, 'modifier': None, 'modifiedTime': None, 'persistStatus': 'nrm', 'promptMessage': None, 'orderId': '0CGWTzKizt9bcGmCIa2A', 'orderItemId': '0lkTvXjiWQJ5jooSOahV', 'parentRowNum': '20', 'parentGoodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'parentGoodsCode': '301020000049', 'parentGoodsName': '小雅AI音箱旗舰版_石墨绿', 'rowNum': '20', 'goodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'goodsCode': '301020000049', 'goodsName': '小雅AI音箱旗舰版_石墨绿', 'goodsImg': '/group1/M00/00/00/rBFAIV0wmbyASJn2AAE4-1jmRp4811.jpg', 'isGift': 0, 'productLineId': '13c512df-ad18-48e5-b75d-166a534cc410', 'rowWeight': 0, 'weight': None, 'rowNetWeight': 0, 'netWeight': None, 'weightUnitId': None, 'weightUnitCode': None, 'weightUnitName': None, 'rowVolume': 0, 'volume': None, 'volumeUnitId': None, 'volumeUnitCode': None, 'volumeUnitName': None, 'orderNum': 5.0, 'orderNumUnitId': 'UNIT-12', 'orderNumUnitCode': 'EA', 'orderNumUnitName': '个', 'mainNum': 5.0, 'mainNumUnitId': 'UNIT-12', 'mainNumUnitCode': 'EA', 'mainNumUnitName': '个', 'conversionRate': 1.0, 'basePrice': None, 'salePrice': 2689.0, 'amount': 13445.0, 'dealPrice': 2689.0, 'dealAmount': 13445.0, 'currency': None, 'planDeliveryDate': 1584187053000, 'deliveryInvOrgId': 'ebcd635d-237e-4a15-819c-3983ac49436f', 'deliveryWarehouseId': None, 'baseGoodsOptId': None, 'baseGoodsOptVals': None, 'baseGoodsOptValue': None, 'version': 1, 'originalGoodsId': '03e77ae0-469d-4d8a-ba34-733c2ada3749', 'childGoodsQty': 1, 'projectId': None, 'supplierId': None, 'srcOrderCode': None, 'srcOrderId': None, 'srcOrderItemId': None, 'srcOrderItemBomId': None, 'srcReqOrderCode': None, 'goodsSupplement': 0, 'srcReqOrderId': None, 'srcReqOrderItemId': None, 'srcReqOrderItemBomId': None, 'existingNum': None, 'ext01': None, 'ext02': None, 'ext03': None, 'ext04': None, 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None, 'deliveryInvOrgCode': None, 'deliveryInvOrgName': None, 'deliveryWarehouseCode': None, 'deliveryWarehouseName': None, 'goodsSupplementPrice': None, 'costPrice': None, 'supplierPrice': None, 'supplierCode': None, 'supplierName': None, 'logisticsId': None, 'logisticsCode': None, 'logisticsName': None, 'deliveryNum': None, 'stockInNum': None, 'stockOutNum': None, 'returnNum': None, 'refundNum': None, 'signNum': None, 'replenishNum': None, 'coordinateNum': None, 'isClose': 0, 'closeReason': None, 'isDeClose': 0, 'isOutClose': None, 'offsetAmount': None, 'settleFinancialOrgId': 'e53fc87e-1a16-4a2b-978c-63bfd14fd88b', 'settleFinancialOrgCode': '1101', 'settleFinancialOrgName': '上海证大喜马拉雅网络科技有限公司', 'remark': None}], 'orderPromRels': [], 'orderAttachments': [], 'logisticsId': None, 'logisticsCode': None, 'logisticsName': None, 'logisticsBillCode': None, 'originalOrderCode': None, 'totalReturnAmount': None, 'returnReasonId': None, 'returnReasonCode': None, 'returnReasonName': None, 'accountPeriodId': 'a1ee592c-4412-42dc-8cee-94d2ac8aa355', 'accountPeriodCode': '001', 'accountPeriodName': '001', 'superiorCustomerId': None, 'superiorCustomerCode': None, 'superiorCustomerName': None, 'totalGoodsSuppleAmount': 0.0, 'orderCorrelationMoney': None, 'flushSelected': [], 'contractTypeId': None, 'ext01Id': None, 'ext01Code': None, 'ext01Name': None, 'ext02Id': None, 'ext02Code': None, 'ext02Name': None, 'ext03': None, 'ext04': None, 'ext05': None, 'ext06': None, 'ext07': None, 'ext08': None, 'ext09': None, 'ext10': None, 'ext11': None, 'ext12': None, 'ext13': None, 'ext14': None, 'ext15': None, 'goodsOutStyleId': None, 'goodsOutStyleCode': None, 'goodsOutStyleName': None, 'isBomCalcPrice': None, 'underPaymentModeId': None, 'underPaymentModeCode': None, 'underPaymentModeName': None})
#
# @allure.feature('测试')
# def test_check_result():
#     assert check_result(case,code,resp_data)
#     # print('校验结果',re)
#
# # test_check_json(src_data,res_data)
# if __name__ == '__main__':
#     pytest.main()

# check_result(case,code,resp_data)