#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/7/6 11:37
# @Author  : luozhenjie
# @FileName: test_diff_device_mode_check.py
# @Software: PyCharm

import sys
sys.path.insert(0, 'C:/Users/X-X/Desktop/HLY-AUTO-TEST')
import time
import allure
import jsonpath
from api.LOG import logger
from api.HLY_API import HLY_API
from api.IOT_CLOUD_API import IOT_CLOUD_API


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


@allure.title('探头兼容性测试')
def test_diff_device_mode_check():
    logger.info('已开始进行不同探头占号识别的测试')
    for mode in mode_list:
        if mode == 1:
            singal = 40
        else:
            singal = 0
        if HLY.check_collect_status():
            logger.info('正在模拟探头数据，探头占号设置为%s' % mode)
            for i in range(30):
                HLY.com_send1(HLY.create_data(1, mode, 5000, 5000, singal))
                time.sleep(1)

        if HLY.check_push_status():
            logger.info('等待10s后开始校验数据')
            time.sleep(10)
            sm_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                        '$...dataPoints[?(@.dataPointName == "SM" )].dataPointReportedValue')
            logger.info('当前设备占号设置为：'+str(sm_data))
            assert sm_data == [mode], '设备不能识别不同探头的占号！！'
