#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/7/6 14:16
# @Author  : luozhenjie
# @FileName: test_data_filter_check.py
# @Software: PyCharm

import sys

import pytest

sys.path.insert(0, 'C:/Users/X-X/Desktop/HLY-AUTO-TEST')
import time
import allure
import jsonpath
from api.LOG import logger
from random import randint
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


@allure.title('倾斜角度大于6度数据是否过滤')
def test_angle_filter_morethan_6():
    logger.info('已开始进行倾角大于6度的功能测试')
    angle = randint(7, 360)
    HLY.init_data(1, 1, 1000, 1000, 40)
    HLY.check_collect_status()
    logger.info('正在模拟探头数据，倾角数据大于6度，液位高度为3000')
    for i in range(30):
        HLY.com_send1(HLY.create_data(angle, 1, 3000, 3000, 40))
        time.sleep(1)

    HLY.check_push_status()
    logger.info('等待10s后开始校验数据')
    time.sleep(10)
    oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
    angle_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                   '$...dataPoints[?(@.dataPointName == "Ag" )].dataPointReportedValue')
    logger.info('液位高度为：' + str(oh_data))
    logger.info('当前倾角为：' + str(angle_data))
    assert oh_data == [1000], '倾斜角度大于6度的数据应全部过滤掉！！'


@allure.title('倾斜角度小于等于6度数据是否过滤')
def test_angle_filter_lessthan_6():
    logger.info('已开始进行倾角小于等于6度的功能测试')
    angle = randint(0, 6)
    HLY.init_data(1, 1, 1000, 1000, 40)
    HLY.check_collect_status()
    logger.info('正在模拟探头数据，倾角数据小于等于6度，液位高度为3000')
    for i in range(30):
        HLY.com_send1(HLY.create_data(angle, 1, 3000, 3000, 40))
        time.sleep(1)

    HLY.check_push_status()
    logger.info('等待10s后开始校验数据')
    time.sleep(10)
    oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
    angle_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                   '$...dataPoints[?(@.dataPointName == "Ag" )].dataPointReportedValue')
    logger.info('液位高度为：' + str(oh_data))
    logger.info('当前倾角为：' + str(angle_data))
    assert oh_data == [3000], '倾斜角度小于等于6度的数据应正常接收！！'


@allure.title('液位高度等于0数据是否过滤')
def test_oh_filter_equal_0():
    logger.info('已开始进行液位高度等于0的功能测试')
    for mode in mode_list:
        if mode == 1:
            singal = 40
        else:
            singal = 0
        HLY.init_data(1, mode, 1000, 1000, singal)
        HLY.check_collect_status()
        logger.info('正在模拟探头数据，液位高度为0')
        for i in range(30):
            HLY.com_send1(HLY.create_data(1, mode, 0, 0, singal))

        HLY.check_push_status()
        logger.info('等待10s后开始校验数据')
        time.sleep(10)
        oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                    '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
        sm_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                    '$...dataPoints[?(@.dataPointName == "SM" )].dataPointReportedValue')
        logger.info('液位高度为：' + str(oh_data))
        logger.info('当前测试的占号为：' + str(sm_data))
        assert oh_data == [1000], '液位高度等于0时，该条数据不会被接收！！'


@allure.title('液位高度等于FFFF数据是否过滤')
def test_oh_filter_equal_ffff():
    logger.info('已开始进行液位高度等于FFFF的功能测试')
    for mode in mode_list:
        if mode == 1:
            singal = 40
        else:
            singal = 0
        HLY.init_data(1, mode, 1000, 1000, singal)
        HLY.check_collect_status()
        logger.info('正在模拟探头数据，液位高度为FFFF')
        for i in range(30):
            HLY.com_send1(HLY.create_data(1, mode, 'FFFF', 'FFFF', singal))
            time.sleep(1)

        HLY.check_push_status()
        logger.info('等待10s后开始校验数据')
        time.sleep(10)
        oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                    '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
        sm_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                    '$...dataPoints[?(@.dataPointName == "SM" )].dataPointReportedValue')
        logger.info('液位高度为：' + str(oh_data))
        logger.info('当前测试的占号为：' + str(sm_data))
        assert oh_data == [1000], '液位高度等于FFFF时，该条数据不会被接收！！'


@allure.title('电应普信号值大于等于20的数据是否过滤')
def test_singal_filter_morethan_20_dyp():
    logger.info('已开始进行电应普信号值大于等于20的功能测试')
    singal = randint(20, 30)
    HLY.init_data(1, 2, 1000, 1000, 0)
    HLY.check_collect_status()
    logger.info('正在模拟探头数据，信号值大于等于20,液位高度为3000')
    for i in range(30):
        HLY.com_send1(HLY.create_data(1, 2, 3000, 3000, singal))
        time.sleep(1)

    HLY.check_push_status()
    logger.info('等待10s后开始校验数据')
    time.sleep(10)
    oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
    singal_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                    '$...dataPoints[?(@.dataPointName == "SS" )].dataPointReportedValue')
    logger.info('液位高度为：' + str(oh_data))
    logger.info('当前信号值为：' + str(singal_data))
    assert oh_data == [1000], '电应普信号值大于等于20时，数据不会被接收！！'


