#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Do."""
# @Date    : 2019-04-15 13:36:56
# @Author  : wuyan (msn734506700@live.com)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pandas as pd


def read_csv(filename):
    data = pd.read_csv(filename, sep=', ', squeeze=False)
    return data

def write_csv(filename, data):
    writer = pd.ExcelWriter(filename)
    data.to_excel(writer, 'Sheet1', index=False)
    writer.save()

def main():
    sf = u'/Users/xiaowei.song/资料/tongdun/爬虫/codes.csv'
    df = u'/Users/xiaowei.song/t.xls'
    data = read_csv(sf)
    write_csv(df, data)

if __name__ == '__main__':
    main()