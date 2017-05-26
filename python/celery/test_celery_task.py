#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-26 09:53:30
# @Author  : wuyan (msn734506700@live)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# import os
from datetime import datetime

from tasks import add

if __name__ == '__main__':
    star_time = datetime.now()
    i = 0
    task_handler = []
    for _ in xrange(100000):
        x = add.delay(5, 6)
        task_handler.append(x)

    for t in task_handler:
        while t.ready():
            task_handler.