@allure.title('电应普信号值小于20的数据是否过滤')
def test_singal_filter_lessthan_20_dyp():
    logger.info('已开始进行电应普信号值小于20的功能测试')
    singal = randint(0, 19)
    HLY.init_data(1, 2, 1000, 1000, 0)
    HLY.check_collect_status()
    logger.info('正在模拟探头数据，信号值小于20,液位高度为3000')
    for i in range(30):
        HLY.com_send1(HLY.create_data(1, 2, 3000, 3000, singal))
        time.sleep(1)

    HLY.check_push_status()
    logger.info('等待10s后开始校验数据')
    time.sleep(10)
    oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
    singal_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                    '$...dataPoints[?(@.dataPointName == "SS" )].dataPointReportedValue')
    logger.info('液位高度为：' + str(oh_data))
    logger.info('当前信号值为：' + str(singal_data))
    assert oh_data == [3000], '电应普信号值小于20时，数据可以正常接收！！'


@allure.title('泛特信号值小于等于30的数据是否过滤')
def test_singal_filter_lessthan_30_ft():
    logger.info('已开始进行泛特信号值小于等于30的功能测试')
    singal = randint(0, 30)
    HLY.init_data(1, 1, 1000, 1000, 40)
    HLY.check_collect_status()
    logger.info('正在模拟探头数据，信号值小于等于30,液位高度为3000')
    for i in range(30):
        HLY.com_send1(HLY.create_data(1, 1, 3000, 3000, singal))
        time.sleep(1)

    HLY.check_push_status()
    logger.info('等待10s后开始校验数据')
    time.sleep(10)
    oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
    singal_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                    '$...dataPoints[?(@.dataPointName == "SS" )].dataPointReportedValue')
    logger.info('液位高度为：' + str(oh_data))
    logger.info('当前信号值为：' + str(singal_data))
    assert oh_data == [1000], '泛特信号值小于等于30时，数据不会被接收！！'


@allure.title('泛特信号值大于30的数据是否过滤')
def test_singal_filter_morethan_30_ft():
    logger.info('已开始进行泛特信号值大于30的功能测试')
    singal = randint(31, 40)
    HLY.init_data(1, 1, 1000, 1000, 40)
    HLY.check_collect_status()
    logger.info('正在模拟探头数据，信号值大于30,液位高度为3000')
    for i in range(30):
        HLY.com_send1(HLY.create_data(1, 1, 3000, 3000, singal))
        time.sleep(1)

    HLY.check_push_status()
    logger.info('等待10s后开始校验数据')
    time.sleep(10)
    oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
    singal_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                    '$...dataPoints[?(@.dataPointName == "SS" )].dataPointReportedValue')
    logger.info('液位高度为：' + str(oh_data))
    logger.info('当前信号值为：' + str(singal_data))
    assert oh_data == [3000], '泛特信号值大于30时，数据可以正常接收！！'


@allure.title('电应普小于等于盲区值的数据是否过滤')
def test_lessthan_fade_filter_dyp():
    logger.info('已开始进行电应普小于等于盲区值过滤的功能测试')
    HLY.fade_init(2)
    logger.info('现将液位值初始化至2')
    HLY.init_data(1, 2, 2, 2, 0)

    fz = randint(2, 1999)
    cloud.fz = str(fz)
    logger.info('下发盲区值%s' % fz)
    fz_oh = randint(2, fz)
    cloud.send_device_datapoint()

    while True:
        time.sleep(100)
        fz_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                    '$...dataPoints[?(@.dataPointName == "FZ" )].dataPointReportedValue')
        if fz_data == [fz]:
            logger.info('当前盲区值已修改至%s' % fz)
            HLY.check_collect_status()
            logger.info('正在模拟探头数据，液位高度为%s' % fz_oh)
            for i in range(30):
                HLY.com_send1(HLY.create_data(1, 2, fz_oh, fz_oh, 0))
                time.sleep(1)

            HLY.check_push_status()
            logger.info('等待10s后开始校验数据')
            time.sleep(10)
            oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                        '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
            logger.info('液位高度为：' + str(oh_data))
            assert oh_data == [2], '探头液位值小于等于盲区值时，数据不能被接收！！'
            break
        else:
            continue


