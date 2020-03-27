# -*- coding: utf-8 -*-
# !/bin/bash

def edit_param(data):
    if isinstance(data,dict):
        for key in data:
            this_key=key
            if isinstance(data[key],dict):
                edit_param(data[key])
            elif isinstance(type(data[this_key]),str):
                if data[this_key]=='null':
                    data[this_key] = 'None'
    else:
        raise Exception('带转换数据类型不为dict')




