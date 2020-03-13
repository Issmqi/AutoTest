import json
import os
import requests
import login
import simplejson
import logging

def post(header,url,data,files=None):
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
        param=eval(data)

    if h == {"Content-Type": "application/json", "charset": "UTF-8"}:
        body = json.dumps(param)
    else:
        body=param

    response=requests.post(url=url,headers=h,data=body)

    try:
        if response.status_code!=200:
            return response.status_code,response.text
        else:
            return response.status_code,response.json()
            print(response.status_code,response.json())

    except json.decoder.JSONDecodeError:
        return response.status_code
    except simplejson.errors.JSONDecodeError:
        return response.status_code
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)

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
        logging.exception('ERROR')
        logging.error(e)


