#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/7/6 14:16
# @Author  : luozhenjie
# @FileName: test_data_filter_check.py
# @Software: PyCharm

import sys
import re
import time
from random import randint

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


def test_angle_filter_morethan_6():
    print('已开始进行倾角大于6度的功能测试')
    HLY.init_data(1, 1, 1000, 1000, 40)
    while True:
        start_collect = re.search('sent done', HLY.com_read())
        if start_collect:
            print('正在模拟探头数据，倾角数据大于6度，液位高度为3000')
            for i in range(30):
                HLY.com_send1(HLY.create_data(randint(7, 360), 1, 3000, 3000, 40))
                time.sleep(1)
            break
        else:
            continue

    while True:
        report_data = re.search('sendStr', HLY.com_read())
        if report_data:
            print('设备已进行主动上报，等待15s再进行OLC与AT检查')
            time.sleep(15)
            oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                         '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
            angle_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                         '$...dataPoints[?(@.dataPointName == "Ag" )].dataPointReportedValue')
            print('液位高度为：' + str(oh_data))
            print('当前倾角为：' + str(angle_data))
            assert oh_data == [1000], '倾斜角度大于6度的数据应全部过滤掉！！'
            break
        else:
            continue


def test_angle_filter_lessthan_6():
    print('已开始进行倾角小于等于6度的功能测试')
    HLY.init_data(1, 1, 1000, 1000, 40)
    while True:
        start_collect = re.search('sent done', HLY.com_read())
        if start_collect:
            print('正在模拟探头数据，倾角数据小于等于6度，液位高度为3000')
            for i in range(30):
                HLY.com_send1(HLY.create_data(randint(0, 6), 1, 3000, 3000, 40))
                time.sleep(1)
            break
        else:
            continue

    while True:
        report_data = re.search('sendStr', HLY.com_read())
        if report_data:
            print('设备已进行主动上报，等待15s再进行OLC与AT检查')
            time.sleep(15)
            oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                         '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
            angle_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                           '$...dataPoints[?(@.dataPointName == "Ag" )].dataPointReportedValue')
            print('液位高度为：' + str(oh_data))
            print('当前倾角为：' + str(angle_data))
            assert oh_data == [3000], '倾斜角度小于等于6度的数据应正常接收！！'
            break
        else:
            continue


def test_oh_filter_equal_0():
    print('已开始进行液位高度等于0的功能测试')
    for mode in mode_list:
        if mode == 1:
            singal = 40
        else:
            singal = 0
        HLY.init_data(1, mode, 1000, 1000, singal)
        while True:
            start_collect = re.search('sent done', HLY.com_read())
            if start_collect:
                print('正在模拟探头数据，液位高度为0')
                for i in range(30):
                    HLY.com_send1(HLY.create_data(1, mode, 0, 0, singal))
                    time.sleep(1)
                break
            else:
                continue

        while True:
            report_data = re.search('sendStr', HLY.com_read())
            if report_data:
                print('设备已进行主动上报，等待15s再进行OLC与AT检查')
                time.sleep(15)
                oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                             '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
                sm_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                             '$...dataPoints[?(@.dataPointName == "SM" )].dataPointReportedValue')
                print('液位高度为：'+str(oh_data))
                print('当前测试的占号为：' + str(sm_data))
                assert oh_data == [1000], '液位高度等于0时，该条数据不会被接收！！'
                break
            else:
                continue


def test_oh_filter_equal_ffff():
    print('已开始进行液位高度等于FFFF的功能测试')
    for mode in mode_list:
        if mode == 1:
            singal = 40
        else:
            singal = 0
        HLY.init_data(1, mode, 1000, 1000, singal)
        while True:
            start_collect = re.search('sent done', HLY.com_read())
            if start_collect:
                print('正在模拟探头数据，液位高度为FFFF')
                for i in range(30):
                    HLY.com_send1(HLY.create_data(1, mode, 'FFFF', 'FFFF', singal))
                    time.sleep(1)
                break
            else:
                continue

        while True:
            report_data = re.search('sendStr', HLY.com_read())
            if report_data:
                print('设备已进行主动上报，等待15s再进行OLC与AT检查')
                time.sleep(15)
                oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                             '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
                sm_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                            '$...dataPoints[?(@.dataPointName == "SM" )].dataPointReportedValue')
                print('液位高度为：' + str(oh_data))
                print('当前测试的占号为：' + str(sm_data))
                assert oh_data == [1000], '液位高度等于FFFF时，该条数据不会被接收！！'
                break
            else:
                continue


