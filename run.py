import pytest
import os

pytest.main(['--workers=2','-s', '--alluredir', '../report/xml'])
os.system('allure generate --clean ../report/xml/ -o ../report/html/')