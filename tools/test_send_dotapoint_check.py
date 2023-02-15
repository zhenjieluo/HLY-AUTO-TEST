# /*
#  * @Author: luo zhenjie 
#  * @Date: 2022-07-01 15:02:02 
#  * @Last Modified by:   luo zhenjie 
#  * @Last Modified time: 2022-07-01 15:02:02 
#  */
import re
import sys
import time
import jsonpath

from api.IOT_CLOUD_API import IOT_CLOUD_API
from api.HLY_API import HLY_API
from loguru import logger
sys.path.insert(0, 'C:/Users/X-X/Desktop/HLY-AUTO-TEST')

cloud = IOT_CLOUD_API()
HLY = HLY_API()

cloud.username = 'luozhenjie'
cloud.password = 'aa123456'

# cloud.username = 'xiejiaxing'
# cloud.password = 'xjx1703002'
# cloud.device_id = 'BmEtZdx62WMyeoY04HIA'
# HLY.com = 'com3'
cloud.device_id = 'BnO8UIpJbWZtWAZH4EUA'

# cloud.username = 'luozhenjie1'
# cloud.password = 'aa123456'
# cloud.device_id = 'BkHEbIpw5WTZcsZs4FAA'
# HLY.com = 'com3'
HLY.com = 'com5'
HLY.port = 115200
data = []


def test_check_dyp_fz():
    logger.info('请接入电应普探头！！，10s后开始测试')
    time.sleep(10)
    for i in range(1, 1999):    #接探头后测试
        cloud.fz = str(i)
        cloud.send_device_datapoint()
        logger.info('-----盲区值下发为:%s' % i)
        time.sleep(120)
        while True:
            fz_data = check_dyp_fz_value()
            if fz_data == []:
                continue
            else:
                break
        logger.info('盲区值已修改为:%s' % fz_data)
        assert fz_data == [cloud.fz], '设置盲区值 %s 失败' % cloud.fz


def check_dyp_fz_value():
    t_end = time.time() + 5
    HLY.com_send('query parameters')
    while time.time() < t_end:
        ser_data = HLY.com_read()
        data.append(ser_data)
    fz_data = re.findall('(?<=DYP fade value: ).[0-9]*', str(data))
    data.clear()
    return fz_data


def check_ft_fz_value():
    t_end = time.time() + 5
    HLY.com_send('query parameters')
    while time.time() < t_end:
        ser_data = HLY.com_read()
        data.append(ser_data)
    fz_data = re.findall('(?<=FT fade value: ).[0-9]*', str(data))
    data.clear()
    return fz_data


def test_check_ft_fz():
    logger.info('请接入泛特探头！！，10s后开始测试')
    time.sleep(10)
    for i in range(1, 99):    #接探头后测试
        j = i*100
        cloud.fz = str(j)
        cloud.send_device_datapoint()
        logger.info('-----盲区值下发为:%s' % j)
        time.sleep(120)
        while True:
            fz_data = check_ft_fz_value()
            if fz_data == []:
                continue
            else:
                break
        logger.info('盲区值已修改为:%s' % fz_data)
        assert fz_data == [cloud.fz], '设置盲区值 %s 失败' % cloud.fz

def test_neicun():
    for i in range(10, 30):    #接探头后测试
        cloud.sn = str(i)
        cloud.send_device_datapoint()
        time.sleep(60)
# def test_check_sn():
#     for i in range(1, 30):
#         cloud.sn = 1
#         cloud.send_device_datapoint()
#         time.sleep(60)
#         device_data = cloud.get_device_detail()
#         sn_data = jsonpath.jsonpath(device_data, '$...dataPoints[?(@.dataPointName == "SN" )].dataPointReportedValue')
#         logger.info(sn_data)
#         assert sn_data == cloud.sn, '设置样本数 %s 失败' % cloud.sn
#         cloud.sn += 1
#
#
# def test_check_rf():
#     for i in range(2, 10):
#         cloud.rf = 2
#         cloud.send_device_datapoint()
#         time.sleep(60)
#         device_data = cloud.get_device_detail()
#         rf_data = jsonpath.jsonpath(device_data, '$...dataPoints[?(@.dataPointName == "RF" )].dataPointReportedValue')
#         logger.info(rf_data)
#         assert rf_data == cloud.rf, '设置工时上报频率 %s 失败' % cloud.rf
#         cloud.rf += 1
