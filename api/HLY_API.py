# /*
#  * @Author: luo zhenjie 
#  * @Date: 2022-06-29 10:23:51 
#  * @Last Modified by:   luo zhenjie 
#  * @Last Modified time: 2022-06-29 10:23:51 
#  */

from importlib.resources import read_text
from msilib.schema import Class
import serial



class HLY_API(object):

    def __init__(self):
        self.com  = ''
        self.port = ''

    def com_send(self,sendtext):      #串口发送
        com  = self.com
        port = self.port
        ser = serial.Serial(com, port)
        ser.write(sendtext.encode())
        ser.close()

    def com_read(self):                #串口读取
        com  = self.com
        port = self.port
        ser = serial.Serial(com, port)
        while True:
            readtext = ''
            while ser.in_waiting > 0:
                readtext = ser.read(ser.in_waiting).decode('latin1')  # 一个一个的读取
                return readtext
    

