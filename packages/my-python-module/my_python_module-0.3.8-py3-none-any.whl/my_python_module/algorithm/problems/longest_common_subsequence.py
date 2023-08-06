#!/usr/bin/env python
# -*-coding:utf-8-*-


"""

动态规划法解最长公共子序列问题，经典案例，还是很实用的。

子序列不一定要求递增的，更多的是比较相似度

"""

import pandas as pd


def longest_common_subsequence(seq_one, seq_two):
    df = pd.DataFrame(index=[item for item in seq_one], columns=[item for item in seq_two])

    df = df.fillna(0)

    for i, c1 in enumerate(seq_one):
        for j, c2 in enumerate(seq_two):
            if c1 == c2:
                if (i - 1 < 0) or (j - 1 < 0):
                    df.iloc[i][j] = 1
                else:
                    df.iloc[i][j] = df.iloc[i - 1][j - 1] + 1
            else:
                if i < 1 and j < 1:
                    df.iloc[i][j] = 0
                elif i < 1:
                    df.iloc[i][j] = max(0, df.iloc[i][j - 1])
                elif j < 1:
                    df.iloc[i][j] = max(df.iloc[i - 1][j], 0)
                else:
                    df.iloc[i][j] = max(df.iloc[i - 1][j], df.iloc[i][j - 1])
    print(df)

