#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Do."""
# @Date    : 2017-06-23 21:53:44
# @Author  : wuyan (msn734506700@live.com)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import collections
import json

import pandas as pd

# import os
from collections import deque

# a = deque([0, 1, 0, 0, 0])
# K = 20
# k = 2
# print(a, sum(a))
# while k <= K:
#     a.appendleft(0)
#     a[0] = a[2] + a[4]
#     a.pop()
#     # print(a)
#
# # m, l = 1, 0
# # k = 1
# # t2 = 0
# # while k <= K:
# #     if k % 2 == 1:
# #         l -= t2
# #     elif k % 2 == 0:
# #         t = m
# #         m = m + l
# #         t2 = l
# #         l += t
#     k += 1
#     # print('K:{}，m:{}, l:{}'.format(K, m, l), m + l)
#     print(a, sum(a))



# 【1， 0， 0， 0]
# [1, 0, 1, 0, 0]
# [0, 1, 0, 1, 0]
# [2, 0, 1, 0, 1]
# [0, 2, 0, 1, 0]
# [3, 0, 2, 0, 1]

# 【1， 1， 0， 0】

#  [0, 1, 1, 0]

# 【1， 1， 0， 0】
# 【0， 1， 0， 1】
# 【2， 0， 1， 1】
# 【0， 2， 0， 1】
# [1, 1, 0, 0, 0]    1

# [0, 1, 1, 0, 0] 2

# [1, 0, 1, 1, 0]    3

# [0, 2, 0, 1, 1]  4

# [1, 0, 2, 0, 1]  5
import prestodb

phone_lists = ['13958404221',
'13906894657',
'13616898888',
'13906893618',
'18967953439',
'18967953767',
'13606799297',
'15868915898',
'13906896790',
'13867922880',
'13967996461',
'13957933108',
'13575986133',
'13757920210',
'13705798039',
'13064601865',
'15958442662',
'13732403330',
'13606899937',
'18329075257',
'18957907533',
'13906891245',
'13758903029',
'15868908885',
'13757953628',
'13586957937',
'13819967059',
'13819961616',
'13606899681',
'13957935817',
'13906890192',
'13606892305',
'13735651670',
'13515898732',
'13757926754',
'13705799992',
'13806791136',
'13906890882',
'15355300606',
'13957907558',
'13957914488',
'13606891511',
'15868960000',
'13867918885',
'13606893275',
'13516988657',
'13735653828',
'13958499178',
'13738999888',
'13705795350',
'13735751888',
'13705794675',
'13605820552',
'13515892916',
'13957915178',
'13665858162',
'18757671777',
'15868929618',
'13906891953',
'13757959951',
'13858965819',
'13065914444',
'13957903445',
'13806792429',
'13566719726',
'13605820028',
'13506893858',
'13605828493',
'18857971111']

conn = prestodb.dbapi.connect(
    host='172.18.5.10',
    port=28765,
    user='hive',
    catalog='hive',
    schema='dim',
)


if __name__ == '__main__':
    df = pd.read_excel(r'C:\Users\Administrator\Desktop\老板娘直播签约清册.xlsx', header=0)
    df = df.fillna(0.0)
    df[['联系方式']] = df[['联系方式']].astype(str)
    landlady_supplier_phone_list = df.to_dict('records')
    landlady_supplier_phone_set = {str(p['联系方式']) for p in landlady_supplier_phone_list}
    supplier_shop_id_m = {}
    # print(landlady_supplier_phone_set)

    select_sql_params = "','".join(landlady_supplier_phone_set)
    select_sql = '''
            select shop_id
            ,contact_phone
            from dim.dim_ncg_shops_zf
            where 1=1
            and end_date = '9999-12-31'
            and lang = 'zh'
            and is_shop_on = 'Y'
            and contact_phone in ('{}')
          '''.format(select_sql_params)

    presto_cur = conn.cursor()
    presto_cur.execute(select_sql)
    records = presto_cur.fetchall()
    supplier_shop_id_phone_df = pd.DataFrame(records, columns=['shop_id', 'contact_phone'])

    rdf = pd.merge(df, supplier_shop_id_phone_df, how='left', left_on='联系方式', right_on='contact_phone')
    # rdf = df.join(supplier_shop_id_phone_df.set_index('contact_phone'), how='left', on=['联系方式'])

    rdf.to_excel(r'C:\Users\Administrator\Desktop\老板娘直播签约清册补充店铺编号.xlsx')

    # # print("records: {}".format(records))
    # supplier_shop_id_num_m = collections.defaultdict(int)
    # for r in records:
    #     supplier_shop_id_m[r[1]] = r[0]
    #     supplier_shop_id_num_m[r[1]] += 1

    # for k, v in supplier_shop_id_num_m.items():
    #     if v > 1:
    #         print('phone: {}, v: {}'.format(k, v))
    #
    # for sp in landlady_supplier_phone_list:
    #     sp['shop_id'] = supplier_shop_id_m.get(str(sp['联系方式']), ' ')
    #
    # print(json.dumps(landlady_supplier_phone_list, ensure_ascii=False))

    # phone_years_dict = {}
    # print(phone_years_list)
    # for p in phone_years_list:
    #     phone_years_dict[p.get('owner_phone')] = p.get('year_num', 0)
    # print(phone_years_dict)
    # for p in phone_lists:
    #     print('{},{}'.format(p, round(phone_years_dict.get(int(p), 0))))

