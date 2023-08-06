#!/usr/bin/env python
# -*-coding:utf-8-*-

import logging
from collections import deque

logger = logging.getLogger(__name__)


def get_related_value(d, item):
    if item in d:
        return d[item]

    if item in d.values():
        return item

    raise ValueError("Can not found the related value.")


def remove_dict_key(d, key, inplace=True):
    """
    delete some key in dict

    inplace = True : delete in origin dict

    """
    if inplace:
        new_d = d.copy()
        try:
            del new_d[key]
        except KeyError:
            pass
        return new_d
    else:
        try:
            del d[key]
        except KeyError:
            pass

        return d


class LastElements(deque):
    """
    优雅版： 继承自deque对象，然后加上一些方便的方法
    data 返回列表，让人们忘了deque这个玩意儿吧，列表大家都熟悉，然后 __iter__ 属性还是在的。
    后面还会有一些对原python对象的简单封装，其中data这个属性含义总是表达本封装对象内应该存储的数据。
    """

    def __init__(self, length, data=None):
        if data is None:
            super().__init__(maxlen=length)
        else:
            super().__init__(data, maxlen=length)

    @property
    def data(self):
        return list(self)