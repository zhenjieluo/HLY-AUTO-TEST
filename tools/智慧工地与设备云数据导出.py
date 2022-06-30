# /*
#  * @Author: luo zhenjie 
#  * @Date: 2022-06-30 10:31:01 
#  * @Last Modified by:   luo zhenjie 
#  * @Last Modified time: 2022-06-30 10:31:01 
#  */

from ast import Param
from email import header
from email.header import Header
from logging import NullHandler
from platform import machine
from sqlite3 import Time
from turtle import rt
from urllib import request, response
import jmespath
from jmespath import search
import operator
from functools import reduce
import numpy as np
import requests,json,openpyxl,time,datetime
from tqdm import trange

from yaml import serialize


url1 = 'http://sby.kindaiot.com/api/project/device-origin-data/search'
url2 = 'http://kindaiot.com/api/csoi/tm/thing/origin/data'
def getData():
    try:
        num = 1
        pingtai = input('请输入期望导出的平台数据，1为智慧工地数据，2为设备云数据------')
        if pingtai == '1':
            machineid = input('请输入机械ID------')
            url = url2
            startTime = input('请输入开始时间，格式2022-04-28 10:00:00------')
            timeArray = time.strptime(startTime, "%Y-%m-%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            endTime  =input('请输入截止时间，格式2022-04-28 10:00:00------')
            timeArray1 = time.strptime(endTime, "%Y-%m-%d %H:%M:%S")
            timeStamp1 = int(time.mktime(timeArray1))
            headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) browse-thing-data/0.1.0 Chrome/91.0.4472.164 Electron/13.6.3 Safari/537.36'
            }
            params = {
            'machineId':machineid,  #'BWKrSsFP7EiGc2pEgEgA'
            'startTime':(timeStamp*1000),  #1650902400000
            'endTime':(timeStamp1*1000),      #1651075200000
            'page':1,
            'per_page':5
                    }
            response = requests.get(url=url,headers=headers,params=params)
            data = response.text
            data1 = json.loads(data)
            if data1['status'] == 200:
                print('---------已开始数据导出，请稍后---------')
                wb = openpyxl.Workbook()
                sheet = wb.active
                sheet.title ='真实数据'
                cycle = data1['responseData']['total']
                page = (cycle+9)//10
                starttime = datetime.datetime.now()
                for i in trange(page):
                    x = 0
                    url = url2
                    params1 = {
                            'machineId':machineid,  #'BWKrSsFP7EiGc2pEgEgA'
                            'startTime':(timeStamp*1000),  #1650902400000
                            'endTime':(timeStamp1*1000),      #1651075200000
                            'page':num,
                            'per_page':10
                        }
                    num += 1
                    response1 = requests.get(url=url,headers=headers,params=params1)
                    data2 = response1.text
                    data3 = json.loads(data2)
                    size = len(data3['responseData']['dataList'])
                    for i in range(size):
                        TIME = othertime(data3['responseData']['dataList'][x]['timestamp'])
                        data4 = search('responseData.dataList[%s].[dataPoints[].[dataPointValue]]'%x,data3)
                        data5 = np.ravel(data4)
                        data6 = search('responseData.dataList[%s].[dataPoints[].[dataPointAlias]]'%x,data3)
                        data7 = np.ravel(data6)
                        timestamp4 = search('responseData.dataList[%s].[dataPoints[].[dataPointTimestamp]]'%x,data3)
                        timestamp5 = np.ravel(timestamp4)
                        L = []
                        M = []
                        S = []
                        Q = []
                        for i in range(len(timestamp5)):
                            l = othertime(timestamp5[i])
                            L.append(l)
                        for i in range(len(data5)):
                            m = data5[i]
                            M.append(m)
                        for i in range(len(data7)):
                            q = data7[i]
                            Q.append(q)
                        sheetdata = reduce(operator.add,list(zip(L,Q,M)))
                        for i in range(len(sheetdata)):
                            s = sheetdata[i]
                            S.append(s)
                        S.insert(0,TIME)
                        sheet.append(S)
                        x += 1
                wb.save('real.xlsx')
                endtime = datetime.datetime.now()
                usetime = (endtime - starttime).seconds
                print ('累计用时'+str(usetime)+'s')
                print('############全部数据已导入完成############')
                input('--------输入回车后退出--------')
            elif BaseException != None:
                print('未找到对应的数据信息')
                input('--------输入回车后退出--------')
        elif pingtai == '2':
            thingId = input('请输入设备ID------')
            url = url1
            startTime = input('请输入开始时间，格式2022-04-28 10:00:00------')
            timeArray = time.strptime(startTime, "%Y-%m-%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            endTime  =input('请输入截止时间，格式2022-04-28 10:00:00------')
            timeArray1 = time.strptime(endTime, "%Y-%m-%d %H:%M:%S")
            timeStamp1 = int(time.mktime(timeArray1))
            headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) browse-thing-data/0.1.0 Chrome/91.0.4472.164 Electron/13.6.3 Safari/537.36'
            }
            params = {
            'category' : 'thing',
            'thingId':thingId,  #'BWKrSsFP7EiGc2pEgEgA'
            'gatewayId':'',
            'startTime':(timeStamp*1000),  #1650902400000
            'endTime':(timeStamp1*1000),      #1651075200000
            'page':1,
            'perPage':10
                    }
            response = requests.get(url=url,headers=headers,params=params)
            data = response.text
            data1 = json.loads(data)
            if data1['status'] == 200:
                print('---------已开始数据导出，请稍后---------')
                wb = openpyxl.Workbook()
                sheet = wb.active
                sheet.title ='真实数据'
                cycle = data1['data']['total']
                page = (cycle+9)//10
                starttime = datetime.datetime.now()
                for i in trange(page):
                    x = 0
                    url = url1
                    params1 = {
                            'category' : 'thing',
                            'thingId':thingId,  #'BWKrSsFP7EiGc2pEgEgA'
                            'gatewayId':'',
                            'startTime':(timeStamp*1000),  #1650902400000
                            'endTime':(timeStamp1*1000),      #1651075200000
                            'page':num,
                            'perPage':10
                                    }
                    num += 1
                    response1 = requests.get(url=url,headers=headers,params=params1)
                    data2 = response1.text
                    data3 = json.loads(data2)
                    size = len(data3['data']['dataList'])
                    for i in range(size):
                        TIME = othertime(data3['data']['dataList'][x]['timestamp'])
                        data4 = jmespath.search('data.dataList[%s].[dataPoints[].[dataPointValue]]'%x,data3)
                        data5 = np.ravel(data4)
                        data6 = jmespath.search('data.dataList[%s].[dataPoints[].[dataPointAlias]]'%x,data3)
                        data7 = np.ravel(data6)
                        timestamp4 = jmespath.search('data.dataList[%s].[dataPoints[].[dataPointTimestamp]]'%x,data3)
                        timestamp5 = np.ravel(timestamp4)
                        L = []
                        M = []
                        S = []
                        Q = []
                        for i in range(len(timestamp5)):
                            l = othertime(timestamp5[i])
                            L.append(l)
                        for i in range(len(data5)):
                            m = data5[i]
                            M.append(m)
                        for i in range(len(data7)):
                            q = data7[i]
                            Q.append(q)
                        sheetdata = reduce(operator.add,list(zip(L,Q,M)))
                        for i in range(len(sheetdata)):
                            s = sheetdata[i]
                            S.append(s)
                        S.insert(0,TIME)
                        sheet.append(S)
                        x +=1
                wb.save('real.xlsx')
                endtime = datetime.datetime.now()
                usetime = (endtime - starttime).seconds
                print ('累计用时'+str(usetime)+'s')
                print('############全部数据已导入完成############')
                input('--------输入回车后退出--------')
            elif BaseException != None:
                print('未找到对应的数据信息')
                input('--------输入回车后退出--------')
        else:
            print('---------数据异常,输入回车后退出---------')
    except:
        input('--------数据异常,输入回车后退出--------')
def othertime(realtime):
    if realtime == None:
        return 0 
    else:
        timestamp = realtime/1000
        timeArray = time.localtime(timestamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime
if __name__ =='__main__':
    getData()