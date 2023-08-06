#!/usr/bin/python3
# -*- coding:utf-8 -*-
import re
from collections import OrderedDict
from smart_tag_tools.LinqTool import linq
from smart_tag_tools.AuxiliaryManager import MyTreeClass
from smart_tag_tools.TimeCodeConvertHelper import TimeCodeConvertHelper


class MetadataConverter:
    """
    元数据结构字段调整
    """

    @staticmethod
    def update_field_name(val, **kwargs):
        for x, y in kwargs.items():
            if x in val:
                val[y] = val.pop(x)

    @staticmethod
    def delete_field(val, *args):
        for x in args:
            val.pop(x, '404')

    @staticmethod
    def add_or_update_field(val, **kwargs):
        for x, y in kwargs.items():
            val[x] = y

    @classmethod
    def convert(cls, result, **kwargs):
        """
        元数据字段调整
        :param result: 元数据结构
        :param kwargs: 自定义字典
        :return:
        """
        frame_rate = kwargs.get('frame_rate')

        for meta in result['metadatas']:

            # model_sobey_smart_story
            if 'story' in meta['type']:
                for dic in meta['metadata']:
                    cls.update_field_name(dic, relatedperson='relatedpeople')
                    cls.delete_field(dic, 'subtitlevoicepeople', 'smartface')
                    cls.add_or_update_field(dic, framerate=frame_rate)

            # model_sobey_smart_scene
            elif 'scene' in meta['type']:
                for dic in meta['metadata']:
                    cls.update_field_name(dic, scenename='title', sceneplace='eventplace')
                    cls.delete_field(dic, 'keyframelist', 'smartface', 'shot_container')
                    cls.add_or_update_field(dic, framerate=frame_rate)

            # model_sobey_smart_shot
            elif 'shot' in meta['type']:
                for dic in meta['metadata']:
                    cls.update_field_name(dic, people='relatedpeople', is_actual='actual')
                    cls.delete_field(dic, 'smartface', 'visual_person')
                    cls.add_or_update_field(dic, framerate=frame_rate)

            # model_sobey_smart_face_
            elif 'face' in meta['type']:
                for dic in meta['metadata']:
                    cls.update_field_name(dic, keyFrameUrl='keyframepath')
                    cls.delete_field(dic, 'groups', 'type')
                    cls.add_or_update_field(dic, framerate=frame_rate)
                    for d in dic['segment']:
                        cls.update_field_name(d, **{'keyFrame': 'keyframeno', 'in': 'inpoint', 'out': 'outpoint'})
                        cls.add_or_update_field(d, keyframeno=TimeCodeConvertHelper().L100Ns2Frame(
                            d['keyframeno'], frame_rate))

            # model_sobey_smart_subtitles_
            elif 'subtitles' in meta['type']:
                for dic in meta['metadata']:
                    cls.delete_field(dic, 'keyFrame')
                    cls.update_field_name(dic, **{'in': 'inpoint', 'out': 'outpoint'})
                    cls.add_or_update_field(dic, framerate=frame_rate)

            # model_sobey_smart_voice_
            elif 'voice' in meta['type']:
                for dic in meta['metadata']:
                    cls.update_field_name(dic, **{'in': 'inpoint', 'out': 'outpoint'})
                    cls.delete_field(dic, 'word', 'index')
                    cls.add_or_update_field(dic, framerate=frame_rate)

            # model_sobey_smart_entity
            elif 'entity' in meta['type']:
                for dic in meta['metadata']:
                    cls.add_or_update_field(dic, framerate=frame_rate)


