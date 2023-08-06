#!/usr/bin/env python
# -*-coding:utf-8-*-

import logging
import pandas as pd
import numpy as np
from collections import Iterable

logger = logging.getLogger(__name__)

"""
pandas的DataFrame的一些便捷操作函数
"""


def combine_df(df_value, old_df):
    """
    输入ndarray值，然后根据给的老df的column列名来输出一个新的df
    :param df_value:
    :param old_df:
    :return:
    """
    new_df = pd.DataFrame(df_value, columns=old_df.columns)
    return new_df


def change_df_type(df, column_name, type):
    """
    输入 df column_name type
    将df的某个列的类型更改为某个type 比如float等

    :param df:
    :param column_name:
    :param type:
    :return:
    """
    df[column_name] = df[column_name].astype(type)


def rename_df_columns(df, columns):
    """
    重新设置列名
    """
    df.rename(columns=columns, inplace=True)


def rename_df_column_by_index(dataset, index, to):
    """
    将index column 名字修改为 to
    :param dataset:
    :param index:
    :param to:
    :return:
    """
    assert isinstance(index, int)

    d = {dataset.columns[index]: to}
    logger.debug(f'dataset column {dataset.columns[index]}  renamed to {to}')
    dataset.rename(columns=d, inplace=True)
    return dataset


def rename_df_column_by_name(dataset, name, to):
    """
    将某个column 名字修改为 to
    :param dataset:
    :param name:
    :param to:
    :return:
    """
    assert isinstance(name, str)
    assert isinstance(to, str)

    d = {name: to}
    logger.debug(f'dataset column {name} renamed to {to}')
    dataset.rename(columns=d, inplace=True)
    return dataset


def get_all_column(df, column_name, remove_duplicate=True):
    """
    获取一列所有的值 默认去重
    :param column_name:
    :param remove_duplicate:
    :return:
    """
    column_values = df[column_name].values
    if remove_duplicate:
        column_values = set(column_values)

    column_values = list(column_values)

    return column_values


class NoInputDataError(Exception):
    pass


class DataReader(object):
    """
    pandas的io接口做的很好

    read data source from
    - file
    - python  DataFrame dict ...
    - sql

    ## 读取数据函数  - 后续可能会扩展补充附加数据模式
    - 初始化读取数据 利用DataFrame的初始化 加载数据
    - load_from_txt
    - load_from_csv
    - load_from_excel
    - load_from_sql

    ## 获取数据
    - get_dataset 获取数据集 feature_columns 指定那些列为你想要的dataset
                  返回ndarray [[],[]]
    - get_labels  label_column 指定label的列的index 返回ndarrya []


    ## 列名控制 非必要
    - set_columns 设置列名
    - rename_column
    - renmae_columns

    """

    def __init__(self, data=None, **kwargs):
        if data is None:
            self.df = None
        else:
            self.df = pd.DataFrame(data, **kwargs)

    def load_from_txt(self, filename, **kwargs):
        self.df = pd.read_csv(filename, **kwargs)

    def load_from_csv(self, filename, **kwargs):
        self.df = pd.read_csv(filename, **kwargs)

    def load_from_excel(self, filename, **kwargs):
        self.df = pd.read_excel(filename, **kwargs)

    def load_from_json(self, filename, **kwargs):
        self.df = pd.read_json(filename, **kwargs)

    def load_from_sql(self, sql_query, sql_conn, **kwargs):
        self.df = pd.read_sql(sql_query, sql_conn, **kwargs)

    def set_columns(self, columns):
        self.df.columns = columns

    def rename_column(self, origin_column_name, column_name):
        """
        默认的column 可用 0 1 2 <int> 来引用
        :param origin_column_name:
        :param column_name:
        :return:
        """
        d = {}
        d[origin_column_name] = column_name
        self.df.rename(columns=d, inplace=True)

    def rename_columns(self, columns):
        self.df.rename(columns=columns, inplace=True)

    def get_df(self):
        return self.df

    def get_dataset(self, feature_columns):
        """
        输入 pandas 初步处理了的 df数据，针对knn进行数据准备
        :param df:
        :return:
        """
        if self.df is None:
            raise NoInputDataError

        dataset = self.df.iloc[:, feature_columns].values

        return dataset

    def get_labels(self, label_column):
        if self.df is None:
            raise NoInputDataError

        labels = self.df.iloc[:, label_column].values
        return labels


def to_ndarray(pyobj, dtype=None):
    """
    将一个可迭代的python对象转变成为numpy的ndarray对象
    """
    if not isinstance(pyobj, Iterable):
        raise TypeError('it is not a iterable object')

    if isinstance(pyobj, np.ndarray):
        return pyobj

    if dtype is not None:
        return np.array(pyobj, dtype)
    else:
        return np.array(pyobj)


def mean(obj):
    """
    计算均值
    """
    obj = to_ndarray(obj)
    return obj.mean()


def median(obj, axis=None):
    """
    计算中位数
    """
    obj = to_ndarray(obj)
    return np.median(obj, axis=axis)


from collections import Counter


def mode(obj):
    """
    计算众数，支持最大相同记数返回
    """

    c = Counter(obj)

    most = 0
    first = True
    for k, v in c.most_common():
        if first:
            most = v
            first = False
            yield k
        else:
            if most == v:
                yield k
            else:
                break


def quantile(obj, seq=None):
    """
    计算分位数
    """
    obj = to_ndarray(obj)

    if seq is None:
        seq = range(0, 101, 25)

    res = pd.Series(np.percentile(obj, seq), index=seq)
    return res


def pvariance(obj):
    """
    计算总体方差
    """
    obj = to_ndarray(obj)

    return np.var(obj)


def pstd_deviation(obj):
    """
    计算总体标准差
    """
    obj = to_ndarray(obj)

    return np.std(obj)


def variance(obj):
    """
    计算样本方差
    """
    obj = to_ndarray(obj)

    return np.var(obj, ddof=1)


def std_deviation(obj):
    """
    计算样本标准差
    :param obj:
    :return:
    """
    obj = to_ndarray(obj)

    return np.std(obj, ddof=1)


def permutation(n, k):
    """
    排列数 n!(n-k)!
    :param n:
    :param k:
    :return:
    """
    from scipy.special import perm
    return perm(n, k, exact=True)


def combination(n, k):
    """
    组合数 n!/k!(n-k)!
    :param n:
    :param k:
    :return:
    """
    from scipy.special import comb
    return comb(n, k, exact=True)


def n_choose_k(n, k, order=None):
    """
    n个元素选择k个
    :param n:
    :param k:
    :param order: 默认为None，也就是组合数，其他输入值将进行bool处理，获得True之后返回排列数。
    :return:
    """
    if order is None or not bool(order):
        return combination(n, k)
    elif bool(order):
        return permutation(n, k)
