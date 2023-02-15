#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/12/1 15:48
# @Author  : luozhenjie
# @FileName: test_matploblib.py
# @Software: PyCharm
import time

import jsonpath
import matplotlib.pyplot as plt
import json,math
from matplotlib import colors
from api.IOT_CLOUD_API import IOT_CLOUD_API
from numpy.lib.npyio import load


cloud = IOT_CLOUD_API()


cloud.username = 'luozhenjie'
cloud.password = 'aa123456'
cloud.device_id = 'Bm35VEJuEmaveUZx4GYA'
x_data = []
y_data = []
def test_make_figure():
    fig = plt.figure()
    ax=fig.add_subplot(111)
    plt.ion()
    a = 0
    while True:
        a += 1
        plt.clf()
        wtime_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                    '$...dataPoints[?(@.dataPointName == "RT" )].dataPointReportedValue')
        wtime = int(wtime_data[0])
        x_data.append(a)
        y_data.append(wtime)

        plt.plot(x_data,y_data,label ='work time = %s s'%(wtime),color = 'red')
        plt.xlim(0,a)
        plt.ylim(-10,60)

        plt.savefig('end.jpg')
        plt.pause(60)
