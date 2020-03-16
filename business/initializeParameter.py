import setupMain
import json
import jsonpath
from log import Log
log=Log()

def ini_parameter(relevanceCase,relevanceKeys,param):
    '''

    :param RelevanceCase: 依赖的caseName str
    :param RelevanceKey: 依赖的关键字 list
    :param param: 请求参数 dict
    :return:
    '''

    path=setupMain.json_result_path+relevanceCase+'_result.json'
    print(path)
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
        for key in relevanceKeys:
            if key in data:
                relevance_value=jsonpath.jsonpath(data,'$..%s'%key)
                param[key]=relevance_value
            else:
                log.error('参数依赖关键字%s在关联结果中找不到')
        print('更新后params是：',param)


relevanceCase='create_sales_order'
relevanceKeys=['ids']
# param='{"ids":"02R6zxnuQ30MkkRoltEu",search_AUTH_APPCODE":"saleorder"}'
# param_dict=json.loads(param)
param_dict={
	"ids": "02R6zxnuQ30MkkRoltEu",
	"search_AUTH_APPCODE ":"saleorder"
}
ini_parameter(relevanceCase,relevanceKeys,param_dict)

