# /*
#  * @Author: luo zhenjie 
#  * @Date: 2022-07-01 15:02:02 
#  * @Last Modified by:   luo zhenjie 
#  * @Last Modified time: 2022-07-01 15:02:02 
#  */

import sys
import time
import jsonpath

from api.IOT_CLOUD_API import IOT_CLOUD_API

sys.path.insert(0, 'C:/Users/X-X/Desktop/HLY-AUTO-TEST')

cloud = IOT_CLOUD_API()

cloud.username = 'luozhenjie'
cloud.password = 'aa123456'
cloud.device_id = 'BllRQflFa1jvbcZE4DYA'


def test_check_fz():
    for i in range(1, 99):
        cloud.fz = 1
        cloud.send_device_datapoint()
        time.sleep(60)
        device_data = cloud.get_device_detail()
        fz_data = jsonpath.jsonpath(device_data, '$...dataPoints[?(@.dataPointName == "FZ" )].dataPointReportedValue')
        print(fz_data)
        assert fz_data == cloud.fz, '设置盲区值 %s 失败' % cloud.fz
        cloud.fz += 1


def test_check_sn():
    for i in range(1, 30):
        cloud.sn = 1
        cloud.send_device_datapoint()
        time.sleep(60)
        device_data = cloud.get_device_detail()
        sn_data = jsonpath.jsonpath(device_data, '$...dataPoints[?(@.dataPointName == "SN" )].dataPointReportedValue')
        print(sn_data)
        assert sn_data == cloud.sn, '设置样本数 %s 失败' % cloud.sn
        cloud.sn += 1


def test_check_rf():
    for i in range(2, 10):
        cloud.rf = 2
        cloud.send_device_datapoint()
        time.sleep(60)
        device_data = cloud.get_device_detail()
        rf_data = jsonpath.jsonpath(device_data, '$...dataPoints[?(@.dataPointName == "RF" )].dataPointReportedValue')
        print(rf_data)
        assert rf_data == cloud.rf, '设置工时上报频率 %s 失败' % cloud.rf
        cloud.rf += 1
