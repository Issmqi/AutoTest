import pytest
import os

pytest.main(['-s', '--alluredir', '../report/xml'])
os.system('allure generate --clean ../report/xml/ -o ../report/html/')