import pytest
import os

pytest.main(['./','-s', '-q', '--alluredir', '../report/xml'])
os.system('allure generate --clean ../report/xml/ -o ../report/html/')
