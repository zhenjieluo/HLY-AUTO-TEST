# /*
#  * @Author: luo zhenjie 
#  * @Date: 2022-06-30 10:32:57 
#  * @Last Modified by:   luo zhenjie 
#  * @Last Modified time: 2022-06-30 10:32:57 
#  */

def ascii1():
    while True:
        s=input('请输入:')
        b =[]
        for i in s:
            a=ord(i)
            b.append(a)
            l = len(b)
        if l == 28: 
            print('*XD,'+ s +str(sum(b))+'#')
        elif l > 28:
            c = b[:28]
            print('*XD,'+ s +str(sum(c))+'#') 
        s1 =input('输入Q键后退出！！！')
        if s1 == 'Q':
            return False
if __name__ =='__main__':
    ascii1()