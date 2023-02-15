#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 11:16
# @Author  : luozhenjie
# @FileName: 123.py
# @Software: PyCharm
import re
from xlutils.copy import copy

import pandas as pd
import xlrd


def qwe():
    # filename是文件的路径名称
    workbook = xlrd.open_workbook(filename='b.xls')
    # 获取第一个sheet表格
    table = workbook.sheets()[0]
    # 获取sheet中有效行数
    row = table.nrows
    table_list = table.col_values(colx=18, start_rowx=0, end_rowx=None)
    for i in range(row):
        data = table.cell_value(rowx=i,colx=18)
        if re.search('您想解决的问题',str(data)):
            new = table.put_cell(rowx=i, colx=23, ctype=1, value=str(data),xf_index=0)
        else:
            continue
    wb = copy(workbook)
    wb.save('c.xls')
if __name__ == '__main__':
    qwe()