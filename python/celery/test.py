#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Do."""
# @Date    : 2017-06-23 21:53:44
# @Author  : wuyan (msn734506700@live.com)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# import os
from collections import deque

a = deque([0, 1, 0, 0, 0])
K = 20
k = 2
print(a, sum(a))
while k <= K:
    a.appendleft(0)
    a[0] = a[2] + a[4]
    a.pop()
    # print(a)

# m, l = 1, 0
# k = 1
# t2 = 0
# while k <= K:
#     if k % 2 == 1:
#         l -= t2
#     elif k % 2 == 0:
#         t = m
#         m = m + l
#         t2 = l
#         l += t
    k += 1
    # print('K:{}，m:{}, l:{}'.format(K, m, l), m + l)
    print(a, sum(a))



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

