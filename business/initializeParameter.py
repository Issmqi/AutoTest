import setupMain
import json
from jsonpath import jsonpath
from log import Log
log=Log()

def ini_parameter(dependCase,relevanceList,parameter):
    '''

    :param dependCase: 依赖的caseName str
    :param relevanceList: 依赖的关键字 list
    :param parameter: 请求参数 str
    :return:
    '''
    param=json.loads(parameter)
    path=setupMain.json_result_path+dependCase+'_result.json'
    print(path)
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
        for relevance_data in relevanceList:#遍历relevanceList中的依赖关系dict
            if isinstance(relevance_data,dict):
                for key in relevance_data:
                    this_key=key
                    relevance_key=relevance_data[this_key]
                    if relevance_key in data:
                        param[this_key]=jsonpath(data,'$..%s'%relevance_key)[0]
                else:
                    log.error('参数依赖关键字%s在关联结果中找不到')
            else:log.error('依赖关系不为dict')


        print('更新后params是：',param)
        return json.dumps(param)


relevanceCase='create_sales_order'
relevanceKeys=[{"ids":"id"}]
# param='{"ids":"02R6zxnuQ30MkkRoltEu",search_AUTH_APPCODE":"saleorder"}'
# param_dict=json.loads(param)
param_dict={
	"ids": "02R6zxnuQ30MkkRoltEu",
	"search_AUTH_APPCODE ":"saleorder"
}
ini_parameter(relevanceCase,relevanceKeys,param_dict)

