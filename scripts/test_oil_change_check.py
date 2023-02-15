#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/7/5 9:30
# @Author  : luozhenjie
# @FileName: test_oil_change_check.py
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

HLY.com = 'com10'
HLY.port = 115200
HLY.com1 = 'com6'
HLY.port1 = 9600
cloud.username = 'luozhenjie'
cloud.password = 'aa123456'
cloud.device_id = 'Bm35VEJuEmaveUZx4GYA'


@allure.title('校验偷油量等于400是否告警')
def test_steal_oil_check_equal_400():
    logger.info('已开始进行偷油量等于400功能测试')
    HLY.init_data(1, 2, 3000, 3000, 0)
    HLY.check_collect_status()
    logger.info('正在模拟探头数据，液位高度设置为2600')
    for i in range(30):
        HLY.com_send1(HLY.create_data(1, 2, 2600, 2600, 0))
        time.sleep(1)

    HLY.check_push_status()
    logger.info('等待10s后开始校验数据')
    time.sleep(10)
    olc_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                 '$...dataPoints[?(@.dataPointName == "OLC" )].dataPointReportedValue')
    at_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                 '$...dataPoints[?(@.dataPointName == "AT" )].dataPointReportedValue')
    logger.info('液位下降高度为：'+str(olc_data))
    logger.info('AT异常告警为：'+str(at_data))
    assert olc_data == [0], '液位下降等于400，不应新增油位变化量！！'
    assert at_data != [3], '液位下降等于400，不应发出异常油位告警'


@allure.title('校验偷油量小于400是否告警')
def test_steal_oil_check_lessthan_400():
    logger.info('已开始进行偷油量小于400功能测试')
    HLY.init_data(1, 2, 2600, 2600, 0)
    HLY.check_collect_status()
    logger.info('正在模拟探头数据，液位高度设置为2300')
    for i in range(30):
        HLY.com_send1(HLY.create_data(1, 2, 2300, 2300, 0))
        time.sleep(1)

    HLY.check_push_status()
    logger.info('等待10s后开始校验数据')
    time.sleep(10)
    olc_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                 '$...dataPoints[?(@.dataPointName == "OLC" )].dataPointReportedValue')
    at_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                 '$...dataPoints[?(@.dataPointName == "AT" )].dataPointReportedValue')
    logger.info('液位下降高度为：'+str(olc_data))
    logger.info('AT异常告警为：'+str(at_data))
    assert olc_data == [0], '液位下降小于400，不应新增油位变化量！！'
    assert at_data != [3], '液位下降小于400，不应发出异常油位告警'


@allure.title('校验偷油量大于400是否告警')
def test_steal_oil_check_morethan_400():
    logger.info('已开始进行偷油量大于400功能测试')
    HLY.init_data(1, 2, 2300, 2300, 0)
    HLY.check_collect_status()
    logger.info('正在模拟探头数据，液位高度设置为1700')
    for i in range(30):
        HLY.com_send1(HLY.create_data(1, 2, 1700, 1700, 0))
        time.sleep(1)

    HLY.check_push_status()
    logger.info('等待10s后开始校验数据')
    time.sleep(10)
    olc_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                 '$...dataPoints[?(@.dataPointName == "OLC" )].dataPointReportedValue')
    at_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                 '$...dataPoints[?(@.dataPointName == "AT" )].dataPointReportedValue')
    logger.info('液位下降高度为：'+str(olc_data))
    logger.info('AT异常告警为：'+str(at_data))
    assert olc_data == [-600], '液位异常下降，没有新增油位变化量！！'
    assert at_data == [3], '液位异常下降，没有发出异常油位告警'


@allure.title('校验加油量小于800是否上报')
def test_add_oil_check_lessthan_800():
    logger.info('已开始进行加油量小于800功能测试')
    HLY.init_data(1, 2, 1200, 1200, 0)
    HLY.check_collect_status()
    logger.info('正在模拟探头数据，液位高度设置为1900')
    for i in range(30):
        HLY.com_send1(HLY.create_data(1, 2, 1900, 1900, 0))
        time.sleep(1)

    HLY.check_push_status()
    logger.info('等待70s后开始校验数据')
    time.sleep(70)
    olc_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                 '$...dataPoints[?(@.dataPointName == "OLC" )].dataPointReportedValue')
    oh_data1 = jsonpath.jsonpath(cloud.get_device_detail(),
                                '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
    logger.info('当前设备液位值为：'+str(oh_data1))
    logger.info('液位上涨高度为：'+str(olc_data))
    assert olc_data == [0], '液位上涨，没有新增油位变化量！！'
    assert oh_data1 == [1200], '液位上涨不超过800，液位值不更新！！'


@allure.title('校验加油量等于800是否上报')
def test_add_oil_check_equal_800():
    logger.info('已开始进行加油量等于800功能测试')
    HLY.init_data(1, 2, 1200, 1200, 0)
    HLY.check_collect_status()
    logger.info('正在模拟探头数据，液位高度设置为2000')
    for i in range(30):
        HLY.com_send1(HLY.create_data(1, 2, 2000, 2000, 0))
        time.sleep(1)

    HLY.check_push_status()
    logger.info('等待70s后开始校验数据')
    time.sleep(70)
    olc_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                 '$...dataPoints[?(@.dataPointName == "OLC" )].dataPointReportedValue')
    oh_data1 = jsonpath.jsonpath(cloud.get_device_detail(),
                                 '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
    logger.info('当前设备液位值为：' + str(oh_data1))
    logger.info('液位上涨高度为：'+str(olc_data))
    assert olc_data == [0], '液位上涨，没有新增油位变化量！！'
    assert oh_data1 == [1200], '液位上涨不超过800，液位值不更新！！'


@allure.title('校验加油量大于800是否上报')
def test_add_oil_check_morethan_800():
    logger.info('已开始进行加油量大于800功能测试')
    HLY.init_data(1, 2, 1200, 1200, 0)
    HLY.check_collect_status()
    logger.info('正在模拟探头数据，液位高度设置为3000')
    for i in range(30):
        HLY.com_send1(HLY.create_data(1, 2, 3000, 3000, 0))
        time.sleep(1)

    HLY.check_push_status()
    logger.info('等待70s后开始校验数据')
    time.sleep(70)
    olc_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                 '$...dataPoints[?(@.dataPointName == "OLC" )].dataPointReportedValue')
    logger.info('液位上涨高度为：'+str(olc_data))
    assert olc_data == [1800], '液位上涨，没有新增油位变化量！！'
