#!/usr/bin/env python
# -*-coding:utf-8-*-

"""

这里放着很多和项目相关的唯一性标识id生成函数，慢慢都应该在这里汇总，规范起来。

"""
import shortuuid


def one_activation_code(length=6):
    """
    长度默认6位
    小写字母或数字 考虑l和1看不太清楚,将l去除了。
    这样还是会有四十几亿的可能性。'abcdefghijkmnopqrstuvwxyz0123456789'
    shortuuid 使用os.urandom，引入机器随机，基本保证激活码不重复。
    """

    res = shortuuid.ShortUUID(
        alphabet='abcdefghijkmnopqrstuvwxyz0123456789').random(length)
    return res


def gen_activation_code(n=50, length=6):
    """
    输出多个激活码，返回一个生成器以提高效率。
    """
    res = (one_activation_code(length) for i in range(n))
    return res
