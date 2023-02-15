#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/7/19 10:43
# @Author  : luozhenjie
# @FileName: test_shuini_data.py
# @Software: PyCharm
import re
import sys

import pytest

sys.path.insert(0, '/')
import time
import allure
import jsonpath
from api.LOG import logger
from binascii import unhexlify
from crcmod import mkCrcFun, crcmod
from random import randint
from api.HLY_API import HLY_API
from api.IOT_CLOUD_API import IOT_CLOUD_API

HLY = HLY_API()
cloud = IOT_CLOUD_API()

HLY.com = 'com5'
HLY.port = 115200
HLY.com1 = 'com13'
HLY.port1 = 9600
cloud.username = 'lijun2022'
cloud.password = 'lijun123456'
cloud.device_id = 'BjmoaDlFVlrbYoZX4HkA'
test_cycle = 99999


def test_shuini_data():
    for count in range(test_cycle):
        logger.info('第%s次更改水泥管重量' % (count+1))
        shuini = re.search('01 03 00 00 00 02 C4 0B ', HLY.com_read1())
        data_10 = randint(1,1199999)
        logger.info('下发的重量为%s' % data_10)
        str1 = "{:06X}".format(data_10, 16)
        send_data = '01 03 04 ' + str(str1[2:4]) + ' ' + str(str1[4:6]) + ' ' + '00' + ' ' + str(str1[0:2])
        crc_data = send_data.replace(" ", "")
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
        crc = hex(crc16(unhexlify(crc_data))).upper()
        str_list = list(crc)
        if len(str_list) == 5:
            str_list.insert(2, '0')  # 位数不足补0，因为一般最少是5个
        crc_data1 = "".join(str_list)
        str_data = send_data + ' ' + str(crc_data1[4:6]) + ' ' + str(crc_data1[2:4])
        hex_data = bytes.fromhex(str_data)
        logger.info('回复的消息为：%s' % str_data)
        HLY.com_send1(hex_data)
        logger.info('等待10s检查上报重量是否正确')
        time.sleep(10)
        weight_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                    '$...dataPoints[?(@.dataPointName == "weight")].dataPointReportedValue')
        assert weight_data == [str(data_10)]
