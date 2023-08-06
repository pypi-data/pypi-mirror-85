#!/usr/bin/env python
# -*-coding:utf-8-*-


"""
matplotlib plot help utils

line_plot line plot
bar_plot vertical bar plot
barh_plot horizontal bar plot
hist_plot histogram
box_plot box plot
area_plot
pie_plot pie plot
scatter_plot scatter plot
hexbin_plot hexbin plot

‘kde’ : Kernel Density Estimation plot
‘density’ : same as ‘kde’
"""

import matplotlib.pyplot as plt
import numpy as np


def set_matplotlib_support_chinese(font='SimHei'):
    """
    设置matplotlib支持中文
    :param font:
    :return:
    """
    from matplotlib import rcParams

    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'].insert_child(0, font)  # 插入中文字体
    rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


fig, ax = plt.subplots()


# from matplotlib.axes._axes import Axes

def line_plot1(ax, y_values, x_ticks, xlabel='', ylabel='', ylim=None,
               **kwargs):
    """
    绘制直线图
    :param ax:
    :param x:
    :param y:
    :param param_dict:
    :return:
    """
    if ylabel:
        ax.set_ylabel(ylabel)  # 设置y标签

    if xlabel:
        ax.set_xlabel(xlabel)  # 设置x标签

    x_values = np.arange(len(x_ticks))
    ax.set_xticks(x_values)  # 设置x标记
    ax.set_xticklabels(x_ticks)

    if ylim is not None:
        ax.set_ylim(ylim)  # 设置y轴范围

    out = ax.plot(y_values, **kwargs)
    return out


def pie_plot(ax, labels, sizes, **kwargs):
    """
    绘制饼状图
    :return:
    """

    ax.axis('equal')  # 确保画成一个圆
    out = ax.pie(sizes, labels=labels, autopct='%2.0f%%', startangle=90,
                 **kwargs)
    return out


def barh_plot(ax, y_values, x_labels, xlabel='', ylabel='', **kwargs):
    """
    水平条形图
    :param ax:
    :return:
    """
    y = np.arange(len(x_labels))

    ax.set_yticks(y)
    ax.set_yticklabels(x_labels)

    if xlabel:
        ax.set_ylabel(xlabel)

    if ylabel:
        ax.set_xlabel(ylabel)

    out = ax.barh(y, y_values, align='center', **kwargs)
    return out


def hist_plot(ax, y_values, x_bins, xlabel='', ylabel='', title='', **kwargs):
    """

    :param ax:
    :return:
    """
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    out = ax.hist(x_bins[:-1], bins=x_bins, weights=y_values, **kwargs)
    return out


def scatter_plot1(ax, X, xlabel='', ylabel='', title='', **kwargs):
    """
    散点图 输入X 第一列x 第二列 y
    :param ax:
    :param X:
    :return:
    """
    x_group = []
    y_group = []
    for x, y in X:
        x_group.append(x)
        y_group.append(y)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)

    out = ax.scatter(x_group, y_group, **kwargs)
    return out


def scatter_plot(ax, x, y, xlabel='', ylabel='', title='', **kwargs):
    """
    :param ax:
    :param X:
    :return:
    """
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)

    out = ax.scatter(x, y, **kwargs)
    return out


def polyfit_plot(ax, x, y, deg=1, xlabel='', ylabel='', title='', **kwargs):
    """
    多项式拟合绘图
    :return:
    """
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)

    predict_func = np.poly1d(np.polyfit(x, y, deg))

    out = ax.plot(x, y, '.', x, predict_func(x), '-', **kwargs)
    return out


def myplotter(ax, x, y, param_dict):
    """
    ax matplotlib ax object
    x data plot on x axis
    y data plot on y axis
    param_dict other kwargs

    """
    out = ax.plot(x, y, **param_dict)
    return out
