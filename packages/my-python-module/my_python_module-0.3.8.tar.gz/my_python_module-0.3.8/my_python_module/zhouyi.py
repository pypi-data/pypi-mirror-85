#!/usr/bin/env python
# -*-coding:utf-8-*-

from random import randint
from itertools import cycle

LIUSHISIGUA = {'乾': (1, 1, 1, 1, 1, 1), '坤': (0, 0, 0, 0, 0, 0),
               '屯': (0, 1, 0, 0, 0, 1), '蒙': (1, 0, 0, 0, 1, 0),
               '需': (0, 1, 0, 1, 1, 1), '讼': (1, 1, 1, 0, 1, 0),
               '师': (0, 0, 0, 0, 1, 0), '比': (0, 1, 0, 0, 0, 0),
               '小畜': (1, 1, 0, 1, 1, 1), '履': (1, 1, 1, 0, 1, 1),
               '泰': (0, 0, 0, 1, 1, 1), '否': (1, 1, 1, 0, 0, 0),
               '同人': (1, 1, 1, 1, 0, 1), '大有': (1, 0, 1, 1, 1, 1),
               '谦': (0, 0, 0, 1, 0, 0), '豫': (0, 0, 1, 0, 0, 0),
               '随': (0, 1, 1, 0, 0, 1), '蛊': (1, 0, 0, 1, 1, 0),
               '临': (0, 0, 0, 0, 1, 1), '观': (1, 1, 0, 0, 0, 0),
               '噬嗑': (1, 0, 1, 0, 0, 1), '贲': (1, 0, 0, 1, 0, 1),
               '剥': (1, 0, 0, 0, 0, 0), '复': (0, 0, 0, 0, 0, 1),
               '无妄': (1, 1, 1, 0, 0, 1), '大畜': (1, 0, 0, 1, 1, 1),
               '颐': (1, 0, 0, 0, 0, 1), '大过': (0, 1, 1, 1, 1, 0),
               '坎': (0, 1, 0, 0, 1, 0), '离': (1, 0, 1, 1, 0, 1),
               '咸': (0, 1, 1, 1, 0, 0), '恒': (0, 0, 1, 1, 1, 0),
               '遁': (1, 1, 1, 1, 0, 0), '大壮': (0, 0, 1, 1, 1, 1),
               '晋': (1, 0, 1, 0, 0, 0), '明夷': (0, 0, 0, 1, 0, 1),
               '家人': (1, 1, 0, 1, 0, 1), '睽': (1, 0, 1, 0, 1, 1),
               '蹇': (0, 1, 0, 1, 0, 0), '解': (0, 0, 1, 0, 1, 0),
               '损': (1, 0, 0, 0, 1, 1), '益': (1, 1, 0, 0, 0, 1),
               '夬': (0, 1, 1, 1, 1, 1), '姤': (1, 1, 1, 1, 1, 0),
               '萃': (0, 1, 1, 0, 0, 0), '升': (0, 0, 0, 1, 1, 0),
               '困': (0, 1, 1, 0, 1, 0), '井': (0, 1, 0, 1, 1, 0),
               '革': (0, 1, 1, 1, 0, 1), '鼎': (1, 0, 1, 1, 1, 0),
               '震': (0, 0, 1, 0, 0, 1), '艮': (1, 0, 0, 1, 0, 0),
               '渐': (1, 1, 0, 1, 0, 0), '归妹': (0, 0, 1, 0, 1, 1),
               '丰': (0, 0, 1, 1, 0, 1), '旅': (1, 0, 1, 1, 0, 0),
               '巽': (1, 1, 0, 1, 1, 0), '兑': (0, 1, 1, 0, 1, 1),
               '涣': (1, 1, 0, 0, 1, 0), '节': (0, 1, 0, 0, 1, 1),
               '中孚': (1, 1, 0, 0, 1, 1), '小过': (0, 0, 1, 1, 0, 0),
               '既济': (0, 1, 0, 1, 0, 1), '未济': (1, 0, 1, 0, 1, 0)}

FUXI_GUA_LIST = ['鼎', '恒', '巽', '井', '蛊', '升', '讼', '困', '未济', '解', '涣',
                 '坎', '蒙', '师', '遁', '咸', '旅', '小过', '渐', '蹇', '艮', '谦',
                 '否', '萃', '晋', '豫', '观', '比', '剥', '坤', '复', '颐', '屯',
                 '益', '震', '噬嗑', '随', '无妄', '明夷', '贲', '既济', '家人',
                 '丰', '离', '革', '同人', '临', '损', '节', '中孚', '归妹', '睽',
                 '兑', '履', '泰', '大畜', '需', '小畜', '大壮', '大有', '夬', '乾',
                 '姤', '大过']

FUXI_GUA = [LIUSHISIGUA[name] for name in FUXI_GUA_LIST]

FUXI_LIUSHI = [item for item in FUXI_GUA if item not in [
    (1, 1, 1, 1, 1, 1),
    (0, 0, 0, 0, 0, 0),
    (0, 1, 0, 0, 1, 0),
    (1, 0, 1, 1, 0, 1),
]]

