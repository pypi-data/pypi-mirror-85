#!/usr/bin/env python
# -*-coding:utf-8-*-

import pytest
from my_python_module.unique_key import mapping_string
from my_python_module.basic.str import random_string_generator
from collections import defaultdict
from my_python_module.basic.list import double_iter


def test_mapping_string():
    data = defaultdict(lambda: 0)

    for i in range(100000):
        s = random_string_generator()

        c = mapping_string(s)

        data[c] += 1

    values = list(data.values())

    for i, j in double_iter(values):
        assert i == pytest.approx(j, rel=0.1)
