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


app = Celery('tasks', broker='redis://127.0.0.1:6379/2', backend='redis')

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    CELERY_RESULT_BACKEND="redis"
)


@app.task(bind=True, max_retries=5, default_retry_delay=1 * 6)
def add(self, x, y, **kwargs):
    a = kwargs.get('a')
    print(self)
    print(dir(self))
    print(a)
    b = int('1.a')
    add.apply_async((6, 10), {'a': 'c'}, countdown=10)
    return x + y



