# -*- coding: utf-8 -*-
# !/bin/bash
import sys, os
import allure
import pytest
import setupMain
path = os.path.dirname(sys.path[0])
sys.path.append(path)
from util.readExcel import ReadExcel
from util import apiSendCheck

# from utils import readExcel

data = setupMain.PATH + '/data/testdata.xlsx'
case_dict = ReadExcel(data).get_full_dict()


# print(case_dict)

@allure.feature('渠道云接口自动化测试')
class TestCase:

    @pytest.mark.parametrize('case_data', case_dict, ids=[])
    @allure.story("接口测试")
    # @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_api(self, case_data):
        '''
        :param case_data: 测试用例
        :return:
        '''
        assert apiSendCheck.api_send_check(case_data)

# if __name__ == '__main__':
#     # pytest.main()
#     # pytest.main("test_api.py")
#     pytest.main(['-s', '--alluredir', '../report/xml'])
#     os.system('allure generate --clean ../report/xml/ -o ../report/html/')
