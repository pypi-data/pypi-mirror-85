from collections import Iterable


class linq(object):
    def __init__(self, iterable):
        if isinstance(iterable, list):
            iterable = iter(iterable)
        if not isinstance(iterable, Iterable):
            raise TypeError('参数类型错误')
        self.__end = False
        self.__iterable = iterable

    def __get_iterable(self):
        if self.__end:
            raise StopIteration('迭代器不可重复使用')

        self.__end = True
        return self.__iterable

    def all(self, predicate):
        return all(map(predicate, self.__get_iterable()))

    def any(self, predicate=None):
        return any(map(predicate, self.__get_iterable()))

    def where(self, predicate):
        return linq(filter(predicate, self.__get_iterable()))

    def max(self):
        return max(self.__get_iterable())

    def min(self):
        return min(self.__get_iterable())

    def average(self):
        count = 0
        total = 0.0
        for number in self.__get_iterable():
            total += number
            count += 1
        return total / count

    def union(self, iterable):
        return linq(self.__union(iterable))

    def __union(self, iterable):
        for x in self.__get_iterable():
            yield x
        for x in iterable:
            yield x

    def count(self):
        count = 0
        for number in self.__get_iterable():
            count += 1
        return count

    def first(self, default=None):
        return next(self.__get_iterable(), default)

    def last(self, default=None):
        it = self.__get_iterable()
        x = None
        b = False
        while True:
            try:
                x = next(it)
                b = True
            except StopIteration:
                if b:
                    return x
                return default

    def sum(self):
        return sum(self.__get_iterable())

    def tolist(self):
        return list(self.__get_iterable())

    def select(self, selector):
        return linq(map(selector, self.__get_iterable()))

    def order_by(self, predicate=None, default=False):
        return linq(iter(sorted(self.__get_iterable(), reverse=default, key=predicate)))

    def distinct(self):
        news_li = []
        for i in self.__get_iterable():
            if i not in news_li:
                news_li.append(i)
        return linq(news_li)

    def group_by(self, predicate=None):
        data = dict()
        s = list()
        if predicate:
            for dic in self.__get_iterable():
                if dic.get(predicate) in s:
                    data[dic.get(predicate)].append(dic)
                else:
                    l = list()
                    l.append(dic)
                    data[dic.get(predicate)] = l
                    s.append(dic.get(predicate))
            return data
        else:
            for dic in self.__get_iterable():
                for k, v in dic.items():
                    if k in s:
                        data[k].append(v)
                    else:
                        l = list()
                        l.append(v)
                        data[k] = l
                        s.append(k)
            return data

    def limit(self, count):
        return linq(iter(list(self.__get_iterable())[:count]))
