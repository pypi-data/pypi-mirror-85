#!/usr/bin/env python
# -*-coding:utf-8-*-


"""

show how to talk to windows dll

"""

import ctypes
import os

"""
依赖dll必须修改系统变量PATH才能工作，调试模式打开，正式的根据exe所在路径即可正常工作
"""
# 当前工作目录下的dll加入系统搜索环境
abs_path_current = os.path.abspath('../utils')
os.environ['PATH'] = abs_path_current + os.pathsep + os.environ['PATH']


def add_dll_search_path(dll_path='.'):
    abs_path = os.path.abspath(dll_path)
    os.environ['PATH'] = abs_path + os.pathsep + os.environ['PATH']


def get_libdll(dll_path):
    """
    获取dll的ctype对象
    :param dll_path:
    :return:
    """

    libdll = ctypes.windll.LoadLibrary(dll_path)
    return libdll


# call dll function
# res = libdll.func(args1,args2)


# type map

# char *  -----     ctypes.c_char_p(string.encode())

# int  -----  ctypes.c_int(number)


# struct  ---  define ---


class INFO(ctypes.Structure):
    """
    基础信息结构体
    """
    _fields_ = [
        ('s1', ctypes.c_char * 24),
        ('s2', ctypes.c_char * 24),
        ('s3', ctypes.c_char * 40),
        ('s4', ctypes.c_char * 120),
        ('s5', ctypes.c_char * 120),
        ('s6', ctypes.c_char * 120),
        ('s7', ctypes.c_char * 120)
    ]

#         ---  传入    info = INFO()
#         info_ = ctypes.byref(info)
#         最后把这个info_ 传入进去


#  C# StringBuilder  ----- scbm = ctypes.create_string_buffer(40)

# C ByteArray  C# byte [] ----    mydata = bytearray([0] * 8192)
#
#     output = ctypes.create_string_buffer(bytes(mydata), len(mydata)) output就是要传进去的字节流
