#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/7/5 9:30
# @Author  : luozhenjie
# @FileName: test_oil_change_check.py
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


def test_add_oil_check_700():
    print('已开始进行加油量小于800功能测试')
    while True:
        start_collect = re.search('sent done', HLY.com_read())
        if start_collect:
            print('正在模拟探头数据，液位高度设置为1200')
            for i in range(30):
                HLY.com_send1('*XD,0001,02,1200,1200,0005,0253,1344#')
                time.sleep(1)
            break
        else:
            continue

    while True:
        report_data = re.search('sendStr', HLY.com_read())
        if report_data:
            print('设备已进行主动上报')
            time.sleep(60)
            break
        else:
            continue

    while True:
        oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                    '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
        print(oh_data)
        if oh_data == [1200]:
            break
        else:
            continue
    print('油位高度已下降至1200')

    while True:
        start_collect1 = re.search('sent done', HLY.com_read())
        if start_collect1:
            print('正在模拟探头数据，液位高度设置为1900')
            for i in range(30):
                HLY.com_send1('*XD,0001,02,1900,1900,0005,0253,1358#')
                time.sleep(1)
            break
        else:
            continue

    while True:
        report_data1 = re.search('sendStr', HLY.com_read())
        if report_data1:
            print('设备已进行主动上报，等待70s再进行OLC检查')
            time.sleep(70)
            olc_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                         '$...dataPoints[?(@.dataPointName == "OLC" )].dataPointReportedValue')
            oh_data1 = jsonpath.jsonpath(cloud.get_device_detail(),
                                        '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
            print('当前设备液位值为：'+str(oh_data1))
            print('液位上涨高度为：'+str(olc_data))
            assert olc_data == [0], '液位上涨，没有新增油位变化量！！'
            assert oh_data1 == [1200], '液位上涨不超过800，液位值不更新！！'
            break
        else:
            continue


def test_add_oil_check_800():
    print('已开始进行加油量等于800功能测试')
    while True:
        start_collect = re.search('sent done', HLY.com_read())
        if start_collect:
            print('正在模拟探头数据，液位高度设置为1200')
            for i in range(30):
                HLY.com_send1('*XD,0001,02,1200,1200,0005,0253,1344#')
                time.sleep(1)
            break
        else:
            continue

    while True:
        report_data = re.search('sendStr', HLY.com_read())
        if report_data:
            print('设备已进行主动上报')
            time.sleep(60)
            break
        else:
            continue

    while True:
        oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                    '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
        print(oh_data)
        if oh_data == [1200]:
            break
        else:
            continue
    print('油位高度已下降至1200')

    while True:
        start_collect1 = re.search('sent done', HLY.com_read())
        if start_collect1:
            print('正在模拟探头数据，液位高度设置为2000')
            for i in range(30):
                HLY.com_send1('*XD,0001,02,2000,2000,0005,0253,1342#')
                time.sleep(1)
            break
        else:
            continue

    while True:
        report_data1 = re.search('sendStr', HLY.com_read())
        if report_data1:
            print('设备已进行主动上报，等待70s再进行OLC检查')
            time.sleep(70)
            olc_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                         '$...dataPoints[?(@.dataPointName == "OLC" )].dataPointReportedValue')
            oh_data1 = jsonpath.jsonpath(cloud.get_device_detail(),
                                         '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
            print('当前设备液位值为：' + str(oh_data1))
            print('液位上涨高度为：'+str(olc_data))
            assert olc_data == [0], '液位上涨，没有新增油位变化量！！'
            assert oh_data1 == [1200], '液位上涨不超过800，液位值不更新！！'
            break
        else:
            continue



def test_add_oil_check_1800():
    print('已开始进行加油量大于800功能测试')
    while True:
        start_collect = re.search('sent done', HLY.com_read())
        if start_collect:
            print('正在模拟探头数据，液位高度设置为1200')
            for i in range(30):
                HLY.com_send1('*XD,0001,02,1200,1200,0005,0253,1344#')
                time.sleep(1)
            break
        else:
            continue

    while True:
        report_data = re.search('sendStr', HLY.com_read())
        if report_data:
            print('设备已进行主动上报')
            time.sleep(60)
            break
        else:
            continue

    while True:
        oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                    '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
        print(oh_data)
        if oh_data == [1200]:
            break
        else:
            continue
    print('油位高度已下降至1200')

    while True:
        start_collect1 = re.search('sent done', HLY.com_read())
        if start_collect1:
            print('正在模拟探头数据，液位高度设置为3000')
            for i in range(30):
                HLY.com_send1('*XD,0001,02,3000,3000,0005,0253,1344#')
                time.sleep(1)
            break
        else:
            continue

    while True:
        report_data1 = re.search('sendStr', HLY.com_read())
        if report_data1:
            print('设备已进行主动上报，等待70s再进行OLC检查')
            time.sleep(70)
            olc_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                         '$...dataPoints[?(@.dataPointName == "OLC" )].dataPointReportedValue')
            print('液位上涨高度为：'+str(olc_data))
            assert olc_data == [1800], '液位上涨，没有新增油位变化量！！'
            break
        else:
            continue


