#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/8/10 10:16
# @Author  : luozhenjie
# @FileName: test_serial.py
# @Software: PyCharm
import json
import random

import serial
import time
import threading


ser = serial.Serial('com3', 115200)

def test_neicun_send():
    while True:
        for i in range(1, 99):    #接探头后测试
            j = i*100
            parameter = {
                "cmd": "devConfig",
                "params":
                    {
                        "fade_value": str(j)
                    }
            }
            data = json.dumps(parameter)
            ser.write(data.encode())
            time.sleep(60)


def test_neicun_read():
    while True:
        try:
            while ser.in_waiting > 0:
                time.sleep(0.1)
                data = ser.read(ser.in_waiting).decode('latin1')
                t = time.time()
                ct = time.ctime(t)
                print(ct, ':')
                print(data)

                f = open('test.txt', 'a')
                f.writelines(ct)
                f.writelines(':\n')
                f.writelines(data)
                f.close()
        except:
            while ser.in_waiting > 0:
                time.sleep(0.1)
                data = ser.read(ser.in_waiting).decode('latin1')
                t = time.time()
                ct = time.ctime(t)
                print(ct, ':')
                print(data)

                f = open('test.txt', 'a')
                f.writelines(ct)
                f.writelines(':\n')
                f.writelines(data)
                f.close()


if __name__ == '__main__':
    if __name__ == '__main__':
        t1 = threading.Thread(target=test_neicun_send, name='sends')
        t2 = threading.Thread(target=test_neicun_read, name='reads')
        t1.start()
        t2.start()