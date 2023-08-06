import re
import json
import requests
import asyncio
import collections
from datetime import datetime
from smart_tag_tools.TimeTagHelper.TimeHandle import handle
from smart_tag_tools.LinqTool import linq
from pypinyin import lazy_pinyin, Style


class SmartTagsConvertHelper:
    """
    智能标签处理
    """

    def __init__(self, kwargs):
        self.kwargs = kwargs
        # 知识库服务健康检查状态
        self.kb_interface_status = self.__kb_heartbeat_detection__()
        # 实体转换关系记录
        self.entity_convert_map = {'NAME': {}, 'LOC': {}, 'ORG': {}, 'TIME': {}, 'JOB': {}}
        # 实体类型与操作记录类型映射
        self.entity_type_map = {'people': 'NAME', 'loc': 'LOC', 'org': 'ORG', 'time': 'TIME'}

    def __kb_heartbeat_detection__(self):
        """
        知识库心跳检测
        :return:
        """
        try:
            res = requests.get(url='http://{}:{}{}/health-check'.format(
                self.kwargs['RelyOn']['KbService']['ip'],
                self.kwargs['RelyOn']['KbService']['port'],
                self.kwargs['RelyOn']['KbService']['UrlPrefix']),
                timeout=self.kwargs['RelyOn']['KbService']['timeout'])
            if res.status_code == 200:
                return True
            else:
                return False
        except:
            return False

    def GetDateFromText(self, date_str):
        """
        解析字符串中包含的日期数据，通常用于从标题中提取首播日期
        第一现场191025//2019-09-28 吉林新闻联播
        :param date_str: 字符串
        :return:
        """
        if not isinstance(date_str, str):
            raise TypeError('参数类型错误')
        if date_str:
            for reg in self.kwargs['DateReg']:
                date_list = re.findall(reg, date_str, re.S)
                if date_list:
                    year, month, day = date_list[0]
                    if len(year) == 2:
                        year = str(datetime.now().year)[:2] + str(year)
                    try:
                        result = datetime(year=int(year), month=int(month), day=int(day)).strftime('%Y-%m-%d')
                    except:
                        result = ''
                    return result

    def GetNewsDate(self, date_list, reference_date, is_callback=False):
        """
        根据NLP从语音、文稿、字幕中提取出的时间词，结合首播日期等信息，
        获得符合标准的日期标签（YYYYMM或YYYYMMDD)
        2020年1月7日 相关日期：从正面筛选，只需要显示 年月日（号），月日（号），日（号）
        """
        if not isinstance(date_list, list):
            raise TypeError('参数类型错误')
        items = handle(date_list, reference_date)
        result = dict(zip(date_list, items))
        if is_callback:
            self.CallFun(result, 'TIME')
        return list(filter(lambda x: x, result.values()))

    @staticmethod
    def __abs_(value):
        now = datetime.now()
        if value <= now:
            value = 1 / (value - now).total_seconds()
        else:
            value = (value - now).total_seconds()
        return value

    def GetTimeByOrder(self, by_sort_list, order):
        """
        时间排序
        1. 由近到远，先过去，后未来排列；
        2. 按时间从小到大排列；
        3. 按时间从大到小排列。
        :param by_sort_list:待排序的时间列表
        :param order:排序方式
        :return:排序后的时间列表
        """
        if not isinstance(order, int):
            raise TypeError('传入的类型错误,整型数据被需要')
        sorted_list = list()
        if by_sort_list:
            switch = {
                1: lambda x: sorted(x, key=self.__abs_, reverse=False),
                2: lambda x: sorted(x, reverse=False),
                3: lambda x: sorted(x, reverse=True)
            }
            sorted_list = switch.get(order, 1)(by_sort_list)
        return sorted_list

    def GetDataByPriority(self, kwargs):
        """
        按优先级获取
        对于可存在于多个来源的数据，可按预设优先级获取数据，找到有效数据则返回。
        :param kwargs:
        :return:
        """
        if not isinstance(kwargs, dict):
            raise TypeError('参数类型错误,字典被需要')
        for k in sorted(kwargs):
            if kwargs[k]:
                return kwargs[k]

    def GetUnion(self, *args):
        """
        多个标签集合取并集后返回
        :param args:
        :return:
        """
        union_data = set()
        for data in args:
            union_data.update(data)
        return union_data

    def GetIntersection(self, *args):
        """
        多个标签集合取交集后返回
        :param args:
        :return:
        """
        intersection_data = args[0]
        for data in args:
            intersection_data.intersection_update(data)
        return intersection_data

    def __dict_to_obj__(self, dic):
        """
        字典转为json对象，实现类.属性的操作
        :param dic:
        :return:
        """
        if not isinstance(dic, dict):
            raise TypeError('传入的数据类型错误,字典被需要')

        class JSONObject:
            def __init__(self, d):
                self.__dict__ = d

        return json.loads(json.dumps(dic, ensure_ascii=False), object_hook=JSONObject, encoding='utf-8')

    def __kb_interface_call(self, route, data):
        """
        知识库接口调用
        :param route: 相对路径
        :param data: json数据
        :return:
        """
        try:
            res = requests.post(url='http://{}:{}{}{}'.format(
                self.kwargs['RelyOn']['KbService']['ip'],
                self.kwargs['RelyOn']['KbService']['port'],
                self.kwargs['RelyOn']['KbService']['UrlPrefix'], route),
                json=data,
                timeout=self.kwargs['RelyOn']['KbService']['timeout']).json()
            if res['success']:
                return res['data']
        except:
            return None

    def GetColumnFromText(self, text, channel=None):
        """
        栏目提取
        解析字符串中包含的栏目数据，通常用于从标题中提取栏目
        :param text:文本字符串
        :param channel:频道名称
        :return:
        """
        data = {
            'text': text,
            'channel': channel
        }
        if not self.kb_interface_status:
            return None
        res = self.__kb_interface_call('/v1/label/column-names', data)
        if res:
            result = res['result']
            if result:
                return result[0]['column']
        else:
            return None

    def GetNewsLocation(self, address, is_callback=False):
        """
        地点筛选
        根据NLP从语音、文稿、字幕中提取出的地点词, 经过清洗筛选，过滤掉过大，过小的地点词，返回有意义的地点词（具体算法待定）。 过滤掉类似 “四楼咖啡厅"，"客厅"这类词语
        """
        if not isinstance(address, list):
            raise TypeError('参数类型错误')
        result = dict()
        if not self.kb_interface_status:
            return address
        res = self.__kb_interface_call('/v1/label/filtered-locations', address)
        if res:
            for item in res:
                result[item['originvalue']] = item['result'][0].get('name', '') if item['result'] else ''
            if is_callback:
                self.CallFun(result, 'LOC')
            return list(filter(lambda x: x, result.values()))
        return address

    def GetRelatedDivision(self, address):
        """
        获得相关行政区
        根据具体地点返回所属行政区划（完整路径）
        :param address: 地点
        :return:
        """
        if not isinstance(address, list):
            raise TypeError('参数类型错误')
        result = []
        if not self.kb_interface_status:
            return result
        res = self.__kb_interface_call('/v1/label/related-divisions', address)
        if res:
            result = linq(res).where(lambda x: x.get('result')).select(lambda x: x['result']).tolist()
        return result

    def GetFullOrgName(self, agency: list, is_callback=False):
        """
        机构名补全
        对于AI提取的不完整的标签数据，补充限定词。限定词依据电视台所属行政区划数据获得。
        补充地区限定词，当机构名称首字为“省”时，自动补齐“XX省”，如“省人民政府”补充为“XX省人民政府；
        """
        result = dict([(x, x) for x in agency])
        if agency:
            type_dict = collections.OrderedDict((key, value) for key, value in self.kwargs['TvArea'].items() if value)
            for index, item in enumerate(agency):
                if list(filter(lambda x: True if item.startswith(x) or item.startswith('州') else False,
                               type_dict.keys())):
                    if '自治州' not in item and '州' in item:
                        item = item.replace('州', '自治州')
                    for k, v in type_dict.items():
                        if k in item:
                            if k == '区' and '自治区' in item:
                                continue
                            result[agency[index]] = type_dict.get(k).replace(k, '') + item
            if is_callback:
                self.CallFun(result, 'ORG')
        return list(filter(lambda x: x, result.values()))

    def GetNormalizedOrgName(self, org, is_callback=False):
        """
        机构名归一化
        按照机构库名字进行归一化处理，将简称转换为全称
        """
        if not isinstance(org, list):
            raise TypeError('参数类型错误')
        result = dict()
        if not self.kb_interface_status:
            return org
        res = self.__kb_interface_call('/v1/label/normalized-names?type=org', org)
        if res:
            for item in res:
                result[item['origin']] = item.get('result', '')
            if is_callback:
                self.CallFun(result, 'ORG')
            return list(filter(lambda x: x, result.values()))
        return org

    def GetAddressByOrder(self, address, order=1):
        """
        地点排序
        将无序的地点标签数组按指定方式排列，可选以下两种方式：
        1. 按地点从大到小，由本地到外地排列；
        2. 按地点音序排列
        排序方式 level|pronunciation 大小，音序
        :param address: 排序列表
        :param order: 类型
        :return:
        """
        __map__ = {1: 'level', 2: 'pronunciation'}
        if not isinstance(address, list):
            raise TypeError('参数类型错误')
        if not self.kb_interface_status:
            return address
        data = {
            "originvalue": address,
            "pattern": __map__.get(int(order), 1)
        }
        res = self.__kb_interface_call('/v1/label/sorted-locationnames', data)
        if res:
            return res['result']
        return address

    def GetOrgTagsByOrder(self, org, order=1):
        """
        机构标签排序
        将机构标签按由大到小，由本地到外地顺序排列
        :param org: 排序列表
        :param order: 类型
        :return:
        """
        __map__ = {1: 'level'}
        if not isinstance(org, list):
            raise TypeError('参数类型错误')
        if not self.kb_interface_status:
            return org
        data = {
            'originvalue': org,
            'pattern': __map__.get(int(order))
        }
        res = self.__kb_interface_call('/v1/label/sorted-orgnames', data)
        if res:
            return res['result']
        return org

    def GetAlternative(self, replace):
        """
        推荐替换词
        主要用在人工审校环节，按以下逻辑处理：
        1. 标准叙词库中的词语，则直接使用，不推荐修改；
        2. 标准叙词表中不存在的词语，但是在别名字段中存在的词语，推荐修改为实体本名；
        3. 标准叙词表的本名、别名均不存在的，通过近似算法找最相近的5个进行推荐。
        :param replace:被替换词列表
        :return:替换后的列表
        """
        if not isinstance(replace, list):
            raise TypeError('参数类型错误')
        result = dict()
        if not self.kb_interface_status:
            return replace
        res = self.__kb_interface_call('/v1/label/alternative-words', replace)
        if res:
            for item in res:
                result[item['originvalue']] = item['result'][0].get('name', '') if item['result'] else ''
            return result
        return replace

    @staticmethod
    def NumberOfStatistical(items):
        """
        统计词条出现的次数
        :param items:
        :return:
        """
        if not isinstance(items, list):
            raise TypeError('参数类型错误')
        # noinspection PyArgumentList
        return collections.Counter(items)

    def JudgeIsColumn(self, items):
        """
        判断是不是栏目
        :param items:
        :return:
        """
        if not isinstance(items, list):
            raise TypeError('参数类型错误')
        result = list()
        if not self.kb_interface_status:
            return result
        res = self.__kb_interface_call('/v1/label/judged-column-names', items)
        if res:
            result = [tmp['originvalue'] for tmp in filter(lambda x: True if x.get('result') else False, res)]
        return result

    def JudgeIsLocName(self, items):
        """
        判断是不是地区名词
        :param items:
        :return:
        """
        if not isinstance(items, list):
            raise TypeError('参数类型错误')
        result = list()
        if not self.kb_interface_status:
            return result
        res = self.__kb_interface_call('/v1/label/judged-loc-names', items)
        if res:
            result = [tmp['originvalue'] for tmp in filter(lambda x: True if x.get('result') else False, res)]
        return result

    def GetSpecificIdentityPeople(self, people):
        """
        获取特定身份的人
        用于设别主持人，记者或其他人物身份
        :param people:
        :return:
        """
        if not isinstance(people, list):
            raise TypeError('参数类型错误')
        result = list()
        if not self.kb_interface_status:
            return result
        res = self.__kb_interface_call('/v1/label/reporters-comperes', people)
        if res:
            return res
        return result

    def NamesOfErrorCorrection(self, people, is_callback=False):
        """
        人名纠错处理（目前只考虑带头衔的人名）
        """
        if not isinstance(people, list):
            raise TypeError('参数类型错误')
        if not self.kb_interface_status:
            return people
        res = self.__kb_interface_call('/v1/label/homophones', people)
        if res:
            if is_callback:
                self.CallFun(dict(linq(res).select(lambda x: (x.get('origin', ''), x.get('result'))).tolist()), 'NAME')
            return linq(res).select(
                lambda x: {'id': x.get('id'), 'name': x.get('result'), 'confidence': x.get('confidence')}).tolist()
        return people

    def GetNormalizedHumanName(self, people, is_callback=False):
        """
        相关人名归一化
        按照人物库名字进行归一化处理，将常用的多种称谓进行统一，对音译人名进行统一。
        """
        if not isinstance(people, list):
            raise TypeError('参数类型错误')
        if not self.kb_interface_status:
            return people
        res = self.__kb_interface_call('/v1/label/normalized-names?type=people', people)
        if res:
            if is_callback:
                self.CallFun(dict(linq(res).select(lambda x: (x.get('origin', ''), x.get('result'))).tolist()), 'NAME')
            return linq(res).select(lambda x: {'id': x.get('id'), 'name': x.get('result')}).tolist()
        return people

    def GetPeopleTagsByOrder(self, people, order):
        """
        人名标签排序
        将无序的人名标签数组按指定方式排列，可选以下3种方式：
        1. 按照人物级别排序（元首-中央政治局常委【有序】-中央政治局委员-中央委员会委员-前任总书记-曾担任政治局常委的党和国家领导人-省委书记-省长-省委常委【有序】-省厅局级领导-市委书记-市长-市委常委【有序】-市委办局级领导-区县书记-区县长。如同等级别则先主后宾排列。
        2. 按姓名音序排列
        3. 按姓名笔画排列
        排序方式 level | pronunciation | stroke 级别，音序，笔画数
        :param people: 排序列表
        :param order 类型
        :return:
        """
        __map__ = {1: 'level', 2: 'pronunciation', 3: 'stroke'}
        if not isinstance(people, list):
            raise TypeError('参数类型错误')
        if not self.kb_interface_status:
            return people
        data = {
            'originvalue': people,
            'pattern': __map__.get(int(order), 1)
        }
        res = self.__kb_interface_call('/v1/label/sorted-humannames', data)
        if res:
            return res['result']
        return people

    def JudgeIsSensitive(self, items):
        """
        判断是不是敏感人物
        :param items:
        :return:
        """
        if not isinstance(items, list):
            raise TypeError('参数类型错误')
        if not self.kb_interface_status:
            return items
        result = list()
        res = self.__kb_interface_call('/v1/label/judged-sensitive-peoples', items)
        if res:
            for tmp in res:
                if tmp.get('result'):
                    tmp['name'] = '(敏感人物)' + tmp['name']
                result.append(tmp)
            return result
        return items

    @staticmethod
    def edit(str1, str2):
        """
        算两个字符串的最小编辑距离
        """
        matrix = [[i + j for j in range(len(str2) + 1)]
                  for i in range(len(str1) + 1)]

        for i in range(1, len(str1) + 1):
            for j in range(1, len(str2) + 1):
                if str1[i - 1] == str2[j - 1]:
                    d = 0
                else:
                    d = 1
                matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1,
                                   matrix[i - 1][j - 1] + d)

        return round(1 - (matrix[len(str1)][len(str2)] / len(str2)), 2)

    def PinyinIsSimilarity(self, x, y, similarity=0.6):
        """
        判断两个词拼音是不是相似
        """
        pinyin_x = ''.join(lazy_pinyin(x.replace('(敏感人物)', '').split('(')[0], style=Style.NORMAL))
        pinyin_y = ''.join(lazy_pinyin(y.replace('(敏感人物)', '').split('(')[0], style=Style.NORMAL))
        return self.edit(pinyin_x, pinyin_y) > similarity

    async def single_tag_correct(self, word, typ, tag_map):
        data = linq(self.kwargs.get('TagCorrectRecord', {}).get(typ, [])).where(
            lambda x: x['before_correction'] == word).order_by(
            lambda x: x['operate_times'], default=True).first()
        if data:
            tag_map[word] = data['after_correction']

    def BatchTagCorrect(self, entity_string, typ, is_callback=False):
        """
        批量标签修正
        """
        if not entity_string:
            return ''
        tag_map = {k: k for k in entity_string.split(',')}
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        loop = asyncio.get_event_loop()
        tasks = [self.single_tag_correct(tag, typ, tag_map) for tag in tag_map.keys()]
        loop.run_until_complete(asyncio.wait(tasks))
        if is_callback:
            self.CallFun(tag_map, self.entity_type_map[typ])
        return ','.join(tag_map.values())

    @staticmethod
    def chunk_merge(chunk, typ):
        result = list()
        for name, array in linq(chunk).group_by('name').items():
            if len(array) > 1:
                time_line = []
                dic = {'name': name}
                if typ == 'NAME':
                    dic['ids'] = ','.join(linq([arr['ids'] for arr in array]).where(lambda x: x).distinct().tolist())
                for arr in array:
                    time_line.extend(arr['timeline'])
                dic['timeline'] = linq(time_line).order_by(lambda x: (x['source'], x['inpoint'])).distinct().tolist()
                result.append(dic)
            else:
                result.extend(array)
        return result

    def EntityBackFlow(self, entity):
        """
        扫描实体元数据，回流更新记录
        这里需要对相同实体合并时间线
        """
        for group in entity:
            kind = group['type']
            if kind in self.entity_convert_map:
                for dic in group['entitydata']:
                    name = self.entity_convert_map[kind].get(dic['name'])
                    if name:
                        dic['name'] = name
                group['entitydata'] = self.chunk_merge(group['entitydata'], group['type'])

    @staticmethod
    def title_pipeline(x):
        return x.replace('(敏感人物)', '').split('(')[0]

    def CallFun(self, relation, kind):
        """
        回调函数，用于记录实体转换关系
        """
        # 人名实体更新，需要忽略头衔
        if kind == 'NAME':
            relation = dict(linq(relation.items()).select(
                lambda x: (self.title_pipeline(x[0]), self.title_pipeline(x[1]))).tolist())
        # 将每一步获取的转换关系映射更新到实体关系记录表
        for k, v in relation.items():
            key_array = linq(self.entity_convert_map[kind].items()).where(lambda x: x[1] == k).select(
                lambda x: x[0]).tolist()
            if key_array:
                self.entity_convert_map[kind].update({key: v for key in key_array})
            else:
                self.entity_convert_map[kind][k] = v
