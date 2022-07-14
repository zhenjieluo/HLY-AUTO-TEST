#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/7/13 9:00
# @Author  : luozhenjie
# @FileName: test_low_power_check.py
# @Software: PyCharm

# import sys
# sys.path.insert(0, 'C:/Users/X-X/Desktop/HLY-AUTO-TEST')
# import time
# import allure
# import jsonpath
# from api.LOG import logger
# from api.HLY_API import HLY_API
# from api.IOT_CLOUD_API import IOT_CLOUD_API
#
#
# HLY = HLY_API()
# cloud = IOT_CLOUD_API()
#
# HLY.com = 'com5'
# HLY.port = 115200
# HLY.com1 = 'com13'
# HLY.port1 = 9600
# cloud.username = 'luozhenjie'
# cloud.password = 'aa123456'
# cloud.device_id = 'BllRQflFa1jvbcZE4DYA'
#
#
# @allure.title('长供电状态下切换成电池供电，APS显示为2')
# def test_power_status_check():
#     """继电器开关位置"""
#     HLY.check_push_status()
#     logger.info('等待10s后开始校验数据')
#     time.sleep(10)
#     aps_data = jsonpath.jsonpath(cloud.get_device_detail(),
#                                     '$...dataPoints[?(@.dataPointName == "APS" )].dataPointReportedValue')
#     assert aps_data == [2], '切换至电池供电模式后，电源状态应为2'
#
#
# @allure.title('电池供电情况下上报频率是否为10分钟')
# def test_low_power_check():
#     aps_time_data = jsonpath.jsonpath(cloud.get_device_detail(),
#                                 '$...dataPoints[?(@.dataPointName == "APS" )].updateTime')
#     HLY.check_push_status()
#     logger.info('等待10s后开始校验数据')
#     time.sleep(10)
#     aps_time_data_1 = jsonpath.jsonpath(cloud.get_device_detail(),
#                                       '$...dataPoints[?(@.dataPointName == "APS" )].updateTime')
#     assert aps_time_data_1[0] - aps_time_data[0] <= 60, '长供电情况下上报频率应为1分钟'
#
#
# @allure.title('电池供电情况下盲区是否可以正常下发')
# def test_low_power_fz_check():
#     fz_data = jsonpath.jsonpath(cloud.get_device_detail(),
#                                     '$...dataPoints[?(@.dataPointName == "FZ" )].dataPointReportedValue')
#     fz = fz_data[0] + 1
#     cloud.fz = str(fz)
#     logger.info('下发盲区值%s' % fz)
#     cloud.send_device_datapoint()
#
#     HLY.check_push_status()
#     logger.info('已更新第一包数据，再次等待10分钟查看第二包数据')
#     time.sleep(60)
#     HLY.check_push_status()
#     logger.info('等待10s后开始校验数据')
#     time.sleep(10)
#     fz_data1 = jsonpath.jsonpath(cloud.get_device_detail(),
#                                     '$...dataPoints[?(@.dataPointName == "FZ" )].dataPointReportedValue')
#     assert fz_data1[0] == fz, '电池供电情况下，第二包数据应及时更新盲区值'
#
#
# @allure.title('电池供电情况下样本数是否可以正常下发')
# def test_low_power_sn_check():
#     sn_data = jsonpath.jsonpath(cloud.get_device_detail(),
#                                     '$...dataPoints[?(@.dataPointName == "SN" )].dataPointReportedValue')
#     sn = sn_data[0] + 1
#     cloud.sn = str(sn)
#     logger.info('下发盲区值%s' % sn)
#     cloud.send_device_datapoint()
#
#     HLY.check_push_status()
#     logger.info('已更新第一包数据，再次等待10分钟查看第二包数据')
#     time.sleep(60)
#     HLY.check_push_status()
#     logger.info('等待10s后开始校验数据')
#     time.sleep(10)
#     sn_data1 = jsonpath.jsonpath(cloud.get_device_detail(),
#                                     '$...dataPoints[?(@.dataPointName == "SN" )].dataPointReportedValue')
#     assert sn_data1[0] == sn, '电池供电情况下，第二包数据应及时更新样本数量'
#
#
# @allure.title('电池供电情况下工时上报频率是否可以正常下发')
# def test_low_power_rf_check():
#     rf_data = jsonpath.jsonpath(cloud.get_device_detail(),
#                                     '$...dataPoints[?(@.dataPointName == "RF" )].dataPointReportedValue')
#     rf = rf_data[0] + 1
#     cloud.rf = str(rf)
#     logger.info('下发盲区值%s' % rf)
#     cloud.send_device_datapoint()
#
#     HLY.check_push_status()
#     logger.info('已更新第一包数据，再次等待10分钟查看第二包数据')
#     time.sleep(60)
#     HLY.check_push_status()
#     logger.info('等待10s后开始校验数据')
#     time.sleep(10)
#     rf_data1 = jsonpath.jsonpath(cloud.get_device_detail(),
#                                     '$...dataPoints[?(@.dataPointName == "RF" )].dataPointReportedValue')
#     assert rf_data1[0] == rf, '电池供电情况下，第二包数据应及时更新工时上报频率'
#
#
# @allure.title('电池供电状态下切换成长供电，APS显示为1')
# def test_power_status_check():
#     """继电器开关位置"""
#     HLY.check_push_status()
#     logger.info('等待10s后开始校验数据')
#     time.sleep(10)
#     aps_data = jsonpath.jsonpath(cloud.get_device_detail(),
#                                     '$...dataPoints[?(@.dataPointName == "APS" )].dataPointReportedValue')
#     assert aps_data == [1], '切换至长供电模式后，电源状态应为1'
#
#
# @allure.title('主供电情况下上报频率是否为1分钟')
# def test_main_power_check():
#     aps_time_data = jsonpath.jsonpath(cloud.get_device_detail(),
#                                 '$...dataPoints[?(@.dataPointName == "APS" )].updateTime')
#     HLY.check_push_status()
#     logger.info('等待10s后开始校验数据')
#     time.sleep(10)
#     aps_time_data_1 = jsonpath.jsonpath(cloud.get_device_detail(),
#                                       '$...dataPoints[?(@.dataPointName == "APS" )].updateTime')
#     assert aps_time_data_1[0] - aps_time_data[0] <= 10, '长供电情况下上报频率应为1分钟'
#
#
# @allure.title('电池使用时长能否正常记录')
# def test_low_power_time_statistics_check():
#     """继电器开关位置"""
#     HLY.check_push_status()
#     logger.info('等待10s后开始校验数据')
#     time.sleep(10)
#     logger.info('开始校验电池状态下电池使用时长统计是否正确')
#     aps_time_data = jsonpath.jsonpath(cloud.get_device_detail(),
#                                       '$...dataPoints[?(@.dataPointName == "APS" )].updateTime')
#     logger.info('已更新第一包数据，再次等待10分钟查看第二包数据')
#     time.sleep(60)
#     HLY.check_push_status()
#     logger.info('等待10s后开始校验数据')
#     aps_time_data1 = jsonpath.jsonpath(cloud.get_device_detail(),
#                                       '$...dataPoints[?(@.dataPointName == "APS" )].updateTime')
#     battery_data = jsonpath.jsonpath(cloud.get_device_detail(),
#                              '$...dataPoints[?(@.dataPointName == "BPR" )].dataPointReportedValue')
#     battery_time = aps_time_data1[0] - aps_time_data[0]
#     error_data = abs(battery_time - battery_data[0])
#     assert error_data <= 1, '电池使用时长统计误差过大'
#
#     logger.info('开始校验电池使用时长统计在切换至长供电后是否会清零')
#     """继电器开关位置"""
#     HLY.check_push_status()
#     logger.info('等待10s后开始校验数据')
#     time.sleep(10)
#     battery_data1 = jsonpath.jsonpath(cloud.get_device_detail(),
#                                      '$...dataPoints[?(@.dataPointName == "BPR" )].dataPointReportedValue')
#     assert battery_data1 == [0], '电池模式切换至长供电模式后，电池统计时长应清零'