#!/usr/bin/env python
# -*-coding:utf-8-*-


"""

和最长公共子序列的区别是必须是递增的。

"""

import pandas as pd


def longest_increasing_subsequence(seq_one, seq_two):
    df = pd.DataFrame(index=[item for item in seq_one],
                      columns=[item for item in seq_two])

    for i, c1 in enumerate(seq_one):
        for j, c2 in enumerate(seq_two):
            if c1 == c2:
                if (i - 1 < 0) or (j - 1 < 0):
                    df.iloc[i][j] = 1
                else:
                    df.iloc[i][j] = df.iloc[i - 1][j - 1] + 1
            else:
                df.iloc[i][j] = 0
    print(df)
