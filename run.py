import pytest
import os
import allure

# pytest.main(['case/test_purchase_order.py','-s','--alluredir', 'report/xml'])
pytest.main([ '-s','--alluredir', 'report/xml'])
os.system('rm -rf report/xml/*')
os.system('allure generate --clean report/xml -o report/html/')
