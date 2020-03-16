import os

PATH = os.path.split(os.path.realpath(__file__))[0]
print(PATH)
case_path=PATH+'/data/testdata.xlsx'
json_result_path=PATH+'/temp/'