class ComConverter:
    @staticmethod
    def combine_to_heavy(items):
        """
        包含关系去重
        字幕去重/日期去重/地区名词去重/地区去重/头衔去重 ['广东省','广东省广州市']=>['广东省广州市']
        """
        len_ = len(items)
        for i in range(0, len_):
            # 若为无效数据，直接开始下一次循环
            if items[i] == '###':
                continue
            # 为保证序列的顺序，若两个值相等，更新后面的数据
            for j in range(i + 1, len_):
                if items[j] in items[i]:
                    items[j] = '###'
                elif items[i] in items[j]:
                    items[i] = '###'

        return list(filter(lambda x: True if x != '###' else False, items))

    @staticmethod
    def reporter_replace(items: list) -> list:
        """
        王斌(广东台记者/肇庆市人大常委会党组成员)--》王斌/记者、肇庆市人大常委会党组成员
        """

        def nj_replace_func(dic: dict) -> dict:
            k = '记者'
            if k in dic.get('name', ''):
                dic['name'] = dic['name'].replace('(敏感人物)', '###')
                name = dic['name'].split('(')[0].replace('###', '(敏感人物)')
                jobs = list(map(lambda x: k if k in x else x,
                                dic['name'].split('(')[1][:-1].split('/'))) if '(' in dic[
                    'name'] else []
                dic['name'] = '{}({})'.format(name, '/'.join(jobs))
            return dic

        return linq(items).select(lambda x: nj_replace_func(x)).distinct().tolist()

    @staticmethod
    def to_name_job(data: list) -> dict:
        """
        ['习近平(国家主席)','吴楠(CBA篮球运动员)']=>OrderedDict([(习近平, 国家主席),(吴楠, CBA篮球运动员)])
        """
        result = OrderedDict()
        if data:
            for tmp in data:
                job = list()
                tmp = tmp.replace('(敏感人物)', '###')
                if '(' in tmp:
                    job = re.search(r'.*(\(.*\)).*', tmp, re.S).group(1)[1:-1].split('/')
                result[tmp.split('(')[0].replace('###', '(敏感人物)')] = job
        return result

    @classmethod
    def duplicate_people(cls, x: list) -> list:
        """
        人脸去重（考虑头衔问题）
        ['习近平(国家主席)','习近平(中国共产党中央委员会总书记)']=>['习近平(国家主席/中国共产党中央委员会总书记)']
        """
        result = OrderedDict()
        if x:
            names = list()
            for tmp in x:
                tmp = tmp.replace('(敏感人物)', '###')
                name = tmp.split('(')[0].replace('###', '(敏感人物)')
                job = list()
                if '(' in tmp:
                    job = re.search(r'.*(\(.*\)).*', tmp, re.S).group(1)[1:-1].split('/')
                if name not in names:
                    names.append(name)
                    result[name] = job
                else:
                    result[name].extend(job)
        return ['{}({})'.format(k, '/'.join(cls.combine_to_heavy(v))) if v else k for k, v in result.items()]

    @classmethod
    def __intersection__(cls, x: list, y: list) -> list:
        """
        name取交集,相同人名的头衔合并
        """
        result = list()
        if x and y:
            x = cls.to_name_job(cls.duplicate_people(x))
            y = cls.to_name_job(cls.duplicate_people(y))
            for v in x.keys():
                if v in y.keys():
                    if x.get(v) or y.get(v):
                        job = '/'.join(cls.combine_to_heavy(x[v] + y[v]))
                        result.append('{name}({job})'.format(name=v, job=job))
                    else:
                        result.append('{name}'.format(name=v))
        return result

    @classmethod
    def __difference__(cls, x: list, y: list) -> list:
        """
        name取差集
        """
        result = list()
        if x:
            if not y:
                return x
            x = cls.to_name_job(cls.duplicate_people(x))
            y = cls.to_name_job(cls.duplicate_people(y))
            for v in x.keys():
                if v not in y.keys():
                    if x.get(v) or y.get(v):
                        result.append('{name}({job})'.format(name=v, job='/'.join(cls.combine_to_heavy(x[v]))))
                    else:
                        result.append('{name}'.format(name=v))
        return result

    @staticmethod
    def district__helper(data: list) -> list:
        """
        地区标签处理规则
        1.结合知识库查找地点对应地区，
        2.当地区标签个数=1时，直接返回为地区标签；
        3.当地区标签个数>1时，先按逻辑提取省，再提取省级下的市，再提取市级下的区，提取
        逻辑如下：
        取出现频次最高的省（/市/区）作为省级区域；
        特殊情况a.如果出现最高频次有多个省（/市/区）且频次不等于1则都保留
        情况b.如果出现所有省（/市/区）频次均为1则都舍弃
        情况c.如果只有1个省（/市/区）则保留。
        """
        if len(data) < 2:
            return data
        my_tree_class = MyTreeClass()
        district_tree = my_tree_class.tree()
        for row in data:
            my_tree_class.__node_add__(district_tree, row.split('/'))
        result = list()
        for tmp in data:
            filter_data = my_tree_class.__filter__(district_tree, tmp.split('/'))
            if filter_data not in result:
                result.append(filter_data)
        return result
