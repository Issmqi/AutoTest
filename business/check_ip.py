# -*- coding: utf-8 -*-
# !/bin/bash
import allure
import pytest
import os




def check_ip(str):

    l=str.split(".")
    print(l)
    if len(l)==4:
        flag = True
        for i in l:
            # print(i)
            if i.isdigit():#判断字符串是否全部数字组成
                # if i.startswith('0'):#判断字符串是否由0开始
                #     return False
                n=int(i)
                # print(n)
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


@allure.feature('这是一个测试')
def test_check_ip():
    assert  check_ip('111.222.257.223')

#
#
if __name__ == '__main__':
    # pytest.main()

    # pytest.main(['-s', '-q', '--alluredir', './report/xml'])
    pytest.main(['--alluredir', './report/xml'])
    os.system('allure generate ./report/xml  -o ./report/html --clean')



# check_ip("001.123.12.45")

