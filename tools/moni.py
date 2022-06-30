# /*
#  * @Author: luo zhenjie 
#  * @Date: 2022-06-30 10:32:24 
#  * @Last Modified by:   luo zhenjie 
#  * @Last Modified time: 2022-06-30 10:32:24 
#  */

from asyncio.windows_events import NULL
from time import sleep
import serial,re,fileinput


def del_firstline():
    for line1 in fileinput.input("2.txt", inplace = 1):
        if not fileinput.isfirstline():
            print(line1.replace("\n", ""))

def moni():
    com = serial.Serial("COM17",9600, bytesize=8, parity='N', stopbits=1, timeout=1)
    com.is_open
    com1 = serial.Serial("COM9",115200, bytesize=8, parity='N', stopbits=1, timeout=1)
    com1.is_open
    while True:
        if com1.in_waiting>0:
            str = NULL
            str=com1.read(com1.in_waiting).decode('latin1')
            print(str)
            searchObj = re.search( r'0?(13|14|15|18|17)[0-9]{9}', str, re.M|re.I)
            if searchObj:
                for i in range(10):
                    f = open('2.txt')
                    line = f.readline().encode()
                    line = line[:-1]
                    com.write(line)
                    f.close()
                    str=com1.read(com1.in_waiting).decode('latin1')
                    print(str)
                    del_firstline()
                    sleep(1)
                searchObj = NULL
            else:
                continue


if __name__ =='__main__':
    moni()
    