def test_steal_oil_check_400():
    print('已开始进行偷油量等于400功能测试')
    while True:
        start_collect = re.search('sent done', HLY.com_read())
        if start_collect:
            print('正在模拟探头数据，液位高度设置为3000')
            for i in range(30):
                HLY.com_send1('*XD,0001,02,3000,3000,0005,0253,1344#')
                time.sleep(1)
            break
        else:
            continue

    while True:
        report_data = re.search('sendStr', HLY.com_read())
        if report_data:
            print('设备已进行主动上报')
            time.sleep(60)
            break
        else:
            continue

    while True:
        oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                    '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
        print(oh_data)
        if oh_data == [3000]:
            break
        else:
            continue
    print('油位高度已调整为3000')

    while True:
        start_collect = re.search('sent done', HLY.com_read())
        if start_collect:
            print('正在模拟探头数据，液位高度设置为2600')
            for i in range(30):
                HLY.com_send1('*XD,0001,02,2600,2600,0005,0253,1354#')
                time.sleep(1)
            break
        else:
            continue

    while True:
        report_data = re.search('sendStr', HLY.com_read())
        if report_data:
            print('设备已进行主动上报，等待70s再进行OLC与AT检查')
            time.sleep(70)
            olc_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                         '$...dataPoints[?(@.dataPointName == "OLC" )].dataPointReportedValue')
            at_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                         '$...dataPoints[?(@.dataPointName == "AT" )].dataPointReportedValue')
            print('液位下降高度为：'+str(olc_data))
            print('AT异常告警为：'+str(at_data))
            assert olc_data == [0], '液位下降等于400，不应新增油位变化量！！'
            assert at_data != [2], '液位下降等于400，不应发出异常油位告警'
            break
        else:
            continue


def test_steal_oil_check_300():
    print('已开始进行偷油量小于400功能测试')
    while True:
        start_collect = re.search('sent done', HLY.com_read())
        if start_collect:
            print('正在模拟探头数据，液位高度设置为2600')
            for i in range(30):
                HLY.com_send1('*XD,0001,02,2600,2600,0005,0253,1354#')
                time.sleep(1)
            break
        else:
            continue

    while True:
        report_data = re.search('sendStr', HLY.com_read())
        if report_data:
            print('设备已进行主动上报')
            time.sleep(60)
            break
        else:
            continue

    while True:
        oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                    '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
        print(oh_data)
        if oh_data == [2600]:
            break
        else:
            continue
    print('油位高度已调整为2600')

    while True:
        start_collect = re.search('sent done', HLY.com_read())
        if start_collect:
            print('正在模拟探头数据，液位高度设置为2300')
            for i in range(30):
                HLY.com_send1('*XD,0001,02,2300,2300,0005,0253,1348#')
                time.sleep(1)
            break
        else:
            continue

    while True:
        report_data = re.search('sendStr', HLY.com_read())
        if report_data:
            print('设备已进行主动上报，等待70s再进行OLC与AT检查')
            time.sleep(70)
            olc_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                         '$...dataPoints[?(@.dataPointName == "OLC" )].dataPointReportedValue')
            at_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                         '$...dataPoints[?(@.dataPointName == "AT" )].dataPointReportedValue')
            print('液位下降高度为：'+str(olc_data))
            print('AT异常告警为：'+str(at_data))
            assert olc_data == [0], '液位下降小于400，不应新增油位变化量！！'
            assert at_data != [2], '液位下降小于400，不应发出异常油位告警'
            break
        else:
            continue


def test_steal_oil_check_600():
    print('已开始进行偷油量大于400功能测试')
    while True:
        start_collect = re.search('sent done', HLY.com_read())
        if start_collect:
            print('正在模拟探头数据，液位高度设置为2300')
            for i in range(30):
                HLY.com_send1('*XD,0001,02,2300,2300,0005,0253,1348#')
                time.sleep(1)
            break
        else:
            continue

    while True:
        report_data = re.search('sendStr', HLY.com_read())
        if report_data:
            print('设备已进行主动上报')
            time.sleep(60)
            break
        else:
            continue

    while True:
        oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                    '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
        print(oh_data)
        if oh_data == [2300]:
            break
        else:
            continue
    print('油位高度已调整为2300')

    while True:
        start_collect = re.search('sent done', HLY.com_read())
        if start_collect:
            print('正在模拟探头数据，液位高度设置为1700')
            for i in range(30):
                HLY.com_send1('*XD,0001,02,1700,1700,0005,0253,1354#')
                time.sleep(1)
            break
        else:
            continue

    while True:
        report_data = re.search('sendStr', HLY.com_read())
        if report_data:
            print('设备已进行主动上报，等待70s再进行OLC与AT检查')
            time.sleep(70)
            olc_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                         '$...dataPoints[?(@.dataPointName == "OLC" )].dataPointReportedValue')
            at_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                         '$...dataPoints[?(@.dataPointName == "AT" )].dataPointReportedValue')
            print('液位下降高度为：'+str(olc_data))
            print('AT异常告警为：'+str(at_data))
            assert olc_data == [-600], '液位异常下降，没有新增油位变化量！！'
            assert at_data == [2], '液位异常下降，没有发出异常油位告警'
            break
        else:
            continue