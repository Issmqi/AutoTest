# -*- coding: utf-8 -*-
# !/bin/bash

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
data={'CaseId': 2.0, 'CaseName': 'get_sales_order_details', 'APIName': '查询销售订单详情', 'Headers': "{'Content-Type':'application/x-www-form-urlencoded','charset': 'UTF-8'}", 'Path': '/occ-b2b-order/b2b/order/detail', 'Method': 'get', 'ParameterType': 'parameter', 'Params': '{"id":"040pnM4EHJ4dzuEqtgxG","search_AUTH_APPCODE":"saleorder"}', 'CheckTpye': 'check_json', 'ExpectedCode': 200.0, 'ExpectedData': '{"id":"040pnM4EHJ4dzuEqtgxG","dr":0,"ts":1584497206000,"creator":"gaojian","creationTime":1584497206000,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":null,"state":0,"approver":null,"approveTime":null,"approveOpinion":null,"sycnNCStatus":null,"sycnOutStatus":null,"saleOrgId":"e53fc87e-1a16-4a2b-978c-63bfd14fd88b","saleOrgCode":"1101","saleOrgName":"上海证大喜马拉雅网络科技有限公司","supplierId":null,"supplierCode":null,"supplierName":null,"receiveCustomerId":"a3456c3b-edaa-4cf8-8dff-29ddc68d0749","receiveCustomerCode":"10001621","receiveCustomerName":"贵州喜马拉雅网络科技有限公司","contractId":null,"contractCode":null,"contractName":null,"settleFinancialOrgId":null,"settleFinancialOrgCode":null,"settleFinancialOrgName":null,"sameFinancialOrg":false,"orderTypeId":"0yDZwkYyas4KNNKM4RNF","orderTypeCode":"30-Cxx-02","orderTypeName":"先货后款","billTypeId":"SaleOrder","billTypeCode":"SaleOrder","billTypeName":"销售订单","costTypeId":null,"costTypeCode":null,"costTypeName":null,"saleModel":"01","orderCode":"SOO20200318000009","orderDate":1584186535000,"orderStatusId":"42c874d4-a9f0-4104-9342-4a2cd8c4a600","orderStatusCode":"01","orderStatusName":"待处理","customerId":"a3456c3b-edaa-4cf8-8dff-29ddc68d0749","customerCode":"10001621","customerName":"贵州喜马拉雅网络科技有限公司","marketAreaId":null,"marketAreaCode":null,"marketAreaName":null,"salesManagerId":"8e73d0b7-5d0e-4c9d-bcdb-1db337b0b971","salesManagerCode":"3527","salesManagerName":"诸佳艺","salesDeptId":"1d5f2aff-5455-4e40-8818-d0e2bbc7e37a","salesDeptCode":"01010101","salesDeptName":"区域招商","transportModeId":null,"transportModeCode":null,"transportModeName":null,"settleModeId":null,"settleModeCode":null,"settleModeName":null,"deliveryDate":1584186535000,"totalNum":5.00000000,"currencyId":"7cbc1420-737d-4206-97e3-140ebdbe841f","currencyCode":"CNY","currencyName":"人民币","currencyPriceScale":null,"currencyAmountScale":null,"totalDealAmount":13445.00000000,"totalAmount":13445.00000000,"promAmount":null,"offsetAmount":null,"totalWeight":0E-8,"totalNetWeight":0E-8,"totalVolume":0E-8,"orderSource":"02","isClose":0,"closer":null,"closeTime":null,"isDeClose":0,"deCloser":null,"deCloseTime":null,"closeReason":null,"remark":null,"rejecter":null,"rejectTime":null,"rejectReason":null,"srcOrderCode":null,"srcOrderId":null,"srcReqOrderCode":"REQ20200318000009","srcReqOrderId":"0GWSDyo52GFam6Z679Qs","orderReceiveAddress":{"id":"0CYZt2RzFIEl2UeMF0FI","dr":0,"ts":1584497206000,"creator":"gaojian","creationTime":1584497206000,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":null,"orderId":"040pnM4EHJ4dzuEqtgxG","receiveAddressId":"a8188818-435b-4f9b-bc26-ff98a5bca778","receiver":"黎阳","receiverTel":"","receiverPhone":"19979010823","country":"中国","countryId":"COUNTRY-01","receiverProvince":"贵州省","receiverProvinceId":"52","receiverCity":"贵阳市","receiverCityId":"520100000000","receiverCounty":"观山湖区","receiverCountyId":"520115000000","receiverTown":"世纪城社区服务中心","receiverTownId":"520115400000","receiverAddress":"长岭南路33号天一国际10栋902","receiverZipcode":null},"orderInvoice":{"id":"0Amgzx4s0B6W5FIJf6z4","dr":0,"ts":1584497206000,"creator":"gaojian","creationTime":1584497206000,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":null,"orderId":"040pnM4EHJ4dzuEqtgxG","invoiceId":"f0d8b999-8614-464a-8e50-32e2e69fbfe5","invoiceType":"增值税发票","invoiceContent":null,"invoiceTitle":"贵州喜马拉雅网络科技有限公司","invoiceTaxId":null,"invoiceBank":"中国建设银行股份有限公司贵阳城北支行","invoiceAccount":null,"invoiceSubBank":null},"orderReceiveAddressStr":null,"orderInvoiceStr":null,"orderItems":[{"id":"0MVKo2c7xOvjDbQmC2op","dr":0,"ts":1584497206000,"creator":"gaojian","creationTime":1584497206000,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":null,"orderId":"040pnM4EHJ4dzuEqtgxG","orderCode":"SOO20200318000009","orderBillType":"SaleOrder","customerId":"a3456c3b-edaa-4cf8-8dff-29ddc68d0749","customerName":null,"rowNum":"20","productId":"996cc839-60e8-4500-82c6-9a7c7b95646d","goodsCategoryId":null,"goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","goodsCode":"301020000049","goodsName":"小雅AI音箱旗舰版_石墨绿","goodsDisplayName":"小雅AI音箱旗舰版_石墨绿","goodsImg":"/group1/M00/00/00/rBFAIV0wmbyASJn2AAE4-1jmRp4811.jpg","productLineId":"13c512df-ad18-48e5-b75d-166a534cc410","rowWeight":0E-8,"weight":null,"rowNetWeight":0E-8,"netWeight":null,"weightUnitId":null,"weightUnitCode":null,"weightUnitName":null,"rowVolume":0E-8,"volume":null,"volumeUnitId":null,"volumeUnitCode":null,"volumeUnitName":null,"orderNum":5.00000000,"orderNumUnitId":"UNIT-12","orderNumUnitCode":"EA","orderNumUnitName":"个","mainNum":5.00000000,"mainNumUnitId":"UNIT-12","mainNumUnitCode":"EA","mainNumUnitName":"个","conversionRate":1.00000000,"basePrice":2789.00000000,"supplierPrice":null,"salePrice":2689.00000000,"promPrice":2689.00000000,"dealPrice":2689.00000000,"amount":13445.00000000,"promAmount":null,"offsetAmount":null,"dealAmount":13445.00000000,"currencyId":"7cbc1420-737d-4206-97e3-140ebdbe841f","currencyCode":"CNY","currencyName":"人民币","currencySign":null,"currencyAmountScale":null,"currencyPriceScale":null,"isGift":0,"logisticsId":null,"logisticsCode":null,"logisticsName":null,"promotinId":null,"promotinCode":null,"promotinName":null,"planDeliveryDate":1584187053000,"deliveryInvOrgId":"ebcd635d-237e-4a15-819c-3983ac49436f","deliveryInvOrgCode":"1302","deliveryInvOrgName":"上海喜日电子科技有限公司","deliveryWarehouseId":null,"deliveryWarehouseCode":null,"deliveryWarehouseName":null,"isClose":0,"isDeClose":0,"remark":null,"deliveryNum":0E-8,"stockInNum":0E-8,"stockOutNum":0E-8,"returnNum":0E-8,"refundNum":0E-8,"signNum":0E-8,"replenishNum":0E-8,"coordinateNum":0E-8,"srcOrderCode":null,"srcOrderId":null,"srcOrderItemId":null,"srcOrderTrantypeId":null,"srcOrderBilltypeId":null,"srcReqOrderCode":"REQ20200318000009","srcReqOrderId":"0GWSDyo52GFam6Z679Qs","srcReqOrderItemId":null,"totalReturnAmount":null,"returnReasonId":null,"returnReasonCode":null,"returnReasonName":null,"returnTypeId":null,"returnTypeCode":null,"returnTypeName":null,"orderPromRels":[],"orderAttachments":[],"version":1,"originalGoodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","settleFinancialOrgId":"e53fc87e-1a16-4a2b-978c-63bfd14fd88b","settleFinancialOrgCode":"1101","settleFinancialOrgName":"上海证大喜马拉雅网络科技有限公司","projectId":null,"projectCode":null,"projectName":null,"baseGoodsOptId":null,"baseGoodsOptValue":null,"supplierId":null,"supplierCode":null,"supplierName":null,"batchCodeId":null,"batchCodeCode":null,"batchCodeName":null,"goodsSupplement":0,"srcContractId":null,"srcContractCode":null,"srcContractType":null,"srcQuoteId":null,"goodsSupplementPrice":null,"offsetDetailsDtoList":[],"existingNum":null,"availableNum":null,"closeReason":null,"orderCorrelationMoney":null,"ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null,"bomSplit":null}],"orderItemBoms":[{"id":"0mocF2YMY31TldnrVaC4","dr":0,"ts":1584497206000,"creator":"gaojian","creationTime":1584497206000,"modifier":null,"modifiedTime":null,"persistStatus":"nrm","promptMessage":null,"orderId":"040pnM4EHJ4dzuEqtgxG","orderItemId":"0MVKo2c7xOvjDbQmC2op","parentRowNum":"20","parentGoodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","parentGoodsCode":"301020000049","parentGoodsName":"小雅AI音箱旗舰版_石墨绿","rowNum":"20","goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","goodsCode":"301020000049","goodsName":"小雅AI音箱旗舰版_石墨绿","goodsImg":"/group1/M00/00/00/rBFAIV0wmbyASJn2AAE4-1jmRp4811.jpg","isGift":0,"productLineId":"13c512df-ad18-48e5-b75d-166a534cc410","rowWeight":0E-8,"weight":null,"rowNetWeight":0E-8,"netWeight":null,"weightUnitId":null,"weightUnitCode":null,"weightUnitName":null,"rowVolume":0E-8,"volume":null,"volumeUnitId":null,"volumeUnitCode":null,"volumeUnitName":null,"orderNum":5.00000000,"orderNumUnitId":"UNIT-12","orderNumUnitCode":"EA","orderNumUnitName":"个","mainNum":5.00000000,"mainNumUnitId":"UNIT-12","mainNumUnitCode":"EA","mainNumUnitName":"个","conversionRate":1.00000000,"basePrice":null,"salePrice":2689.00000000,"amount":13445.00000000,"dealPrice":2689.00000000,"dealAmount":13445.00000000,"currency":null,"planDeliveryDate":1584187053000,"deliveryInvOrgId":"ebcd635d-237e-4a15-819c-3983ac49436f","deliveryWarehouseId":null,"baseGoodsOptId":null,"baseGoodsOptVals":null,"baseGoodsOptValue":null,"version":1,"originalGoodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","childGoodsQty":1.00000000,"projectId":null,"supplierId":null,"srcOrderCode":null,"srcOrderId":null,"srcOrderItemId":null,"srcOrderItemBomId":null,"srcReqOrderCode":"REQ20200318000009","goodsSupplement":0,"srcReqOrderId":"0GWSDyo52GFam6Z679Qs","srcReqOrderItemId":null,"srcReqOrderItemBomId":null,"existingNum":null,"ext01":null,"ext02":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null,"deliveryInvOrgCode":null,"deliveryInvOrgName":null,"deliveryWarehouseCode":null,"deliveryWarehouseName":null,"goodsSupplementPrice":null,"costPrice":null,"supplierPrice":null,"supplierCode":null,"supplierName":null,"logisticsId":null,"logisticsCode":null,"logisticsName":null,"deliveryNum":null,"stockInNum":null,"stockOutNum":null,"returnNum":null,"refundNum":null,"signNum":null,"replenishNum":null,"coordinateNum":null,"isClose":0,"closeReason":null,"isDeClose":0,"isOutClose":null,"offsetAmount":null,"settleFinancialOrgId":"e53fc87e-1a16-4a2b-978c-63bfd14fd88b","settleFinancialOrgCode":"1101","settleFinancialOrgName":"上海证大喜马拉雅网络科技有限公司","remark":null}],"orderPromRels":[],"orderAttachments":[],"logisticsId":null,"logisticsCode":null,"logisticsName":null,"logisticsBillCode":null,"originalOrderCode":null,"totalReturnAmount":null,"returnReasonId":null,"returnReasonCode":null,"returnReasonName":null,"accountPeriodId":"a1ee592c-4412-42dc-8cee-94d2ac8aa355","accountPeriodCode":"001","accountPeriodName":"001","superiorCustomerId":null,"superiorCustomerCode":null,"superiorCustomerName":null,"totalGoodsSuppleAmount":0E-8,"orderCorrelationMoney":null,"flushSelected":null,"contractTypeId":null,"ext01Id":null,"ext01Code":null,"ext01Name":null,"ext02Id":null,"ext02Code":null,"ext02Name":null,"ext03":null,"ext04":null,"ext05":null,"ext06":null,"ext07":null,"ext08":null,"ext09":null,"ext10":null,"ext11":null,"ext12":null,"ext13":null,"ext14":null,"ext15":null,"goodsOutStyleId":null,"goodsOutStyleCode":null,"goodsOutStyleName":null,"isBomCalcPrice":null,"underPaymentModeId":null,"underPaymentModeCode":null,"underPaymentModeName":null}', 'User': 'Manager', 'DependCase': 'create_sales_order', 'RelevanceList': '', 'IsDepend': ''}

send_request(data)
