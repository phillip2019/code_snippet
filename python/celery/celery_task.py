#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-26 09:49:15
# @Author  : wuyan (msn734506700@live)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# import os

from celery import Celery


app = Celery('tasks', broker='redis://127.0.0.1:6379/')


@app.task
def add(x, y):
    return x + y


