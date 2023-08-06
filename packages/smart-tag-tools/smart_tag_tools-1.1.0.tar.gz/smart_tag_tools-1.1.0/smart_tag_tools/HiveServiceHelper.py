#!/usr/bin/python3
# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
import requests
import base64
import hmac
from hashlib import sha1


class HiveSearchApi:
    """
    hive查询类
    """
    system_secret_key = "e2c84557fc9c4d069bfc7b958abccdca"
    user_code = "admin"
    site_code = operate_site = "S1"
    system_code = "MAM"
    contenttype = 'application/json'
    GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

    def __init__(self, ip, port, timeout):
        self.url = "http://{}:{}/sobeyhive-bp/v1/entity".format(ip, port)
        self.timeout = timeout

    def get_entityinfo_url(self, contentid):
        data = {'contentid': contentid, 'pathtype': 1}
        dateStr = (datetime.utcnow() - timedelta(minutes=0)).strftime(self.GMT_FORMAT)
        sign = self.__get_request_signature_header('GET', dateStr, self.contenttype)
        headers = {
            'sobeyhive-http-site': self.site_code,
            'sobeyhive-http-date': dateStr,
            'sobeyhive-http-authorization': sign,
            'sobeyhive-http-system': self.system_code,
            'sobeyhive-http-operate-site': self.operate_site,
            'Content-Type': self.contenttype,
            'current-user-code': self.user_code
        }
        res = requests.get(url=self.url, headers=headers, params=data, timeout=self.timeout)
        return res.json()

    def __get_request_signature_header(self, method, dateStr, contenttype='application/json'):
        sign = self.__get_request_signature(
            method, '', self.system_secret_key, dateStr, contenttype)

        return 'SobeyHive {system_code}:{sign}'.format(system_code=self.system_code, sign=sign)

    @staticmethod
    def __get_request_signature(method, conentmd5, encryptKey, dateStr, contenttype='application/json'):
        stringToSign = '{method}\n{conentmd5}\n{contenttype}\n{dateStr}'.format(method=method,
                                                                                conentmd5=conentmd5,
                                                                                contenttype=contenttype,
                                                                                dateStr=dateStr)

        hmac_code = hmac.new(encryptKey.encode(), stringToSign.encode(), sha1)
        signature = base64.b64encode(hmac_code.digest())
        return str(signature, 'utf8')
