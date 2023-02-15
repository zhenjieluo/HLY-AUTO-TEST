#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/10/21 9:37
# @Author  : luozhenjie
# @FileName: picture_low.py
# @Software: PyCharm




""" 读取文件 """
from http import client


def get_file_content(filePath):
    with open(filePath, "rb") as fp:
        return fp.read()


image = get_file_content('文件路径')
url = "https://www.x.com/sample.jpg"
pdf_file = get_file_content('文件路径')

# 调用通用文字识别（标准版）
res_image = client.basicGeneral(image)
res_url = client.basicGeneralUrl(url)
res_pdf = client.basicGeneralPdf(pdf_file)
print(res_image)
print(res_url)
print(res_pdf)

# 如果有可选参数
options = {}
options["language_type"] = "CHN_ENG"
options["detect_direction"] = "true"
options["detect_language"] = "true"
options["probability"] = "true"
res_image = client.basicGeneral(image, options)
res_url = client.basicGeneralUrl(url, options)
res_pdf = client.basicGeneralPdf(pdf_file, options)
print(res_image)
print(res_url)
print(res_pdf)
