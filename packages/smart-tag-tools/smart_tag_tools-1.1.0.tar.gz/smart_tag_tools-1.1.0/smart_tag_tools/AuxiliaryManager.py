#!/usr/bin/python3
# -*- coding:utf-8 -*-

from collections import defaultdict


class MyDefaultDict(defaultdict):
    """
    利用defaultdict实现树结构，考虑树节点的计数问题
    """

    def __init__(self, default_factory=None, num=0):
        super().__init__(default_factory)
        self.num = num


class MyTreeClass:
    """
    树结构的实现和具体方法
    """

    def tree(self):
        """
        树结构的初始化
        """
        return MyDefaultDict(self.tree)

    @staticmethod
    def __node_add__(t, keys):
        """
        节点添加
        """
        for key in keys:
            t = t[key]
            t.num += 1

    @staticmethod
    def __filter__(t, items):
        """
        过滤节点
        """
        for index, key in enumerate(items):
            t = t[key]
            if t.num <= 1:
                items[index] = 'oo'
        return '/'.join(filter(lambda x: True if x != 'oo' else False, items))


class Metaclass(type):

    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__ConvertFunc__'] = []
        attrs['__ConvertFuncLabel__'] = []
        for k, v in attrs.items():
            if 'convert' in k:
                attrs['__ConvertFunc__'].append(k)
                attrs['__ConvertFuncLabel__'].append(k[2:].replace('_convert__', ''))
                count += 1
        attrs['__ConvertFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Decorator:

    @staticmethod
    def exc(func):

        def wrapper(*args):
            try:
                return func(*args)
            except:
                return None

        return wrapper
