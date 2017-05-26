#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-26 20:04:52
# @Author  : wuyan (msn734506700@live)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# import os
from collections import deque
from datetime import datetime


COUNTER = 10000000


def main():
    t_list = []
    b_append = datetime.now()
    for i in xrange(COUNTER):
        t_list.append(i)
    e_append = datetime.now()

    b_pop = datetime.now()
    for i in xrange(COUNTER - 1, -1, -1):
        t_list.pop(i)
    e_pop = datetime.now()

    b2_append = datetime.now()
    t_deque = deque()
    for i in xrange(COUNTER):
        t_deque.append(i)
    e2_append = datetime.now()

    b2_pop = datetime.now()
    for i in xrange(COUNTER):
        t_deque.popleft()
    e2_pop = datetime.now()
    print('list append %d time %s' % (COUNTER, e_append - b_append))
    print('list pop %d time %s' % (COUNTER, e_pop - b_pop))
    print('deque append %d time %s' % (COUNTER, e2_append - b2_append))
    print('deque pop %d time %s' % (COUNTER, e2_pop - b2_pop))


if __name__ == '__main__':
    main()

