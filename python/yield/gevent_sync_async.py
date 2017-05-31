#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Do."""
# @Date    : 2017-05-31 15:36:25
# @Author  : wuyan (msn734506700@live.com)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# import os

import gevent
import random


def task(pid):
    """Some non-deterministic task."""
    gevent.sleep(1)
    print('Task %s done' % pid)


def synchronous():
    """Sync."""
    for i in range(1, 10):
        task(i)


def asynchronous():
    """Async."""
    threads = [gevent.spawn(task, i) for i in xrange(10)]
    gevent.joinall(threads)


print('Synchronous:')
synchronous()

print('Asynchronous:')
asynchronous()
