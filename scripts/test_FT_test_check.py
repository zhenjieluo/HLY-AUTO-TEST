# /*
#  * @Author: luo zhenjie 
#  * @Date: 2022-06-29 11:05:13 
#  * @Last Modified by:   luo zhenjie 
#  * @Last Modified time: 2022-06-29 11:05:13 
#  */

import sys
sys.path.insert(0, '/')
import re
import time
import allure
from api.LOG import logger
from api.HLY_API import HLY_API


HLY = HLY_API()

HLY.com = 'com5'
HLY.port = 115200
data = []


@allure.title('FT测试校验')
def test_FT():
    num = 0
    logger.info('开始进行FT测试校验')
    HLY.com_send('reboot')
    rb_data = re.search('wait test cmd counter', HLY.com_read())
    time.sleep(1)
    HLY.com_send('start FT')

    t_end = time.time() + 50
    while time.time() < t_end:
        ser_data = HLY.com_read()
        data.append(ser_data)
    ft_start = re.search('start FT', str(data))
    acc_start = re.search('FT acceleration', str(data))
    flash_start = re.search('FT flash', str(data))
    battery_start = re.search('FT battery', str(data))
    rs485_start = re.search('FT rs485', str(data))
    gps_start = re.search('FT GPS', str(data))
    cat1_start = re.search('FT cat1', str(data))
    ft_end = re.search('iap start!', str(data))

    if ft_start or acc_start or flash_start or battery_start or rs485_start or gps_start or cat1_start or ft_end:
        if ft_start:
            logger.info('FT测试开始')
            num += 1
        if acc_start:
            logger.info('加速度传感器测试已完成')
            num += 1
        if flash_start:
            logger.info('flash测试已完成')
            num += 1
        if battery_start:
            logger.info('电池测试已完成')
            num += 1
        if rs485_start:
            logger.info('485通讯测试已完成')
            num += 1
        if gps_start:
            logger.info('GPS测试已完成')
            num += 1
        if cat1_start:
            logger.info('4G模组测试已完成')
            num += 1
        if ft_end:
            logger.info('FT 测试已完成')
            num += 1
    assert num == 8, 'FT生产测试异常'
