#!/usr/bin/env python
# -*-coding:utf-8-*-


import dataset

db = dataset.connect('sqlite:///:memory:')

table = db['sometable']