def test_singal_filter_morethan_20_dyp():
    print('已开始进行电应普信号值大于等于20的功能测试')
    HLY.init_data(1, 2, 1000, 1000, 0)
    while True:
        start_collect = re.search('sent done', HLY.com_read())
        if start_collect:
            print('正在模拟探头数据，信号值大于等于20,液位高度为3000')
            for i in range(30):
                HLY.com_send1(HLY.create_data(1, 2, 3000, 3000, randint(20, 30)))
                time.sleep(1)
            break
        else:
            continue

    while True:
        report_data = re.search('sendStr', HLY.com_read())
        if report_data:
            print('设备已进行主动上报，等待15s再进行OLC与AT检查')
            time.sleep(15)
            oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                        '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
            singal_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                            '$...dataPoints[?(@.dataPointName == "SS" )].dataPointReportedValue')
            print('液位高度为：' + str(oh_data))
            print('当前信号值为：' + str(singal_data))
            assert oh_data == [1000], '电应普信号值大于等于20时，数据不会被接收！！'
            break
        else:
            continue


def test_singal_filter_lessthan_20_dyp():
    print('已开始进行电应普信号值小于20的功能测试')
    HLY.init_data(1, 2, 1000, 1000, 0)
    while True:
        start_collect = re.search('sent done', HLY.com_read())
        if start_collect:
            print('正在模拟探头数据，信号值小于20,液位高度为3000')
            for i in range(30):
                HLY.com_send1(HLY.create_data(1, 2, 3000, 3000, randint(0, 19)))
                time.sleep(1)
            break
        else:
            continue

    while True:
        report_data = re.search('sendStr', HLY.com_read())
        if report_data:
            print('设备已进行主动上报，等待15s再进行OLC与AT检查')
            time.sleep(15)
            oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                        '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
            singal_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                        '$...dataPoints[?(@.dataPointName == "SS" )].dataPointReportedValue')
            print('液位高度为：' + str(oh_data))
            print('当前信号值为：' + str(singal_data))
            assert oh_data == [3000], '电应普信号值小于20时，数据可以正常接收！！'
            break
        else:
            continue


def test_singal_filter_lessthan_30_ft():
    print('已开始进行泛特信号值小于等于30的功能测试')
    HLY.init_data(1, 1, 1000, 1000, 40)
    while True:
        start_collect = re.search('sent done', HLY.com_read())
        if start_collect:
            print('正在模拟探头数据，信号值小于等于30,液位高度为3000')
            for i in range(30):
                HLY.com_send1(HLY.create_data(1, 1, 3000, 3000, randint(0, 30)))
                time.sleep(1)
            break
        else:
            continue

    while True:
        report_data = re.search('sendStr', HLY.com_read())
        if report_data:
            print('设备已进行主动上报，等待15s再进行OLC与AT检查')
            time.sleep(15)
            oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                        '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
            singal_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                        '$...dataPoints[?(@.dataPointName == "SS" )].dataPointReportedValue')
            print('液位高度为：' + str(oh_data))
            print('当前信号值为：' + str(singal_data))
            assert oh_data == [1000], '泛特信号值小于等于30时，数据不会被接收！！'
            break
        else:
            continue


def test_singal_filter_morethan_30_ft():
    print('已开始进行泛特信号值大于30的功能测试')
    HLY.init_data(1, 1, 1000, 1000, 40)
    while True:
        start_collect = re.search('sent done', HLY.com_read())
        if start_collect:
            print('正在模拟探头数据，信号值大于30,液位高度为3000')
            for i in range(30):
                HLY.com_send1(HLY.create_data(1, 1, 3000, 3000, randint(31, 40)))
                time.sleep(1)
            break
        else:
            continue

    while True:
        report_data = re.search('sendStr', HLY.com_read())
        if report_data:
            print('设备已进行主动上报，等待15s再进行OLC与AT检查')
            time.sleep(15)
            oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                        '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
            singal_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                        '$...dataPoints[?(@.dataPointName == "SS" )].dataPointReportedValue')
            print('液位高度为：' + str(oh_data))
            print('当前信号值为：' + str(singal_data))
            assert oh_data == [3000], '泛特信号值大于30时，数据可以正常接收！！'
            break
        else:
            continue


def test_lessthan_fade_filter_dyp():
    print('已开始进行电应普小于等于盲区值过滤的功能测试')
    print('现将液位值初始化至1')
    HLY.init_data(1, 2, 1, 1, 0)

    cloud.fz = randint(2, 1999)
    fz_oh = randint(2, cloud.fz)
    cloud.send_device_datapoint()
    time.sleep(70)

    while True:
        fz_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                        '$...dataPoints[?(@.dataPointName == "FZ" )].dataPointReportedValue')
        if fz_data == [cloud.fz]:
            print('当前盲区值已修改至%s' % cloud.fz)
            while True:
                start_collect = re.search('sent done', HLY.com_read())
                if start_collect:
                    print('正在模拟探头数据，液位高度为%s' % fz_oh)
                    for i in range(30):
                        HLY.com_send1(HLY.create_data(1, 2, fz_oh, fz_oh, 0))
                        time.sleep(1)
                    break
                else:
                    continue

            while True:
                report_data = re.search('sendStr', HLY.com_read())
                if report_data:
                    print('设备已进行主动上报，等待15s再进行OLC与AT检查')
                    time.sleep(15)
                    oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                                '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
                    print('液位高度为：' + str(oh_data))
                    assert oh_data == [1], '探头液位值小于等于盲区值时，数据不能被接收！！'
                    break
                else:
                    continue
        else:
            continue