FUXI_LIUSHI_CYCLE = cycle(FUXI_LIUSHI)


def get_gua_by_number(number):
    assert number < 64 and number >= 0
    x = f'{number:06b}'
    return tuple(int(i) for i in tuple(x))


def yaogua():
    """
    进行一次周易摇卦
    """
    zhugua = []
    biangua = []

    for i in range(0, 6):
        temp_array = []

        for x in range(0, 3):
            n = randint(0, 1)
            temp_array.append(n)

        sum_result = sum(temp_array)

        if sum_result == 3:
            zhugua.append(1)
            biangua.append(0)
        elif sum_result == 2:
            zhugua.append(1)
            biangua.append(1)
        elif sum_result == 1:
            zhugua.append(0)
            biangua.append(0)
        elif sum_result == 0:
            zhugua.append(0)
            biangua.append(1)

    print(get_gua_name(zhugua))
    print(get_gua_name(biangua))

    return {'zhuagua': zhugua,
            'biangua': biangua}


def get_gua_name(gua):
    for name, t in LIUSHISIGUA.items():
        if t == tuple(gua):
            return name + '卦'


def get_next_fuxi_liushi_gua(gua):
    flag = False
    for item in FUXI_LIUSHI_CYCLE:
        if flag:
            return item

        if item == gua:
            flag = True


from copy import copy


def change_yao(gua, num):
    """
    更改第几爻
    """
    new_gua = list(copy(gua))

    if new_gua[-num] == 1:
        new_gua[-num] = 0
    elif new_gua[-num] == 0:
        new_gua[-num] = 1
    return tuple(new_gua)


def hjjs(year):
    """
    输入年份 返回该年份的皇极经世卦象 公元前以负数作为输入
    运的讨论

    大过卦初爻变，化为夬卦。其统摄的时限是：公元前57一公元303年
    大过卦二爻变，化为咸卦。 其统摄的时限是：公元304—663年
    大过卦三爻变，化为困卦。 其统摄的时限是：公元664—1023年
    大过卦四爻变，化为井卦。 其统摄的时限是：公元1024—1383年
    大过卦五爻变，化为恒卦。 其统摄的时限是：公元1384—1743年
    大过卦上爻变，化为姤卦。 其统摄的时限是：公元1744—2103年

    世的讨论
    姤卦初爻变，化为乾卦。 其统摄的时限是：公元1744—1803年
    姤卦二爻变，化为遁卦。 其统摄的时限是：公元1804—1863年
    姤卦三爻变，化为讼卦。 其统摄的时限是：公元1864—1923年
    姤卦四爻变，化为巽卦。 其统摄的时限是：公元1924—1983年
    姤卦五爻变，化为鼎卦。 其统摄的时限是：公元1984—2043年
    姤卦上爻变，化为大过卦。其统摄的时限是：公元2044—2103年

    年的讨论
1984鼎1985恒1986巽1987井1988蛊1989升1990讼1991困1992未济1993解

1994涣1995蒙1996师1997遁1998咸1999旅2000小过2001渐2002蹇2003艮

2004谦2005否2006萃2007晋2008豫2009观2010比2011剥2012复2013颐

2014屯2015益2016震2017噬嗑2018随2019无妄2020明夷2021贲2022既济2023家人

2024丰2025革2026同人2027临2028损2029节2030中孚2031归妹2032睽2033兑

2034履2035泰2036大畜2037需2038小畜2039大壮2040大有2041央2042骺2043大过

    """
    # calc yun
    calc_start_year = -57

    yun_num = (year - (calc_start_year)) // (360 * 6)  # 运卦到下面第几个

    yun_gua_base = (0, 1, 1, 1, 1, 0)
    for i in range(yun_num):
        yun_gua_base = get_next_fuxi_liushi_gua(yun_gua_base)

    yun_yao_num = ((year - (-57)) % (360 * 6)) // 360 + 1  # 第几爻动

    yun_gua = change_yao(yun_gua_base, yun_yao_num)

    # calc shi

    calc_start_year = calc_start_year + (yun_num * 360 * 6) + \
                      (yun_yao_num - 1) * 360 + 1

    shi_yao_num = (year - calc_start_year) // 60 + 1

    shi_gua = change_yao(yun_gua, shi_yao_num)

    # calc year
    calc_start_year = calc_start_year + (60 * (shi_yao_num - 1))

    year_num = (year - calc_start_year)

    year_gua = shi_gua
    for i in range(year_num):
        year_gua = get_next_fuxi_liushi_gua(year_gua)

    print(f'公元{year}年的皇极经世卦象是：\n'
          f'运卦 {get_gua_name(yun_gua)}\n'
          f'世卦 {get_gua_name(shi_gua)}\n'
          f'年卦 {get_gua_name(year_gua)}\n'
          )

    return {
        'yun_gua': yun_gua,
        'shi_gua': shi_gua,
        'year_gua': year_gua
    }


if __name__ == '__main__':
    hjjs(2020)
