#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/10/21 9:39
# @Author  : luozhenjie
# @FileName: picture_high.py
# @Software: PyCharm


""" 读取文件 """
from aip import AipOcr

""" 你的 APPID AK SK """
APP_ID = '你的 App ID'
API_KEY = '你的 Api Key'
SECRET_KEY = '你的 Secret Key'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)



def get_file_content(filePath):
    with open(filePath, "rb") as fp:
        return fp.read()


image = get_file_content('文件路径')
url = "https://www.x.com/sample.jpg"
pdf_file = get_file_content('文件路径')

# 调用通用文字识别（高精度版）
res_image = client.basicAccurate(image)
res_url = client.basicAccurateUrl(url)
res_pdf = client.basicAccuratePdf(pdf_file)
print(res_image)
print(res_url)
print(res_pdf)

# 如果有可选参数
options = {}
options["detect_direction"] = "true"
options["probability"] = "true"
res_image = client.basicAccurate(image, options)
res_url = client.basicAccurateUrl(url, options)
res_pdf = client.basicAccuratePdf(pdf_file, options)
print(res_image)
print(res_url)
print(res_pdf)