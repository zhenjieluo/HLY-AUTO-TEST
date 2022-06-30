# /*
#  * @Author: luo zhenjie 
#  * @Date: 2022-06-30 10:32:47 
#  * @Last Modified by:   luo zhenjie 
#  * @Last Modified time: 2022-06-30 10:32:47 
#  */

import pandas as pd

def makedist():
    df = pd.read_excel('4.xls',engine='xlrd')
    for x in range(4737):
        singnl = df.iat[x,0]
        result = df.iat[x,1]
        real = df.iat[x,2]
        shake = df.iat[x,3]
        angle = df.iat[x,4]
        data = str(angle).zfill(4)+','+str(shake).zfill(2)+','+str(result).zfill(4)+','+str(real).zfill(4)+','+str(singnl).zfill(4)+',0200,'
        b = []
        for i in data:
            a=ord(i)
            b.append(a)
        c = b[:28]
        with open('2.txt','a')as f:
            f.write('*XD,'+ data +str(sum(c))+'#'+'\n')
if __name__ =='__main__':
    makedist()