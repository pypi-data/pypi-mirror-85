# -*- coding: utf-8 -*-
from threading import Thread
import arrow
import regex as re
from smart_tag_tools.TimeTagHelper.TimeNormalizer import TimeNormalizer


class MyThread(Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        Thread.join(self)
        try:
            return self.result
        except:
            return None


def date_format(date_str):
    """
    日期格式化转换
    """
    _count = date_str.count('-')
    switch = {
        0: lambda x: x,
        1: lambda x: '{}年{}月'.format(*re.findall(r'(\d{4})-(\d{2})', x, re.S)[0]),
        2: lambda x: '{}年{}月{}日'.format(*re.findall(r'(\d{4})-(\d{2})-(\d{2})', x, re.S)[0])
    }
    return switch.get(_count, 0)(date_str)


def handle(time_list, base_time=arrow.now().format('YYYY-MM-DD')):
    """
    时间处理
    :param time_list: 时间字符串列表
    :param base_time: 基准时间
    :return:
    """
    tn = TimeNormalizer()
    thread_list = list()
    result_list = list()
    for time_string in time_list:
        t = MyThread(tn.parse, args=(time_string, base_time))
        t.start()
        thread_list.append(t)

    for thread in thread_list:
        result = thread.get_result().get("timestamp", "")
        result_list.append(date_format(result))
    return result_list

# print(handle('九月初六'.split(',')))
