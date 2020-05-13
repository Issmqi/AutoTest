# -*- coding: utf-8 -*-
# !/bin/bash

'''

__author__:'shimengqi'
__description__:'读取测试用例信息'
__mtime__:2018/2/1
'''

import xlrd
import setupMain
from util.readConfig import ReadConfig

ReadConfig = ReadConfig()
import time


class ReadExcel:
    def __init__(self,data):
        '''打开工作表'''
        # 从配置文件获取测试用例地址
        # data = ReadConfig.get_config("DATABASE", "data_address")
        # data = setupMain.PATH + '/data/testdata.xlsx'
        # data_address=os.path.abspath('../data/buyerdata1.xlsx')
        # 从excel提取测试用例信息
        workbook = xlrd.open_workbook(data)
        self.table = workbook.sheets()[0]

    def get_rows(self):
        '''获取工作表行数'''
        rows = self.table.nrows
        return rows

    def get_cell(self, row, col):
        '''获取单元格数据'''
        cell_data = self.table.cell(row, col).value
        return cell_data

    def get_row_value(self, row):
        '''获取整行数据'''
        return self.table.row_values(row)

    def get_col(self, col):
        '''获取整列数据'''
        col_data = self.table.col_values(col)
        return col_data

    def get_row_dict(self, row):
        '''获取一行数据字典'''
        header = self.get_row_value(1)
        values = self.get_row_value(row)
        return dict(zip(header, values))

    def get_full_dict(self):
        '''获取整个Excel的字典列表'''
        if self.get_rows() > 1:
            header = self.get_row_value(1)
            listApiData = []
            for row in range(2, self.get_rows()):
                values = self.get_row_value(row)
                api_dict = dict(zip(header, values))
                listApiData.append(api_dict)
            return listApiData


        else:
            print("测试数据为空！")
            return None


def main():
    # data = setupMain.PATH + '/data/allocation/allocation_data.xlsx'
    # data = setupMain.PATH + '/data/purchase/purchase_order_data.xlsx'
    data = setupMain.PATH + '/data/b2border/sales_order_data.xlsx'
    excel_data = ReadExcel(data)
    print(excel_data.get_rows())
    # print(excel_data.get_full_dict())
    values = excel_data.get_row_dict(3)
    print(values)
    print(excel_data.get_full_dict())
    # CaseID = int(values['CaseId'])
    # Designer = values['Designer']
    # CaseName = values['CaseName']
    # APIName = values['APIName']
    # Path = values['Path']
    # Method = values['Method']


if __name__ == '__main__':
    main()
