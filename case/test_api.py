# -*- coding: utf-8 -*-

import os
import allure
import pytest
import apiSendCheck
from readExcel import ReadExcel

case_dict=ReadExcel().get_full_dict()
# print(case_dict)

@allure.feature('渠道云接口自动化测试')
class Test_Case:

    @pytest.mark.parametrize('case_data',case_dict, ids=[])
    @allure.story("接口测试")
    # @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_api(self,case_data):
        '''
        :param case_data: 单条测试用例数据
        :return:
        '''
        assert apiSendCheck.api_send_check(case_data)


if __name__ == '__main__':
    # pytest.main()
    # pytest.main("test_api.py")
    pytest.main(['--alluredir', '../report/xml'])
    os.system('allure generate --clean ../report/xml/ -o ../report/html/')

