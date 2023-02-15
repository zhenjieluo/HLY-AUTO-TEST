#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/7/18 17:01
# @Author  : luozhenjie
# @FileName: test_shuini_ota.py
# @Software: PyCharm
import sys
import time
import jsonpath
#
from api.IOT_CLOUD_API import IOT_CLOUD_API
from loguru import logger
sys.path.insert(0, '/')

cloud = IOT_CLOUD_API()

cloud.username = 'luozhenjie'
cloud.password = 'aa123456'
cloud.device_id = 'Bm35VEJuEmaveUZx4GYA'
test_cycle = 1000


def test_shuini_ota():
    for count in range(test_cycle):
        logger.info('第%s次开始下发升级命令' % (count+1))
        fv_data = jsonpath.jsonpath(cloud.get_device_detail(), '$...dataPoints[?(@.dataPointName == "FV")].dataPointReportedValue')
        if fv_data == ['HLY_B_V2.0.26A']:
            cloud.fv = 'HLY_B_V2.0.26B'
            cloud.send_device_datapoint()
            logger.info('等待7分钟检查升级是否成功')
            time.sleep(420)
            fv_data1 = jsonpath.jsonpath(cloud.get_device_detail(), '$...dataPoints[?(@.dataPointName == "FV")].dataPointReportedValue')
            assert fv_data1 == ['HLY_B_V2.0.26B'], '升级失败！！！'
        elif fv_data == ['HLY_B_V2.0.26B']:
            cloud.fv = 'HLY_B_V2.0.26A'
            cloud.send_device_datapoint()
            logger.info('等待7分钟检查升级是否成功')
            time.sleep(420)
            fv_data1 = jsonpath.jsonpath(cloud.get_device_detail(), '$...dataPoints[?(@.dataPointName == "FV" '
                                                               ')].dataPointReportedValue')
            assert fv_data1 == ['HLY_B_V2.0.26A'], '升级失败！！！'