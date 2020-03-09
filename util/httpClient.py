import json
from jsonpath import jsonpath
from readConfig import ReadConfig
from log import Log

import login
import requests
import time


log=Log()
readConfig=ReadConfig()
# executeSql=ExecuteSQL()


class HttpClient:

    def __init__(self,request_data):

        self.host=ReadConfig().get_config("HTTP","host")

        self.manager_session = login.manager_login()
        self.customer_01_session = login.customer_01_login()
        self.customer_02_session = login.customer_02_login()

        self.sql=request_data['Sql']
        self.caseid = int(request_data['CaseId'])
        self.casename = request_data['CaseName']
        self.user = request_data['User']
        self.headers=request_data['Headers']
        self.method = request_data['Method']
        self.path = request_data['Path']
        self.param=request_data['Params']
        self.checkpoint=eval(request_data['CheckPoint'])
        self.correlation=request_data['Correlation']
        self.url=self.host+self.path
        # self.cookies={'buyer_token':self.buyer_token}
        # self.id=requests.get('/api/v1/goods/list/admin/query',data={'goods_name':'新增测试删除'})


    def send_request(self):
        # s=requests.session()

        try:
            # if self.sql !="":
            #     print(self.sql)
            #     executeSql.execute_sql(self.sql)

            h=eval(self.headers)

            if self.param == "":
                params=None
            else:
                params=eval(self.param)

            if h == {"Content-Type":"application/json","charset": "UTF-8"}:
                body=json.dumps(params)
            else:
                body=params


            # if self.param == "":
            #     params = None
            # else:
            #     # params = eval(self.param)
            #     params=self.param

            #
            #
            # if self.headers == "{'Content-Type':'application/json','charset': 'UTF-8'}":
            #     # h = None
            #     h = eval(self.headers)
            #     body=json.dumps(params)
            #     # body=params
            # else:
            #     h = eval(self.headers)
            #     body = params

            if self.user=='Manager':
                re = self.manager_session.request(method=self.method, url=self.url, data=body, headers=h)

            elif self.user=='Customer_01':
                re = self.customer_01_session.request(method=self.method, url=self.url, data=body, headers=h)
            elif self.user=='Customer_02':
                re = self.customer_02_session.request(method=self.method, url=self.url, data=body, headers=h)
            else:
                re=requests.request(method=self.method, url=self.url, data=body, headers=h)


            # result = re.json()
            result=re.text

            print(re.status_code)
            log.info('使用%s方法执行用例%s-%s'%(self.method,self.caseid,self.casename))
            log.info('url是：%s'%self.url)
            log.info('请求参数是：%s'%params)
            log.info('响应结果是：%s'%result)


        except Exception as e:
            log.error(e)


    def assertion(self, result):
        '''通用断言，判断checkpoint'''
        try:
            checkPoint=self.checkpoint
            flag = True
            for key in checkPoint:
                ExpectValue = checkPoint[key]
                ActualValue = jsonpath(result, '$..%s' % key)[0]

                if ExpectValue == ActualValue:
                    flag = flag & True
                else:
                    log.error('检查点%s返回错误，实际是%s'%(key,ActualValue))
                    flag = flag & False
            return flag
        except:
            return False







