#!/usr/bin/python3
# -*- coding:utf-8 -*-
import requests


class STAGMApi:
    """
    STAGM接口
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def tag_tidy(self, data):
        try:
            res = requests.post(
                url='http://{}:{}{}/v1/tag/tidy'.format(self.kwargs['ip'], self.kwargs['port'],
                                                        self.kwargs['UrlPrefix']),
                json=data,
                timeout=self.kwargs['timeout']).json()
            if not res['success']:
                raise Exception('调用标签库数据清洗接口失败，错误信息为:{}'.format(res['error']))
            return res['data']
        except Exception as error:
            raise error
