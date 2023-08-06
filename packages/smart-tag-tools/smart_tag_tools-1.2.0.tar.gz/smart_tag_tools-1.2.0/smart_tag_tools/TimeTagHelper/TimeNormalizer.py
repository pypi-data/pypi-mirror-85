# -*- coding: utf-8 -*-
import pickle
import regex as re
import arrow
import json
import os
import threading

import datetime
from smart_tag_tools.TimeTagHelper.StringPreHandler import StringPreHandler
from smart_tag_tools.TimeTagHelper.TimePoint import TimePoint
from smart_tag_tools.TimeTagHelper.TimeUnit import TimeUnit
from smart_tag_tools.TimeTagHelper import glo
from smart_tag_tools.TimeTagHelper.CalendarTool import CalendarTool


# 时间表达式识别的主要工作类
class TimeNormalizer:
    def __init__(self, isPreferFuture=False):
        self.lock = threading.Lock()
        self.isPreferFuture = isPreferFuture
        self.pattern, self.holi_solar, self.holi_lunar = self.init()

    # 这里针对规范的标准输出
    def standard_match(self, date_str):
        reference = datetime.datetime.strptime(self.nowTime, '%Y-%m-%d')
        reference_year, reference_month, reference_day = reference.year, reference.month, reference.day

        day = re.findall(r'(\d+)日', date_str, re.S)
        if not day:
            day = re.findall(r'(\d+)号', date_str, re.S)
        month = re.findall(r'(\d+)月', date_str, re.S)
        year = re.findall(r'(\d{4})年', date_str, re.S)

        if year and month and day:
            return '{}年{}月{}日'.format(year[0], month[0], day[0])
        if month and day:
            return '{}年{}月{}日'.format(reference_year, month[0], day[0])
        if year and month:
            return '{}年{}月'.format(year[0], month[0])

        year = re.findall(r'^(\d{4})年$', date_str, re.S)
        if year:
            if int(year[0]) > 1990:
                return '{}年'.format(year[0])

        month = re.findall(r'^(\d+)月$', date_str, re.S)
        if month:
            if 1 <= int(month[0]) <= 12:
                return '{}年{}月'.format(reference_year, month[0])

        day = re.findall(r'^(\d+)日$', date_str, re.S)
        if not day:
            day = re.findall(r'^(\d+)号$', date_str, re.S)
        if day:
            if 1 <= int(day[0]) <= 31:
                return '{}年{}月{}日'.format(reference_year, reference_month, day[0])

        return date_str

    # 农历日期转换
    def lunar_convert(self, date_str):
        reference = datetime.datetime.strptime(self.nowTime, '%Y-%m-%d')

        # 农历日期判定
        lunar_flag = False
        lunar_date_mark_list = ['大年', '廿', '农历', '卅', "初一", "初二", "初三",
                                "初四", "初五", "初六", "初七", "初八", "初九", "初十"]
        for ld in lunar_date_mark_list:
            if ld in date_str:
                lunar_flag = True
                break

        # 转换中文数字
        date_str = self.chinese_num_to_arab(self.lunar_num_to_arab(date_str))

        # 农历日期转换
        if lunar_flag:
            ld = re.findall(r'(\d+)月(\d+)', date_str, re.S)
            if ld:
                return CalendarTool().__lunar_to_solar__(reference.year, *(int(_) for _ in ld[0]))
        return date_str

    @staticmethod
    def chinese2digits(u_chars_chinese):
        """
        把汉语句子中的汉字（大小写）数字转为阿拉伯数字，不能识别“百分之”
        :param u_chars_chinese:
        :return:
        """
        common_used_numerals_tmp = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8,
                                    '九': 9,
                                    '十': 10,
                                    u'〇': 0, u'壹': 1, u'贰': 2, u'叁': 3, u'肆': 4, u'伍': 5, u'陆': 6, u'柒': 7, u'捌': 8,
                                    u'玖': 9,
                                    '拾': 10,
                                    '百': 100, '千': 1000, u'貮': 2, u'俩': 2, '佰': 100, '仟': 1000, '萬': 10000, '万': 10000,
                                    '亿': 100000000,
                                    '億': 100000000, '兆': 1000000000000}
        total = 0
        r = 1  # 表示单位：个十百千...
        common_used_numerals = {}
        for key in common_used_numerals_tmp:
            common_used_numerals[key] = common_used_numerals_tmp[key]
        for i in range(len(u_chars_chinese) - 1, -1, -1):
            val = common_used_numerals.get(u_chars_chinese[i])
            if val >= 10 and i == 0:  # 应对 十三 十四 十*之类
                if val > r:
                    r = val
                    total = total + val
                else:
                    r = r * val
                    # total =total + r * x
            elif val >= 10:
                if val > r:
                    r = val
                else:
                    r = r * val
            else:
                total = total + r * val
        return total

    def chinese_num_to_arab(self, ori_str):
        num_str_start_symbol = ['一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十',
                                '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖', '拾', '貮', '俩', ]
        more_num_str_symbol = ['零', '一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '亿',
                               '〇', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖', '拾', '貮', '俩', '佰', '仟', '萬', '億', '兆']
        special_used_numerals_tmp = {
            '十': 10,
            '拾': 10,
            '百': 100, '千': 1000, '佰': 100, '仟': 1000, '萬': 10000, '万': 10000,
            '亿': 100000000,
            '億': 100000000, '兆': 1000000000000}
        cn_num = {
            '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '零': 0,
            '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9, '貮': 2, '两': 2,
            '十': 10, '拾': 10
        }
        len_str = len(ori_str)
        a_pro_str = ''
        if len_str == 0:
            return a_pro_str
        su_t_flag = True
        if len_str > 1:
            for su_t in special_used_numerals_tmp:
                if su_t in ori_str:
                    su_t_flag = False
                    break
        if su_t_flag:
            return ''.join(list(map(lambda x: str(cn_num[x]) if x in cn_num.keys() else x, list(ori_str))))
        has_num_start = False
        number_str = ''
        for idx in range(len_str):
            if ori_str[idx] in num_str_start_symbol:
                if not has_num_start:
                    has_num_start = True
                number_str += ori_str[idx]
            else:
                if has_num_start:
                    if ori_str[idx] in more_num_str_symbol:
                        number_str += ori_str[idx]
                        continue
                    else:
                        num_result = str(self.chinese2digits(number_str))
                        number_str = ''
                        has_num_start = False
                        a_pro_str += num_result
                a_pro_str += ori_str[idx]
                pass
        if len(number_str) > 0:
            result_num = self.chinese2digits(number_str)
            a_pro_str += str(result_num)
        return a_pro_str

    @staticmethod
    def lunar_num_to_arab(date_str):
        lunar_num = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
                     "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                     "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十", "卅一"]
        lunar_month_num = {'正月': '1月', '腊月': '12月', '冬月': '11月', '大年': '1月'}
        for lmn in lunar_month_num:
            if lmn in date_str:
                date_str = date_str.replace(lmn, str(lunar_month_num.get(lmn)))
        for ln in lunar_num:
            if ln in date_str:
                date_str = date_str.replace(ln, str(lunar_num.index(ln) + 1))
        return date_str

    # 这里对一些不规范的表达做转换
    def _filter(self, input_query):
        # 特殊情况的处理
        input_query = StringPreHandler.specialTranslator(input_query)
        # 这里对于下个周末这种做转化 把个给移除掉
        input_query = StringPreHandler.numberTranslator(input_query)

        rule = "[0-9]月[0-9]"
        pattern = re.compile(rule)
        match = pattern.search(input_query)
        if match != None:
            glo.set_value("is_Holiday", True)
            index = input_query.find('月')
            rule = "日|号"
            pattern = re.compile(rule)
            match = pattern.search(input_query[index:])
            if match == None:
                rule = "[0-9]月[0-9]+"
                pattern = re.compile(rule)
                match = pattern.search(input_query)
                if match != None:
                    end = match.span()[1]
                    input_query = input_query[:end] + '号' + input_query[end:]

        rule = "月"
        pattern = re.compile(rule)
        match = pattern.search(input_query)
        if match == None:
            input_query = input_query.replace('个', '')

        input_query = input_query.replace('中旬', '15号')
        input_query = input_query.replace('傍晚', '午后')
        input_query = input_query.replace('大年', '')
        input_query = input_query.replace('五一', '劳动节')
        input_query = input_query.replace('十一', '国庆节')
        input_query = input_query.replace('白天', '早上')
        input_query = input_query.replace('：', ':')
        return input_query

    def init(self):
        fpath = os.path.dirname(__file__) + '/resource/reg.pkl'
        try:
            with open(fpath, 'rb') as f:
                pattern = pickle.load(f)
        except:
            with open(os.path.dirname(__file__) + '/resource/regex.txt', 'r', encoding="utf-8") as f:
                content = f.read().replace("\n", "")
            p = re.compile(content)
            with open(fpath, 'wb') as f:
                pickle.dump(p, f)
            with open(fpath, 'rb') as f:
                pattern = pickle.load(f)
        with open(os.path.dirname(__file__) + '/resource/holi_solar.json', 'r', encoding='utf-8') as f:
            holi_solar = json.load(f)
        with open(os.path.dirname(__file__) + '/resource/holi_lunar.json', 'r', encoding='utf-8') as f:
            holi_lunar = json.load(f)
        return pattern, holi_solar, holi_lunar

    def parse(self, target, timeBase):
        """
        TimeNormalizer的构造方法，timeBase取默认的系统当前时间
        :param timeBase: 基准时间点
        :param target: 待分析字符串
        :return: 时间单元数组
        """
        try:
            self.lock.acquire()
            self.timeBase = arrow.get(timeBase).format('YYYY-M-D-H-m-s')
            self.nowTime = timeBase
            self.oldTimeBase = self.timeBase

            # 针对一些自己可以先转换的日期，先处理
            target = self.lunar_convert(self.standard_match(target))

            dic = {}
            glo.set_value("is_Holiday", False)
            self.isTimeSpan = False
            self.invalidSpan = False
            self.timeSpan = ''
            self.target = self._filter(target)
            self.__preHandling()
            self.timeToken = self.__timeEx()
            res = self.timeToken

            if self.isTimeSpan:
                if self.invalidSpan:
                    dic['error'] = 'no time pattern could be extracted.'
                else:
                    result = {}
                    dic['type'] = 'timedelta'
                    dic['timedelta'] = self.timeSpan
                    # print(dic['timedelta'])
                    index = dic['timedelta'].find('days')

                    days = int(dic['timedelta'][:index - 1])
                    result['year'] = int(days / 365)
                    result['month'] = int(days / 30.417 - result['year'] * 12)
                    result['day'] = int(days - result['year'] * 365 - result['month'] * 30.417)
                    index = dic['timedelta'].find(',')
                    time = dic['timedelta'][index + 1:]
                    time = time.split(':')
                    result['hour'] = int(time[0])
                    result['minute'] = int(time[1])
                    result['second'] = int(time[2])
                    dic['timedelta'] = result
            else:
                if len(res) == 0:
                    dic['error'] = 'no time pattern could be extracted.'
                elif len(res) == 1:
                    dic['type'] = 'timestamp'
                    if glo.get_value("is_Holiday"):
                        dic['timestamp'] = res[0].time.format("YYYY-MM-DD HH:mm:ss").replace(" 00:00:00", "").replace(
                            ":00:00", "点")
                    else:
                        dic['timestamp'] = res[0].time.format("YYYY-MM-DD HH:mm:ss").replace("-01-01 00:00:00",
                                                                                             "年").replace(
                            "-01 00:00:00",
                            "").replace(
                            " 00:00:00", "").replace(":00:00", "点")
                else:
                    dic['type'] = 'timespan'
                    dic['timespan'] = [res[0].time.format("YYYY-MM-DD HH:mm:ss"),
                                       res[1].time.format("YYYY-MM-DD HH:mm:ss")]
        except Exception as e:
            print('口语化时间解析报错', e)
            dic = {}
        finally:
            self.lock.release()
        return dic

    def __preHandling(self):
        """
        待匹配字符串的清理空白符和语气助词以及大写数字转化的预处理
        :return:
        """
        self.target = StringPreHandler.delKeyword(self.target, "\\s+")  # 清理空白符
        self.target = StringPreHandler.delKeyword(self.target, "[的]+")  # 清理语气助词
        self.target = StringPreHandler.numberTranslator(self.target)  # 大写数字转化

    def __timeEx(self):
        """

        :param target: 输入文本字符串
        :param timeBase: 输入基准时间
        :return: TimeUnit[]时间表达式类型数组
        """
        startline = -1
        endline = -1
        rpointer = 0
        temp = []

        match = self.pattern.finditer(self.target)
        for m in match:
            startline = m.start()
            if startline == endline:
                rpointer -= 1
                temp[rpointer] = temp[rpointer] + m.group()
            else:
                temp.append(m.group())
            endline = m.end()
            rpointer += 1
        res = []
        # 时间上下文： 前一个识别出来的时间会是下一个时间的上下文，用于处理：周六3点到5点这样的多个时间的识别，第二个5点应识别到是周六的。
        contextTp = TimePoint()
        # print(self.timeBase)
        # print('temp', temp)
        for i in range(0, rpointer):
            # 这里是一个类嵌套了一个类
            res.append(TimeUnit(temp[i], self, contextTp))
            # res[i].tp.tunit[3] = -1
            contextTp = res[i].tp
            # print(self.nowTime.year)
            # print(contextTp.tunit)
        res = self.__filterTimeUnit(res)

        return res

    def __filterTimeUnit(self, tu_arr):
        """
        过滤timeUnit中无用的识别词。无用识别词识别出的时间是1970.01.01 00:00:00(fastTime=0)
        :param tu_arr:
        :return:
        """
        if (tu_arr is None) or (len(tu_arr) < 1):
            return tu_arr
        res = []
        for tu in tu_arr:
            if tu.time.timestamp != 0:
                res.append(tu)
        return res
