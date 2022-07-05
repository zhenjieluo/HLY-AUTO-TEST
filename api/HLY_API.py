# /*
#  * @Author: luo zhenjie 
#  * @Date: 2022-06-29 10:23:51 
#  * @Last Modified by:   luo zhenjie 
#  * @Last Modified time: 2022-06-29 10:23:51 
#  */

import serial


class HLY_API(object):

    def __init__(self):
        self.com = ''
        self.port = ''
        self.com1 = ''
        self.port1 = ''

    def com_send(self, sendtext):  # 串口发送
        com = self.com
        port = self.port
        try:
            ser = serial.Serial(com, port)
        except:
            ser = serial.Serial(com, port)
        ser.write(sendtext.encode())
        ser.close()

    def com_send1(self, sendtext):  # 串口发送
        com1 = self.com1
        port1 = self.port1
        try:
            ser = serial.Serial(com1, port1)
        except:
            ser = serial.Serial(com1, port1)
        ser.write(sendtext.encode())
        ser.close()

    def com_read(self):  # 串口读取
        com = self.com
        port = self.port
        try:
            ser = serial.Serial(com, port)
        except:
            ser = serial.Serial(com, port)
        while True:
            readtext = ''
            while ser.in_waiting > 0:
                readtext = ser.read(ser.in_waiting).decode('latin1')  # 一个一个的读取
                return readtext
