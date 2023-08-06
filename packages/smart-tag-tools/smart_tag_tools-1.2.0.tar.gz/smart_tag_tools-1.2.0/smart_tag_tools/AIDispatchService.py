#!/usr/bin/python3
# -*- coding:utf-8 -*-
import requests


class AIDispatchService:
    """
        {
            "accesstoken": "classification",
            "type": "nlp/classification",
            "version": "1.0",
            "params": {},
            "files": [
                {
                    "type": "text",
                    "id": "uuid_1",
                    "txt": "海军陆战队训练"
                },
                {
                    "type": "text",
                    "id": "uuid_2",
                    "txt": "来自全国各地的医生团体"
                }
            ],
            "callback": ["http://172.16.139.24:2000/sobey/AI/Result"],
            "userdata": {}
        }
    """
    # noinspection PyUnresolvedReferences
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    # noinspection PyDefaultArgument
    def add_task(self, task_type, access_token, version, files, params={}, user_data={},
                 callback=["http://172.16.139.24:2000/sobey/AI/Result"]):
        data = {
            "accesstoken": access_token,
            "type": task_type,
            "version": version,
            "params": params,
            "files": files,
            "callback": callback,
            "userdata": user_data
        }
        try:
            res = self.s.post(self.kwargs['url'], json=data, timeout=self.kwargs.get('timeout', 5)).json()
            if res['code'] == 0:
                return res['data']
            else:
                raise Exception('添加任务失败:{}'.format(res.get('msg')))
        except Exception as error:
            raise error

    def get_task(self, callback_url: str):
        try:
            res = self.s.get(callback_url, timeout=self.kwargs.get('timeout', 5)).json()
            if res.get('code') == 0:
                if res['data']['taskStatus'] == 0:
                    # 任务已完成，判断每个file是不是执行成功。失败的话，直接抛异常
                    for file_task in res['data']['results']:
                        if file_task['statusCode'] != 0:
                            raise Exception('单个file执行失败:{}'.format(file_task['statusInfo']))
                    return res['data']['results']
            else:
                raise Exception('查询任务失败:{}'.format(res.get("message")))
        except Exception as error:
            raise error
