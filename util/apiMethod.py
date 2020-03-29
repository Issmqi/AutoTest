# -*- coding: utf-8 -*-
# !/bin/bash

import json
import requests
import simplejson
from util.log import Log

log = Log()


def post(url, param_type, param, cookie, header):
    '''
    发送post请求
    :param url: 请求路径
    :param param_type: 参数类型 str
    :param param: 参数 str
    :param cookie:
    :param header: str
    :return: (code,re.json())
    '''
    header = eval(header)
    if not param:
        param_dict = None
    else:
        param_dict = json.loads(param)

    if param_type == 'json':
        data = json.dumps(param_dict)
        response = requests.post(url=url, headers=header, data=data, cookies=cookie)
    elif param_type == 'form_data':
        response = requests.post(url=url, headers=header, data=param_dict, cookies=cookie)
    elif param_type == 'parameter':
        response = requests.post(url=url, headers=header, params=param_dict, cookies=cookie)
    else:
        response = None
        log.error('参数类型不存在')

    times = response.elapsed.total_seconds()
    log.info('响应时间为%ss' % times)
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


def put(url, param_type, param, cookie, header):
    '''
    发送put请求
    :param url: 请求路径
    :param param_type: 参数类型 str
    :param param: 参数 str
    :param cookie:
    :param header: str
    :return: (code,re.json())
    '''
    header = eval(header)
    if not param:
        param_dict = None
    else:
        param_dict = json.loads(param)

    if param_type == 'json':
        data = json.dumps(param_dict)
        response = requests.put(url=url, headers=header, data=data, cookies=cookie)
    elif param_type == 'form_data':
        response = requests.put(url=url, headers=header, data=param_dict, cookies=cookie)
    elif param_type == 'parameter':
        response = requests.put(url=url, headers=header, params=param_dict, cookies=cookie)
    else:
        response = None
        log.error('参数类型不存在')

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


def get(header, url, param):
    '''
    发送get请求
    :param header: 请求头
    :param url: 接口路径
    :param data: 请求参数
    :return:
    '''
    if not header:
        header=None
    else:
        header=json.loads(header)
    if not param:
        param = None
    else:
        param = json.loads(param)
    response = requests.get(url=url, headers=header, params=param)
    if response.status_code == 301:
        response = requests.get(url=response.headers['location'])
    try:
        if response.status_code != 200:
            print(response.url)
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
