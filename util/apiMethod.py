import json
import os
import requests
import simplejson
from log import Log
log=Log()

def post(url,header,data,cookie):
    '''
    封装post请求
    :param header: 请求头
    :param url: 接口路径
    :param data: 请求参数
    :return:
    '''

    h = eval(header)
    if not data:
        param=None
    else:
        param=json.loads(data)#str转换pythondict

    if h == {"Content-Type": "application/json", "charset": "UTF-8"}:
        body = json.dumps(param)
    else:
        body=param


    response=requests.post(url=url,headers=h,data=body,cookies=cookie)
    timing=response.elapsed.total_seconds()
    log.info('响应时间为%ss'%timing)
    try:
        if response.status_code!=200:
            return response.status_code,response.text
        else:
            return response.status_code,response.json()

    except json.decoder.JSONDecodeError:
        return response.status_code
    except simplejson.errors.JSONDecodeError:
        return response.status_code
    except Exception as e:
        log.war('ERROR')
        log.error(e)

def post_2(url,param_type,param,cookie,header):
    # header= {"Content-Type": "application/json", "charset": "UTF-8"}
    header=eval(header)

    if not param:
        param_dict=None
    else:
        param_dict=json.loads(param)

    if param_type=='json':
        data=json.dumps(param_dict)
        response = requests.post(url=url, headers=header, data=data, cookies=cookie)
    elif param_type=='form_data':
        response = requests.post(url=url, headers=header, data=param_dict, cookies=cookie)
    elif param_type=='parameter':
        response = requests.post(url=url, headers=header, params=param_dict, cookies=cookie)
    else:
        response=None
        log.error('请求类型不存在')

    timing = response.elapsed.total_seconds()
    log.info('响应时间为%ss' % timing)
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







def get(header,url,data):
    '''

    :param header: 请求头
    :param url: 接口路径
    :param data: 请求参数
    :return:
    '''
    response=requests.get(url=url,headers=header,params=data)
    if response.status_code==301:
        response=requests.get(url=response.headers['location'])
    try:
        if response.status_code!=200:
            return response.status_code,response.text
        else:
            return response.status_code,response.json()
    except json.decoder.JSONDecodeError:
        return response.status_code
    except simplejson.errors.JSONDecodeError:
        return response.status_code
    except Exception as e:
        log.war('ERROR')
        log.error(e)


