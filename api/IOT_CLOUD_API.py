# /*
#  * @Author: luo zhenjie 
#  * @Date: 2022-07-01 09:37:59 
#  * @Last Modified by:   luo zhenjie 
#  * @Last Modified time: 2022-07-01 09:37:59 
#  */


import ddddocr
import json

import requests
import sys

from retrying import retry

sys.path.insert(0, 'C:/Users/X-X/Desktop/HLY-AUTO-TEST')


class IOT_CLOUD_API(object):

    def __init__(self):
        self.username = ''
        self.password = ''
        self.captchaId = ''
        self.captcha = ''
        self.iot_url = 'http://kindaiot.com'
        self.device_id = ''
        self.token = None
        self.cmd = '0'
        self.fv = ''
        self.fz = ''
        self.rf = ''
        self.sn = ''

    @staticmethod
    def get_html_and_get_response(url, data, headers):
        response = requests.get(url=url, params=data, headers=headers)
        result = response.text
        return json.loads(result)

    @staticmethod
    def post_html_and_get_response(url, data, headers):
        response = requests.post(url=url, json=data, headers=headers)
        result = response.text
        return json.loads(result)

    @staticmethod
    def put_html_and_get_response(url, data, headers):
        response = requests.put(url=url, json=data, headers=headers)
        result = response.text
        return json.loads(result)

    def get_captcha(self):
        iot_url = self.iot_url
        url = iot_url + '/api/uums/accounts/captcha'
        header = {
            'Content-Type': 'application/json;charset=UTF-8'
        }
        result = self.get_html_and_get_response(url, None, header)
        return result

    def retry_if_result_none(result):
        return result['status'] != 200

    @retry(retry_on_result=retry_if_result_none)
    def login(self):
        ocr = ddddocr.DdddOcr()
        captcha_result = self.get_captcha()
        username = self.username
        password = self.password
        iot_url = self.iot_url
        image_data = captcha_result['responseData']['image']
        captcha_pic_base64_data = image_data.split(',')[1]
        captcha = ocr.classification(None, captcha_pic_base64_data)
        captcha_id = captcha_result['responseData']['captchaId']
        url = iot_url + '/api/uums/accounts/auth'
        data = {
            'username': username,
            'password': password,
            'captchaId': captcha_id,
            'captcha': captcha,
        }
        header = {
            'Content-Type': 'application/json;charset=UTF-8'
        }
        result = self.post_html_and_get_response(url, data, header)
        return result

    def get_device_detail(self):
        iot_url = self.iot_url
        device_id = self.device_id
        token = self.token
        url = iot_url + '/api/itms/devices/' + device_id + '/datapoints/details'
        if token:
            token_in_use = token
        else:
            login_result = self.login()
            token_in_use = login_result['responseData']['accessToken']
        header = {
            'accessToken': token_in_use,
            'Content-Type': 'application/json;charset=UTF-8'
        }
        result = self.get_html_and_get_response(url, None, header)
        return result

    def send_device_datapoint(self):
        iot_url = self.iot_url
        device_id = self.device_id
        token = self.token
        cmd = self.cmd
        fv = self.fv
        fz = self.fz
        rf = self.rf
        sn = self.sn
        url = iot_url + '/api/itms/devices/' + device_id + '/datapoints'
        if token:
            token_in_use = token
        else:
            login_result = self.login()
            token_in_use = login_result['responseData']['accessToken']
        header = {
            'accessToken': token_in_use,
            'Content-Type': 'application/json'
        }
        data = {
            'dataPoints': [{
                    'dataPointName': 'CMD',
                    'dataPointDesiredValue': cmd
                },
                {
                    'dataPointName': 'FV',
                    'dataPointDesiredValue': fv
                },
                {
                    'dataPointName': 'FZ',
                    'dataPointDesiredValue': fz
                },
                {
                    'dataPointName': 'RF',
                    'dataPointDesiredValue': rf
                },
                {
                    'dataPointName': 'SN',
                    'dataPointDesiredValue': sn
                }
            ]
        }
        result = self.put_html_and_get_response(url, data, header)
        return result

    def send_device_datapoint1(self):
        iot_url = self.iot_url
        device_id = self.device_id
        token = self.token
        cmd = self.cmd
        fv = self.fv
        fz = self.fz
        rf = self.rf
        sn = self.sn
        url = iot_url + '/api/itms/devices/' + device_id + '/datapoints'
        if token:
            token_in_use = token
        else:
            login_result = self.login()
            token_in_use = login_result['responseData']['accessToken']
        header = {
            'accessToken': token_in_use,
            'Content-Type': 'application/json'
        }
        data = {
            'dataPoints': [{
                    'dataPointName': 'CMD',
                    'dataPointDesiredValue': cmd
                },
                {
                    'dataPointName': 'FV',
                    'dataPointDesiredValue': fv
                },
                {
                    'dataPointName': 'URL',
                    'dataPointDesiredValue': ''
                }
            ]
        }
        result = self.put_html_and_get_response(url, data, header)
        return result