@allure.title('电应普大于盲区值的数据是否过滤')
def test_morethan_fade_filter_dyp():
    logger.info('已开始进行电应普大于盲区值过滤的功能测试')
    HLY.fade_init(2)
    logger.info('现将液位值初始化至2')
    HLY.init_data(1, 2, 2, 2, 0)

    fz = randint(2, 1999)
    cloud.fz = str(fz)
    logger.info('下发盲区值%s' % fz)
    fz_oh = randint((fz + 1), 12000)
    cloud.send_device_datapoint()

    while True:
        time.sleep(100)
        fz_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                    '$...dataPoints[?(@.dataPointName == "FZ" )].dataPointReportedValue')
        if fz_data == [fz]:
            logger.info('当前盲区值已修改至%s' % fz)
            HLY.check_collect_status()
            logger.info('正在模拟探头数据，液位高度为%s' % fz_oh)
            for i in range(30):
                HLY.com_send1(HLY.create_data(1, 2, fz_oh, fz_oh, 0))
                time.sleep(1)

            HLY.check_push_status()
            logger.info('等待10s后开始校验数据')
            time.sleep(10)
            oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                        '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
            logger.info('液位高度为：' + str(oh_data))
            assert oh_data == [fz_oh], '探头液位值大于盲区值时，数据可以正常接收！！'
            break
        else:
            continue

# @allure.title('泛特小于等于盲区值的数据是否过滤')
# def test_lessthan_fade_filter_ft():
#     logger.info('已开始进行泛特小于等于盲区值过滤的功能测试')
#     HLY.fade_init(1)
#     logger.info('现将液位值初始化至101')
#     HLY.init_data(1, 1, 101, 101, 40)
#
#     fz = randint(1, 98)
#     cloud.fz = str(fz)
#     logger.info('下发盲区值%s' % fz)
#     fz_oh = randint(1, (fz*100))
#     cloud.send_device_datapoint()
#     time.sleep(70)
#
#     while True:
#         fz_data = jsonpath.jsonpath(cloud.get_device_detail(),
#                                         '$...dataPoints[?(@.dataPointName == "FZ" )].dataPointReportedValue')
#         if fz_data == [fz]:
#             logger.info('当前盲区值已修改至%s' % fz)
#             while True:
#                 start_collect = re.search('sent done', HLY.com_read())
#                 if start_collect:
#                     logger.info('正在模拟探头数据，液位高度为%s' % fz_oh)
#                     for i in range(30):
#                         HLY.com_send1(HLY.create_data(1, 1, fz_oh, fz_oh, 40))
#                         time.sleep(1)
#                     break
#                 else:
#                     continue
#
#             while True:
#                 report_data = re.search('sendStr', HLY.com_read())
#                 if report_data:
#                     logger.info('设备已进行主动上报，等待15s再进行OLC与AT检查')
#                     time.sleep(15)
#                     oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
#                                                 '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
#                     logger.info('液位高度为：' + str(oh_data))
#                     assert oh_data == [2], '探头液位值小于等于盲区值时，数据不能被接收！！'
#                     break
#                 else:
#                     continue
#             break
#         else:
#             continue
#
#
# @allure.title('泛特大于盲区值的数据是否过滤')
# def test_morethan_fade_filter_ft():
#     logger.info('已开始进行泛特大于盲区值过滤的功能测试')
#     HLY.fade_init(1)
#     logger.info('现将液位值初始化至101')
#     HLY.init_data(1, 1, 101, 101, 40)
#
#     fz = randint(1, 98)
#     cloud.fz = randint(1, 98)
#     logger.info('下发盲区值%s' % fz)
#     fz_oh = randint((fz*100) + 1, 12000)
#     cloud.send_device_datapoint()
#     time.sleep(70)
#
#     while True:
#         fz_data = jsonpath.jsonpath(cloud.get_device_detail(),
#                                         '$...dataPoints[?(@.dataPointName == "FZ" )].dataPointReportedValue')
#         if fz_data == [fz]:
#             logger.info('当前盲区值已修改至%s' % fz)
#             while True:
#                 start_collect = re.search('sent done', HLY.com_read())
#                 if start_collect:
#                     logger.info('正在模拟探头数据，液位高度为%s' % fz_oh)
#                     for i in range(30):
#                         HLY.com_send1(HLY.create_data(1, 1, fz_oh, fz_oh, 40))
#                         time.sleep(1)
#                     break
#                 else:
#                     continue
#
#             while True:
#                 report_data = re.search('sendStr', HLY.com_read())
#                 if report_data:
#                     logger.info('设备已进行主动上报，等待15s再进行OLC与AT检查')
#                     time.sleep(15)
#                     oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
#                                                 '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
#                     logger.info('液位高度为：' + str(oh_data))
#                     assert oh_data == [fz_oh], '探头液位值大于盲区值时，数据可以正常接收！！'
#                     break
#                 else:
#                     continue
#             break
#         else:
#             continue
