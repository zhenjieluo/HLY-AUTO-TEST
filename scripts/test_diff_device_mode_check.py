#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/7/6 11:37
# @Author  : luozhenjie
# @FileName: test_diff_device_mode_check.py
# @Software: PyCharm

import sys
import re
import time
import jsonpath
from api.HLY_API import HLY_API
from api.IOT_CLOUD_API import IOT_CLOUD_API

sys.path.insert(0, 'C:/Users/X-X/Desktop/HLY-AUTO-TEST')

HLY = HLY_API()
cloud = IOT_CLOUD_API()

HLY.com = 'com5'
HLY.port = 115200
HLY.com1 = 'com13'
HLY.port1 = 9600
cloud.username = 'luozhenjie'
cloud.password = 'aa123456'
cloud.device_id = 'BllRQflFa1jvbcZE4DYA'
mode_list = [1, 2]


def test_diff_device_mode_check():
    print('已开始进行不同探头占号识别的测试')
    for mode in mode_list:
        if mode == 1:
            singal = 40
        else:
            singal = 0
        while True:
            start_collect = re.search('sent done', HLY.com_read())
            if start_collect:
                print('正在模拟探头数据，探头占号设置为%s' % mode)
                for i in range(30):
                    HLY.com_send1(HLY.create_data(1, mode, 5000, 5000, singal))
                    time.sleep(1)
                break
            else:
                continue

        while True:
            report_data = re.search('sendStr', HLY.com_read())
            if report_data:
                print('设备已进行主动上报，等待15s再进行OLC与AT检查')
                time.sleep(15)
                sm_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                            '$...dataPoints[?(@.dataPointName == "SM" )].dataPointReportedValue')
                print('当前设备占号设置为：'+str(sm_data))
                assert sm_data == [mode], '设备不能识别不同探头的占号！！'
                break
            else:
                continue
