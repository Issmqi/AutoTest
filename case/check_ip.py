#!usr/bin/python
# -*- coding: utf-8 -*-

import pytest
import allure
import os

def check_ip(str):

    l=str.split(".")
    print(l)
    if len(l)==4:
        flag = True
        for i in l:
            print(i)
            if i.isdigit():#判断字符串是否全部数字组成
                # if i.startswith('0'):#判断字符串是否由0开始
                #     return False
                n=int(i)
                print(n)
                if n>=0 and n <256:
                    pass
                else:
                    print('不在0-255之间')
                    flag=False

            else:
                print('不全部由数字组成')
                flag=True

        return flag

    else:
        print('字节长度不为4节')
        return False


# check_ip('111.222.255.223')
data=['001','123.1ab.234.sddf','123.123.111.222.111','111.123.256.111','000.222.255.223']
#
# @allure.feature('测试')
# @pytest.mark.parametrize('param',data)
# def test_check_ip(param):
#     assert check_ip(param)
#
#
# if __name__ == '__main__':
#     pytest.main()

# if __name__ == '__main__':
#     pytest.main(['--alluredir', '../report/xml'])
#     os.system('allure generate --clean ../report/xml/ -o ../report/html/')





check_ip("001.123.12.45")

# data=[
#     ['255.255.255.0',True],
#     ['255.1.1.256',False],
#     ['0.0.0.0',True],
#     ['1.1.1.1',False]
# ]
#
# @pytest.mark.parametrize('test_data',data)
# def test_ipv4(test_data):
#     assert check_ipv4(test_data[0]) ==test_data[1]
#
# if __name__ == '__main__':
#     pytest.main(['test.py'])
