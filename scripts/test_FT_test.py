# /*
#  * @Author: luo zhenjie 
#  * @Date: 2022-06-29 11:05:13 
#  * @Last Modified by:   luo zhenjie 
#  * @Last Modified time: 2022-06-29 11:05:13 
#  */

import re
import sys
import time

from api.HLY_API import HLY_API

sys.path.insert(0, 'C:/Users/X-X/Desktop/HLY-AUTO-TEST')


HLY = HLY_API()

HLY.com = 'com5'
HLY.port = 115200
data = []


def test_FT():
    num = 0
    print('------------- FT test -------------')
    HLY.com_send('start FT')

    t_end = time.time() + 20
    while time.time() < t_end:
        ser_data = HLY.com_read()
        data.append(ser_data)

    ft_start = re.search('start FT', str(data))
    acc_start = re.search('FT acceleration pass' or 'FT acceleration fail', str(data))
    flash_start = re.search('FT flash pass' or 'FT flash fail', str(data))
    battery_start = re.search('FT battery pass' or 'FT battery fail', str(data))
    rs485_start = re.search('FT rs485 pass' or 'FT rs485 fail', str(data))
    gps_start = re.search('FT GPS pass' or 'FT GPS fail', str(data))
    cat1_start = re.search('FT cat1 pass' or 'FT cat1 fail', str(data))
    ft_end = re.search('iap start!', str(data))

    if ft_start or acc_start or flash_start or battery_start or rs485_start or gps_start or cat1_start or ft_end:
        if ft_start:
            print('------------- FT测试已完成 -------------')
            num += 1
        if acc_start:
            print('------------- 加速度传感器测试已完成 -------------')
            num += 1
        if flash_start:
            print('------------- flash测试已完成 -------------')
            num += 1
        if battery_start:
            print('------------- 电池测试已完成 -------------')
            num += 1
        if rs485_start:
            print('------------- 485通讯测试已完成 -------------')
            num += 1
        if gps_start:
            print('------------- GPS测试已完成 -------------')
            num += 1
        if cat1_start:
            print('------------- 4G模组测试已完成 -------------')
            num += 1
        if ft_end:
            print('------------- FT 测试已完成 -------------')
            num += 1
    assert num == 8, '------------- FT生产测试异常 -------------'