if __name__ == '__main__':

    # data={'CaseId': 1, 'Designer': '师孟奇', 'CaseName': '企业业务员添加商机报备', 'APIName': '商机报备', 'Path': '/occ-b2b-order/b2b/goods-prepare', 'Method': 'post', 'Params': '{"channelCustId":"2269c49f-669a-4bb7-a63a-2eb7365bc0bd","channelCustName":"贵州喜马拉雅网络科技有限公司-测试","companyName":"企业新增的贵州喜马的测试","tradeRegNo":"000001","cellName":"师孟奇","depPosition":"测试","cellPhone":"13127908386","provinceId":"31","provinceName":"上海市","cityId":"310100000000","cityName":"市辖区","countyId":"310101000000","countyName":"黄浦区","townId":"","townName":"","detailAddress":"test","custNeedDsc":"测试","businessType":1,"businessState":0,"persistStatus":"new","productList":[]}', 'CheckPoint': '{"busiId":"XMLA551WQ73O6EE20190822"}', 'User': 'Manager', 'Correlation': '', 'Active': 'Yes'}
    # s = requests.session()
    # data={'CaseId': 4, 'Designer': '师孟奇', 'CaseName': '企业业务员代客下单', 'APIName': '2B订单', 'Headers': "{'Content-Type':'application/json','charset': 'UTF-8'}", 'Path': '/occ-b2b-order/b2b/order/create-order', 'Method': 'post', 'Params': '{"id":"","creator":None,"createTime":"","modifier":None,"modifiedTime":"","dr":None,"ts":None,"serialnum":None,"orderReceiveAddress":{"orderId":None,"id":None,"creator":None,"dr":"1","receiveAddressId":"a8188818-435b-4f9b-bc26-ff98a5bca778","receiveAddressName":None,"receiver":"黎阳","receiverTel":"","receiverPhone":"19979010823","country":"中国","countryId":"COUNTRY-01","receiverProvince":"贵州省","receiverProvinceId":"52","receiverCity":"贵阳市","receiverCityId":"520100000000","receiverCounty":"观山湖区","receiverCountyid":None,"receiverTown":"世纪城社区服务中心","receiverTownId":"520115400000","receiverAddress":"长岭南路33号天一国际10栋902","receiverZipcode":None,"receiverCountyId":"","persistStatus":"new"},"orderInvoice":{"orderId":None,"id":None,"creator":None,"dr":None,"invoiceId":"f0d8b999-8614-464a-8e50-32e2e69fbfe5","invoiceType":"增值税发票","invoiceContent":None,"invoiceTitle":"贵州喜马拉雅网络科技有限公司","invoiceTaxId":None,"invoiceBank":"中国建设银行股份有限公司贵阳城北支行","invoiceAccount":None,"invoiceSubBank":None,"persistStatus":"new"},"ext01":None,"ext02":None,"ext03":None,"ext04":None,"ext05":None,"ext06":None,"ext07":None,"ext08":None,"ext09":None,"ext10":None,"ext11":None,"ext12":None,"ext13":None,"ext14":None,"ext15":None,"closer":None,"remark":None,"isClose":None,"rejecter":None,"totalNum":"3.00","closeTime":"","isDeClose":None,"orderCode":None,"orderDate":int(time.time()*1000)\n,"saleModel":"01","saleOrgId":"e53fc87e-1a16-4a2b-978c-63bfd14fd88b","billTypeId":"SaleOrder","contractId":None,"costTypeId":None,"currencyId":"7cbc1420-737d-4206-97e3-140ebdbe841f","customerId":"a3456c3b-edaa-4cf8-8dff-29ddc68d0749","promAmount":None,"rejectTime":"","srcOrderId":None,"supplierId":None,"closeReason":None,"logisticsId":None,"orderSource":"02","orderTypeId":"GeneralSale","salesDeptId":"1d5f2aff-5455-4e40-8818-d0e2bbc7e37a","totalAmount":"1590.00","totalVolume":"0.0000","totalWeight":"0.0000","creationTime":"","deliveryDate":int(time.time()*1000),"marketAreaId":None,"offsetAmount":"0.00","rejectReason":None,"settleModeId":None,"srcOrderCode":None,"approveStatus":None,"orderStatusId":"01","srcReqOrderId":None,"approveOpinion":None,"isBomCalcPrice":None,"returnReasonId":None,"salesManagerId":"8e73d0b7-5d0e-4c9d-bcdb-1db337b0b971","totalNetWeight":"0.0000","accountPeriodId":"a1ee592c-4412-42dc-8cee-94d2ac8aa355","goodsOutStyleId":None,"orderStatusCode":None,"orderStatusName":None,"srcReqOrderCode":None,"totalDealAmount":"1590.00","transportModeId":None,"logisticsBillCode":None,"originalOrderCode":None,"receiveCustomerId":"a3456c3b-edaa-4cf8-8dff-29ddc68d0749","totalReturnAmount":None,"superiorCustomerId":None,"underPaymentModeId":None,"maxPreferentialMoney":None,"settleFinancialOrgId":None,"totalGoodsSuppleAmount":"0.00","persistStatus":"new","orderReceiveAddressName":"中国贵州省贵阳市观山湖区世纪城社区服务中心长岭南路33号天一国际10栋902","orderReceiveAddressFirstReceiver":"黎阳","orderReceiveAddressFirstReceiverTel":"19979010823","orderInvoiceName":"贵州喜马拉雅网络科技有限公司","saleOrgName":None,"currencyName":"人民币","customerName":None,"supplierName":None,"logisticsName":None,"orderTypeName":None,"salesDeptName":None,"marketAreaName":None,"settleModeName":None,"salesManagerName":None,"accountPeriodName":"001","transportModeName":None,"receiveCustomerName":None,"superiorCustomerName":None,"settleFinancialOrgName":None,"flushSelected":[],"currencyCode":"CNY","orderItems":[{"id":None,"creator":None,"createTime":"","modifier":None,"modifiedTime":"","dr":None,"ts":"","serialnum":None,"ext01":None,"ext02":None,"ext03":None,"ext04":None,"ext05":None,"ext06":None,"ext07":None,"ext08":None,"ext09":None,"ext10":None,"ext11":None,"ext12":None,"ext13":None,"ext14":None,"ext15":None,"amount":"1590.00","isGift":0,"remark":None,"rowNum":10,"volume":None,"weight":None,"goodsId":"06852e4b-0aad-437e-bcfc-03281ecc8abf","isClose":0,"mainNum":"3.000000","signNum":None,"version":"1","bomSplit":None,"goodsImg":"/group1/M00/00/00/rBFALF0wl3SABFrOAA-1DMFNtAs187.jpg","orderNum":"3.000000","basePrice":"699.000000","dealPrice":"530.000000","goodsCode":"301020000021","goodsName":"小雅AI音箱_红","isDeClose":0,"netWeight":None,"productId":"86f1d65a-18b6-4527-9d14-62c7e79e578e","projectId":None,"promPrice":"530.000000","refundNum":None,"returnNum":None,"rowVolume":0,"rowWeight":0,"salePrice":"530.000000","batchNumId":None,"currencyId":"7cbc1420-737d-4206-97e3-140ebdbe841f","dealAmount":"1590.00","isOptional":"0","isPromGift":None,"promAmount":None,"promotinId":"","srcOrderId":None,"stockInNum":None,"supplierId":None,"batchCodeId":None,"deliveryNum":None,"existingNum":None,"isDiscounts":None,"logisticsId":None,"priceTypeId":None,"stockOutNum":None,"availableNum":None,"batchNumCode":None,"batchNumName":None,"offsetAmount":None,"replenishNum":None,"returnTypeId":None,"rowNetWeight":0,"srcOrderCode":None,"volumeUnitId":None,"weightUnitId":None,"coordinateNum":None,"isServiceType":None,"mainNumUnitId":"UNIT-12","priceTypeCode":None,"priceTypeName":None,"productLineId":"13c512df-ad18-48e5-b75d-166a534cc410","srcReqOrderId":None,"supplierPrice":None,"baseGoodsOptId":None,"conversionRate":"1.000000","orderNumUnitId":"UNIT-12","returnReasonId":None,"srcOrderItemId":None,"goodsCategoryId":None,"goodsSupplement":0,"originalGoodsId":"06852e4b-0aad-437e-bcfc-03281ecc8abf","srcReqOrderCode":None,"deliveryInvOrgId":"ebcd635d-237e-4a15-819c-3983ac49436f","goodsDisplayName":"小雅AI音箱_红","planDeliveryDate":int(time.time()*1000),"baseGoodsOptValue":None,"srcReqOrderItemId":None,"totalReturnAmount":None,"srcOrderBilltypeId":None,"srcOrderTrantypeId":None,"deliveryWarehouseId":None,"supplementAccountId":None,"goodsSupplementPrice":None,"settleFinancialOrgId":"e53fc87e-1a16-4a2b-978c-63bfd14fd88b","persistStatus":"new","productName":None,"projectName":None,"currencyName":"人民币","promotinName":"","supplierName":None,"logisticsName":None,"volumeUnitName":None,"weightUnitName":None,"mainNumUnitName":"个","productLineName":"喜日","orderNumUnitName":"个","goodsCategoryName":None,"deliveryInvOrgName":"上海喜日电子科技有限公司","deliveryWarehouseName":None,"settleFinancialOrgName":"上海喜马拉雅科技有限公司","currencyCode":"CNY","creationTime":"","description":""}],"orderItemBoms":[{"id":None,"creator":None,"createTime":"","modifier":None,"modifiedTime":"","dr":None,"ts":"","serialnum":None,"settleFinancialOrgId":"e53fc87e-1a16-4a2b-978c-63bfd14fd88b","ext01":None,"ext02":None,"ext03":None,"ext04":None,"ext05":None,"ext06":None,"ext07":None,"ext08":None,"ext09":None,"ext10":None,"ext11":None,"ext12":None,"ext13":None,"ext14":None,"ext15":None,"amount":"1590.00","isGift":0,"remark":None,"rowNum":10,"volume":None,"weight":None,"goodsId":"06852e4b-0aad-437e-bcfc-03281ecc8abf","isClose":0,"mainNum":"3.000000","signNum":"","version":"1","currency":None,"goodsImg":"/group1/M00/00/00/rBFALF0wl3SABFrOAA-1DMFNtAs187.jpg","orderNum":"3.000000","parentRowNum":10,"basePrice":"699.000000","costPrice":None,"dealPrice":"530.000000","goodsCode":"301020000021","goodsName":"小雅AI音箱_红","isDeClose":0,"netWeight":None,"projectId":None,"refundNum":"","returnNum":"","rowVolume":0,"rowWeight":0,"salePrice":"530.000000","dealAmount":"1590.00","isOutClose":None,"srcOrderId":None,"stockInNum":"","supplierId":None,"closeReason":None,"deliveryNum":"","existingNum":"","logisticsId":None,"stockOutNum":"","offsetAmount":"","replenishNum":"","rowNetWeight":0,"srcOrderCode":None,"volumeUnitId":None,"weightUnitId":None,"childGoodsQty":1,"coordinateNum":"","goodsSupplementPrice":"","mainNumUnitId":"UNIT-12","parentGoodsId":"06852e4b-0aad-437e-bcfc-03281ecc8abf","productLineId":"13c512df-ad18-48e5-b75d-166a534cc410","srcReqOrderId":None,"baseGoodsOptId":None,"conversionRate":"1.000000","orderNumUnitId":"UNIT-12","srcOrderItemId":None,"goodsSupplement":0,"originalGoodsId":"06852e4b-0aad-437e-bcfc-03281ecc8abf","parentGoodsCode":"301020000021","parentGoodsName":"小雅AI音箱_红","srcReqOrderCode":None,"deliveryInvOrgId":"ebcd635d-237e-4a15-819c-3983ac49436f","planDeliveryDate":int(time.time()*1000),"baseGoodsOptValue":None,"deliveryWarehouseId":None,"srcOrderItemBomId":None,"srcReqOrderItemBomId":None,"srcReqOrderItemId":None,"bomSplit":None,"productId":"86f1d65a-18b6-4527-9d14-62c7e79e578e","promPrice":"530.000000","batchNumId":None,"currencyId":None,"isOptional":"0","isPromGift":None,"promAmount":None,"promotinId":None,"batchCodeId":None,"isDiscounts":None,"priceTypeId":None,"availableNum":None,"batchNumCode":None,"batchNumName":None,"returnTypeId":None,"isServiceType":None,"priceTypeCode":None,"priceTypeName":None,"supplierPrice":None,"returnReasonId":None,"goodsCategoryId":None,"goodsDisplayName":"小雅AI音箱_红","totalReturnAmount":None,"srcOrderBilltypeId":None,"srcOrderTrantypeId":None,"supplementAccountId":None,"persistStatus":"new","settleFinancialOrgName":"上海喜马拉雅科技有限公司","currencyName":None,"projectName":None,"supplierName":None,"logisticsName":None,"volumeUnitName":None,"weightUnitName":None,"mainNumUnitName":"个","productLineName":"喜日","orderNumUnitName":"个","deliveryInvOrgName":"上海喜日电子科技有限公司","deliveryWarehouseName":None,"productName":None,"promotinName":None,"goodsCategoryName":None,"creationTime":"","description":""}]}', 'CheckPoint': '{"billTypeName":"销售订单"}', 'User': 'Manager', 'Correlation': '', 'Active': 'Yes', 'Sql': ''}
    # data={'CaseId': 1, 'Designer': '师孟奇', 'CaseName': '企业业务员代客下单', 'APIName': '2B订单', 'Headers': "{'Content-Type':'application/json','charset': 'UTF-8'}", 'Path': '/occ-b2b-order/b2b/order/create-order', 'Method': 'post', 'Params': '{"id":"","creator":None,"createTime":"","modifier":None,"modifiedTime":"","dr":None,"ts":None,"serialnum":None,"orderReceiveAddress":{"orderId":None,"id":None,"creator":None,"dr":"1","receiveAddressId":"8fe72429-8c25-4a92-b508-ded3abcc37d2","receiveAddressName":None,"receiver":"周佳","receiverTel":"13518639999","receiverPhone":"13518639999","country":"中国","countryId":"COUNTRY-01","receiverProvince":"山东省","receiverProvinceId":"37","receiverCity":"淄博市","receiverCityId":"370300000000","receiverCounty":"张店区","receiverCountyId":"370303000000","receiverTown":"","receiverTownId":"","receiverAddress":"山东淄博张店联通路东方之珠","receiverZipcode":None,"persistStatus":"new"},"orderInvoice":{"orderId":None,"id":None,"creator":None,"dr":None,"invoiceId":"5df5c54a-bef3-4fab-9ff8-2d9dad5d9b5f","invoiceType":"增值税发票","invoiceContent":None,"invoiceTitle":"山东春和景明文化传播有限公司","invoiceTaxId":None,"invoiceBank":"中国农业银行股份有限公司淄博东方分理处","invoiceAccount":None,"invoiceSubBank":None,"persistStatus":"new"},"ext01":None,"ext02":None,"ext03":None,"ext04":None,"ext05":None,"ext06":None,"ext07":None,"ext08":None,"ext09":None,"ext10":None,"ext11":None,"ext12":None,"ext13":None,"ext14":None,"ext15":None,"closer":None,"remark":None,"isClose":None,"rejecter":None,"totalNum":"30.00","closeTime":"","isDeClose":None,"orderCode":None,"orderDate":1583746129053,"saleModel":"01","saleOrgId":"e53fc87e-1a16-4a2b-978c-63bfd14fd88b","billTypeId":"SaleOrder","contractId":None,"costTypeId":None,"currencyId":"7cbc1420-737d-4206-97e3-140ebdbe841f","customerId":"1878731f-0aca-4e9b-8b27-5944910f1509","promAmount":None,"rejectTime":"","srcOrderId":None,"supplierId":None,"closeReason":None,"logisticsId":None,"orderSource":"02","orderTypeId":"0yDZwkYyas4KNNKM4RNF","salesDeptId":"1d5f2aff-5455-4e40-8818-d0e2bbc7e37a","totalAmount":"30.00","totalVolume":"0.0000","totalWeight":"0.0000","creationTime":"","deliveryDate":1583746129049,"marketAreaId":None,"offsetAmount":None,"rejectReason":None,"settleModeId":None,"srcOrderCode":None,"sycnNCStatus":None,"approveStatus":None,"orderStatusId":"01","srcReqOrderId":None,"sycnOutStatus":None,"approveOpinion":None,"isBomCalcPrice":None,"returnReasonId":None,"salesManagerId":"8e73d0b7-5d0e-4c9d-bcdb-1db337b0b971","totalNetWeight":"0.0000","accountPeriodId":"a1ee592c-4412-42dc-8cee-94d2ac8aa355","goodsOutStyleId":None,"orderStatusCode":None,"orderStatusName":None,"srcReqOrderCode":None,"totalDealAmount":"30.00","transportModeId":None,"logisticsBillCode":None,"originalOrderCode":None,"receiveCustomerId":"1878731f-0aca-4e9b-8b27-5944910f1509","totalReturnAmount":None,"superiorCustomerId":None,"underPaymentModeId":None,"maxPreferentialMoney":None,"settleFinancialOrgId":None,"totalGoodsSuppleAmount":"0.00","persistStatus":"new","orderReceiveAddressName":"中国山东省淄博市张店区山东淄博张店联通路东方之珠","orderReceiveAddressFirstReceiver":"周佳","orderReceiveAddressFirstReceiverTel":"13518639999","orderInvoiceName":"山东春和景明文化传播有限公司","ext01Code":None,"ext01Name":None,"ext02Name":None,"saleOrgName":None,"currencyName":"人民币","customerName":None,"supplierName":None,"logisticsName":None,"orderTypeName":None,"salesDeptName":None,"marketAreaName":None,"settleModeName":None,"salesManagerName":None,"accountPeriodName":"001","transportModeName":None,"receiveCustomerName":None,"superiorCustomerName":None,"settleFinancialOrgName":None,"flushSelected":[],"currencyCode":"CNY","orderItems":[{"id":None,"creator":None,"createTime":"","modifier":None,"modifiedTime":"","dr":None,"ts":"","serialnum":None,"ext01":None,"ext02":None,"ext03":None,"ext04":None,"ext05":None,"ext06":None,"ext07":None,"ext08":None,"ext09":None,"ext10":None,"ext11":None,"ext12":None,"ext13":None,"ext14":None,"ext15":None,"amount":"0.00","isGift":0,"remark":None,"rowNum":10,"volume":None,"weight":None,"goodsId":"0GYRD2D5Q5AhyC898QVf","isClose":0,"mainNum":"10","signNum":None,"version":"1","bomSplit":None,"goodsImg":None,"orderNum":"10.00000000","basePrice":None,"dealPrice":"1.000000","goodsCode":"231010100002","goodsName":"思想史","isDeClose":0,"netWeight":None,"productId":None,"projectId":None,"promPrice":None,"refundNum":None,"returnNum":None,"rowVolume":0,"rowWeight":0,"salePrice":"1.000000","batchNumId":None,"currencyId":"7cbc1420-737d-4206-97e3-140ebdbe841f","dealAmount":"10.00","isOptional":"0","isPromGift":None,"promAmount":None,"promotinId":"","srcOrderId":None,"stockInNum":None,"supplierId":None,"batchCodeId":None,"deliveryNum":None,"existingNum":None,"isDiscounts":None,"logisticsId":None,"priceTypeId":None,"stockOutNum":None,"availableNum":None,"batchNumCode":None,"batchNumName":None,"offsetAmount":None,"replenishNum":None,"returnTypeId":None,"rowNetWeight":0,"srcOrderCode":None,"volumeUnitId":None,"weightUnitId":None,"coordinateNum":None,"isServiceType":None,"mainNumUnitId":"f6d2b99b-a213-4d30-bdc0-7cf968238c3b","priceTypeCode":None,"priceTypeName":None,"productLineId":"f9535deb-a1ff-4a1b-8db1-4ffdd118b46f","srcReqOrderId":None,"supplierPrice":None,"baseGoodsOptId":None,"conversionRate":"1.000000","orderNumUnitId":"f6d2b99b-a213-4d30-bdc0-7cf968238c3b","returnReasonId":None,"srcOrderItemId":None,"goodsCategoryId":None,"goodsSupplement":0,"originalGoodsId":"0GYRD2D5Q5AhyC898QVf","srcReqOrderCode":None,"deliveryInvOrgId":"abd7cf79-511d-4307-9bbd-d288b18d0ef9","goodsDisplayName":"思想史","planDeliveryDate":1583746179254,"baseGoodsOptValue":None,"srcReqOrderItemId":None,"totalReturnAmount":None,"srcOrderBilltypeId":None,"srcOrderTrantypeId":None,"deliveryWarehouseId":None,"supplementAccountId":None,"goodsSupplementPrice":None,"settleFinancialOrgId":"e53fc87e-1a16-4a2b-978c-63bfd14fd88b","persistStatus":"new","productName":None,"projectName":None,"currencyName":"人民币","promotinName":"","supplierName":None,"logisticsName":None,"volumeUnitName":None,"weightUnitName":None,"mainNumUnitName":"册","productLineName":"外部供应商","orderNumUnitName":"册","goodsCategoryName":None,"deliveryInvOrgName":"西安喜马拉雅网络科技有限公司","deliveryWarehouseName":None,"settleFinancialOrgName":"上海证大喜马拉雅网络科技有限公司","currencyCode":"CNY","creationTime":"","description":""},{"id":None,"creator":None,"createTime":"","modifier":None,"modifiedTime":"","dr":None,"ts":"","serialnum":None,"ext01":None,"ext02":None,"ext03":None,"ext04":None,"ext05":None,"ext06":None,"ext07":None,"ext08":None,"ext09":None,"ext10":None,"ext11":None,"ext12":None,"ext13":None,"ext14":None,"ext15":None,"amount":"0.00","isGift":0,"remark":None,"rowNum":20,"volume":None,"weight":None,"goodsId":"0EatunENVoWI2nQQaK9m","isClose":0,"mainNum":"20","signNum":None,"version":"1","bomSplit":None,"goodsImg":None,"orderNum":"20.00000000","basePrice":None,"dealPrice":"1.000000","goodsCode":"231020200007","goodsName":"风雪将至","isDeClose":0,"netWeight":None,"productId":None,"projectId":None,"promPrice":None,"refundNum":None,"returnNum":None,"rowVolume":0,"rowWeight":0,"salePrice":"1.000000","batchNumId":None,"currencyId":"7cbc1420-737d-4206-97e3-140ebdbe841f","dealAmount":"20.00","isOptional":"0","isPromGift":None,"promAmount":None,"promotinId":"","srcOrderId":None,"stockInNum":None,"supplierId":None,"batchCodeId":None,"deliveryNum":None,"existingNum":None,"isDiscounts":None,"logisticsId":None,"priceTypeId":None,"stockOutNum":None,"availableNum":None,"batchNumCode":None,"batchNumName":None,"offsetAmount":None,"replenishNum":None,"returnTypeId":None,"rowNetWeight":0,"srcOrderCode":None,"volumeUnitId":None,"weightUnitId":None,"coordinateNum":None,"isServiceType":None,"mainNumUnitId":"f6d2b99b-a213-4d30-bdc0-7cf968238c3b","priceTypeCode":None,"priceTypeName":None,"productLineId":"f9535deb-a1ff-4a1b-8db1-4ffdd118b46f","srcReqOrderId":None,"supplierPrice":None,"baseGoodsOptId":None,"conversionRate":"1.000000","orderNumUnitId":"f6d2b99b-a213-4d30-bdc0-7cf968238c3b","returnReasonId":None,"srcOrderItemId":None,"goodsCategoryId":None,"goodsSupplement":0,"originalGoodsId":"0EatunENVoWI2nQQaK9m","srcReqOrderCode":None,"deliveryInvOrgId":"abd7cf79-511d-4307-9bbd-d288b18d0ef9","goodsDisplayName":"风雪将至","planDeliveryDate":1583746201231,"baseGoodsOptValue":None,"srcReqOrderItemId":None,"totalReturnAmount":None,"srcOrderBilltypeId":None,"srcOrderTrantypeId":None,"deliveryWarehouseId":None,"supplementAccountId":None,"goodsSupplementPrice":None,"settleFinancialOrgId":"e53fc87e-1a16-4a2b-978c-63bfd14fd88b","persistStatus":"new","productName":None,"projectName":None,"currencyName":"人民币","promotinName":"","supplierName":None,"logisticsName":None,"volumeUnitName":None,"weightUnitName":None,"mainNumUnitName":"册","productLineName":"外部供应商","orderNumUnitName":"册","goodsCategoryName":None,"deliveryInvOrgName":"西安喜马拉雅网络科技有限公司","deliveryWarehouseName":None,"settleFinancialOrgName":"上海证大喜马拉雅网络科技有限公司","currencyCode":"CNY","creationTime":"","description":""}],"orderItemBoms":[{"id":None,"creator":None,"createTime":"","modifier":None,"modifiedTime":"","dr":None,"ts":"","serialnum":None,"settleFinancialOrgId":"e53fc87e-1a16-4a2b-978c-63bfd14fd88b","ext01":None,"ext02":None,"ext03":None,"ext04":None,"ext05":None,"ext06":None,"ext07":None,"ext08":None,"ext09":None,"ext10":None,"ext11":None,"ext12":None,"ext13":None,"ext14":None,"ext15":None,"amount":"0.00","isGift":0,"remark":None,"rowNum":10,"volume":None,"weight":None,"goodsId":"0GYRD2D5Q5AhyC898QVf","isClose":0,"mainNum":"10","signNum":"","version":"1","currency":None,"goodsImg":None,"orderNum":"10","parentRowNum":10,"basePrice":"","costPrice":None,"dealPrice":"0.000000","goodsCode":"231010100002","goodsName":"思想史","isDeClose":0,"netWeight":None,"projectId":None,"refundNum":"","returnNum":"","rowVolume":0,"rowWeight":0,"salePrice":"1.000000","dealAmount":"0.00","isOutClose":None,"srcOrderId":None,"stockInNum":"","supplierId":None,"closeReason":None,"deliveryNum":"","existingNum":"","logisticsId":None,"stockOutNum":"","offsetAmount":"","replenishNum":"","rowNetWeight":0,"srcOrderCode":None,"volumeUnitId":None,"weightUnitId":None,"childGoodsQty":1,"coordinateNum":"","goodsSupplementPrice":"","mainNumUnitId":"f6d2b99b-a213-4d30-bdc0-7cf968238c3b","parentGoodsId":"0GYRD2D5Q5AhyC898QVf","productLineId":"f9535deb-a1ff-4a1b-8db1-4ffdd118b46f","srcReqOrderId":None,"baseGoodsOptId":None,"conversionRate":"1.000000","orderNumUnitId":"f6d2b99b-a213-4d30-bdc0-7cf968238c3b","srcOrderItemId":None,"goodsSupplement":0,"originalGoodsId":"0GYRD2D5Q5AhyC898QVf","parentGoodsCode":"231010100002","parentGoodsName":"思想史","srcReqOrderCode":None,"deliveryInvOrgId":"abd7cf79-511d-4307-9bbd-d288b18d0ef9","planDeliveryDate":1583746179000,"baseGoodsOptValue":None,"deliveryWarehouseId":None,"srcOrderItemBomId":None,"srcReqOrderItemBomId":None,"srcReqOrderItemId":None,"bomSplit":None,"productId":None,"promPrice":None,"batchNumId":None,"currencyId":None,"isOptional":"0","isPromGift":None,"promAmount":None,"promotinId":None,"batchCodeId":None,"isDiscounts":None,"priceTypeId":None,"availableNum":None,"batchNumCode":None,"batchNumName":None,"returnTypeId":None,"isServiceType":None,"priceTypeCode":None,"priceTypeName":None,"supplierPrice":None,"returnReasonId":None,"goodsCategoryId":None,"goodsDisplayName":"思想史","totalReturnAmount":None,"srcOrderBilltypeId":None,"srcOrderTrantypeId":None,"supplementAccountId":None,"persistStatus":"new","settleFinancialOrgName":"上海证大喜马拉雅网络科技有限公司","currencyName":None,"projectName":None,"supplierName":None,"logisticsName":None,"volumeUnitName":None,"weightUnitName":None,"mainNumUnitName":"册","productLineName":"外部供应商","orderNumUnitName":"册","deliveryInvOrgName":"西安喜马拉雅网络科技有限公司","deliveryWarehouseName":None,"productName":None,"promotinName":None,"goodsCategoryName":None,"creationTime":"","description":""},{"id":None,"creator":None,"createTime":"","modifier":None,"modifiedTime":"","dr":None,"ts":"","serialnum":None,"settleFinancialOrgId":"e53fc87e-1a16-4a2b-978c-63bfd14fd88b","ext01":None,"ext02":None,"ext03":None,"ext04":None,"ext05":None,"ext06":None,"ext07":None,"ext08":None,"ext09":None,"ext10":None,"ext11":None,"ext12":None,"ext13":None,"ext14":None,"ext15":None,"amount":"0.00","isGift":0,"remark":None,"rowNum":20,"volume":None,"weight":None,"goodsId":"0EatunENVoWI2nQQaK9m","isClose":0,"mainNum":"20","signNum":"","version":"1","currency":None,"goodsImg":None,"orderNum":"20","parentRowNum":20,"basePrice":"","costPrice":None,"dealPrice":"0.000000","goodsCode":"231020200007","goodsName":"风雪将至","isDeClose":0,"netWeight":None,"projectId":None,"refundNum":"","returnNum":"","rowVolume":0,"rowWeight":0,"salePrice":"1.000000","dealAmount":"0.00","isOutClose":None,"srcOrderId":None,"stockInNum":"","supplierId":None,"closeReason":None,"deliveryNum":"","existingNum":"","logisticsId":None,"stockOutNum":"","offsetAmount":"","replenishNum":"","rowNetWeight":0,"srcOrderCode":None,"volumeUnitId":None,"weightUnitId":None,"childGoodsQty":1,"coordinateNum":"","goodsSupplementPrice":"","mainNumUnitId":"f6d2b99b-a213-4d30-bdc0-7cf968238c3b","parentGoodsId":"0EatunENVoWI2nQQaK9m","productLineId":"f9535deb-a1ff-4a1b-8db1-4ffdd118b46f","srcReqOrderId":None,"baseGoodsOptId":None,"conversionRate":"1.000000","orderNumUnitId":"f6d2b99b-a213-4d30-bdc0-7cf968238c3b","srcOrderItemId":None,"goodsSupplement":0,"originalGoodsId":"0EatunENVoWI2nQQaK9m","parentGoodsCode":"231020200007","parentGoodsName":"风雪将至","srcReqOrderCode":None,"deliveryInvOrgId":"abd7cf79-511d-4307-9bbd-d288b18d0ef9","planDeliveryDate":1583746201000,"baseGoodsOptValue":None,"deliveryWarehouseId":None,"srcOrderItemBomId":None,"srcReqOrderItemBomId":None,"srcReqOrderItemId":None,"bomSplit":None,"productId":None,"promPrice":None,"batchNumId":None,"currencyId":None,"isOptional":"0","isPromGift":None,"promAmount":None,"promotinId":None,"batchCodeId":None,"isDiscounts":None,"priceTypeId":None,"availableNum":None,"batchNumCode":None,"batchNumName":None,"returnTypeId":None,"isServiceType":None,"priceTypeCode":None,"priceTypeName":None,"supplierPrice":None,"returnReasonId":None,"goodsCategoryId":None,"goodsDisplayName":"风雪将至","totalReturnAmount":None,"srcOrderBilltypeId":None,"srcOrderTrantypeId":None,"supplementAccountId":None,"persistStatus":"new","settleFinancialOrgName":"上海证大喜马拉雅网络科技有限公司","currencyName":None,"projectName":None,"supplierName":None,"logisticsName":None,"volumeUnitName":None,"weightUnitName":None,"mainNumUnitName":"册","productLineName":"外部供应商","orderNumUnitName":"册","deliveryInvOrgName":"西安喜马拉雅网络科技有限公司","deliveryWarehouseName":None,"productName":None,"promotinName":None,"goodsCategoryName":None,"creationTime":"","description":""}]}', 'CheckPoint': '{"billTypeName":"销售订单"}', 'User': 'Manager', 'Correlation': '', 'Active': 'Yes', 'Sql': ''}
    data={'CaseId': 2, 'Designer': '师孟奇', 'CaseName': '新增形态转换订单', 'APIName': '形态转换', 'Headers': '{"Content-Type","application/json","charset": "UTF-8"}', 'Path': '/occ-stock/stock/form-changes/add', 'Method': 'post', 'Params': '{"formChangeCode":None,"formChangeDate":1583424000000,"stockOrgId":"abd7cf79-511d-4307-9bbd-d288b18d0ef9","stockOrgName":None,"stockOrgCode":None,"deptId":"0K1ovYvAl1Pk00oCRPjV","deptName":None,"deptCode":None,"businessUserId":"0mWG6nOSCxjsi1zoKEYs","businessUserCode":None,"businessUserName":None,"remark":"自动化测试新增","state":"0","beforeChangeWarehouseId":"1001ZZ100000000DPAP4","beforeChangeWarehouseCode":None,"beforeChangeWarehouseName":None,"afterChangeWarehouseId":"1001ZZ100000000DPAP6","afterChangeWarehouseCode":None,"afterChangeWarehouseName":None,"otherOutboundOrders":None,"otherWarehouseEntry":None,"ifSlotManage":"0","otherOutStockCode":None,"otherInStockCode":None,"persistStatus":"new","purchaseType":"InnerPurchase","formChangeItems":[{"lineNumber":10,"groupNumber":"1","goodsName":"小雅AI音箱旗舰版_石墨绿","goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","goodsCode":"301020000049","goodsUnitId":"UNIT-12","goodsUnitCode":"EA","goodsUnitName":"个","changeTypeId":None,"changeTypeCode":"beforeFormChange","changeTypeName":None,"goodsAmount":"5","remark":None,"batchNumId":None,"batchNumCode":None,"batchNumName":None,"goodsPositionId":None,"goodsPositionCode":None,"goodsPositionName":None,"changeDate":"","srcBillCode":None,"srcBillBcode":None,"srcBillType":None,"firstBillCode":None,"firstBillBcode":None,"firstBillType":None,"enableBatchNumberManage":"0","enableBatchNoManage":"0","enableInvStatusManage":"0","productLineId":"13c512df-ad18-48e5-b75d-166a534cc410","productId":"996cc839-60e8-4500-82c6-9a7c7b95646d","persistStatus":"new"},{"lineNumber":20,"groupNumber":"1","goodsName":"小雅AI音箱旗舰版_石墨绿","goodsId":"03e77ae0-469d-4d8a-ba34-733c2ada3749","goodsCode":"301020000049","goodsUnitId":"UNIT-12","goodsUnitCode":"EA","goodsUnitName":"个","changeTypeId":None,"changeTypeCode":"afterFormChange","changeTypeName":None,"goodsAmount":"5","remark":None,"batchNumId":None,"batchNumCode":None,"batchNumName":None,"goodsPositionId":None,"goodsPositionCode":None,"goodsPositionName":None,"changeDate":"","srcBillCode":None,"srcBillBcode":None,"srcBillType":None,"firstBillCode":None,"firstBillBcode":None,"firstBillType":None,"enableBatchNumberManage":"0","enableBatchNoManage":"0","enableInvStatusManage":"0","productLineId":"13c512df-ad18-48e5-b75d-166a534cc410","productId":"996cc839-60e8-4500-82c6-9a7c7b95646d","persistStatus":"new"}]}', 'CheckPoint': '{"message":"新增成功"}', 'User': 'Manager', 'Correlation': '', 'Active': 'Yes', 'Sql': ''}

    hc=HttpClient(data)
    re=hc.send_request()
    hc.assertion(re)