def test_morethan_fade_filter_dyp():
    print('已开始进行电应普大于盲区值过滤的功能测试')
    print('现将液位值初始化至1')
    HLY.init_data(1, 2, 1, 1, 0)

    cloud.fz = randint(2, 1999)
    fz_oh = randint((cloud.fz + 1), 12000)
    cloud.send_device_datapoint()
    time.sleep(70)

    while True:
        fz_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                        '$...dataPoints[?(@.dataPointName == "FZ" )].dataPointReportedValue')
        if fz_data == [cloud.fz]:
            print('当前盲区值已修改至%s' % cloud.fz)
            while True:
                start_collect = re.search('sent done', HLY.com_read())
                if start_collect:
                    print('正在模拟探头数据，液位高度为%s' % fz_oh)
                    for i in range(30):
                        HLY.com_send1(HLY.create_data(1, 2, fz_oh, fz_oh, 0))
                        time.sleep(1)
                    break
                else:
                    continue

            while True:
                report_data = re.search('sendStr', HLY.com_read())
                if report_data:
                    print('设备已进行主动上报，等待15s再进行OLC与AT检查')
                    time.sleep(15)
                    oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                                '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
                    print('液位高度为：' + str(oh_data))
                    assert oh_data == [fz_oh], '探头液位值大于盲区值时，数据可以正常接收！！'
                    break
                else:
                    continue
        else:
            continue


def test_lessthan_fade_filter_ft():
    print('已开始进行泛特小于等于盲区值过滤的功能测试')
    print('现将液位值初始化至1')
    HLY.init_data(1, 1, 1, 1, 0)

    cloud.fz = randint(1, 98)
    fz_oh = randint(1, (cloud.fz*100))
    cloud.send_device_datapoint()
    time.sleep(70)

    while True:
        fz_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                        '$...dataPoints[?(@.dataPointName == "FZ" )].dataPointReportedValue')
        if fz_data == [cloud.fz]:
            print('当前盲区值已修改至%s' % cloud.fz)
            while True:
                start_collect = re.search('sent done', HLY.com_read())
                if start_collect:
                    print('正在模拟探头数据，液位高度为%s' % fz_oh)
                    for i in range(30):
                        HLY.com_send1(HLY.create_data(1, 1, fz_oh, fz_oh, 0))
                        time.sleep(1)
                    break
                else:
                    continue

            while True:
                report_data = re.search('sendStr', HLY.com_read())
                if report_data:
                    print('设备已进行主动上报，等待15s再进行OLC与AT检查')
                    time.sleep(15)
                    oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                                '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
                    print('液位高度为：' + str(oh_data))
                    assert oh_data == [1], '探头液位值小于等于盲区值时，数据不能被接收！！'
                    break
                else:
                    continue
        else:
            continue


def test_morethan_fade_filter_ft():
    print('已开始进行泛特大于盲区值过滤的功能测试')
    print('现将液位值初始化至1')
    HLY.init_data(1, 1, 1, 1, 0)

    cloud.fz = randint(1, 98)
    fz_oh = randint((cloud.fz*100) + 1, 12000)
    cloud.send_device_datapoint()
    time.sleep(70)

    while True:
        fz_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                        '$...dataPoints[?(@.dataPointName == "FZ" )].dataPointReportedValue')
        if fz_data == [cloud.fz]:
            print('当前盲区值已修改至%s' % cloud.fz)
            while True:
                start_collect = re.search('sent done', HLY.com_read())
                if start_collect:
                    print('正在模拟探头数据，液位高度为%s' % fz_oh)
                    for i in range(30):
                        HLY.com_send1(HLY.create_data(1, 1, fz_oh, fz_oh, 0))
                        time.sleep(1)
                    break
                else:
                    continue

            while True:
                report_data = re.search('sendStr', HLY.com_read())
                if report_data:
                    print('设备已进行主动上报，等待15s再进行OLC与AT检查')
                    time.sleep(15)
                    oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                                '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
                    print('液位高度为：' + str(oh_data))
                    assert oh_data == [fz_oh], '探头液位值大于盲区值时，数据可以正常接收！！'
                    break
                else:
                    continue
        else:
            continue