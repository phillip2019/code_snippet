#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Do."""
# @Date    : 2017-05-31 14:24:37
# @Author  : wuyan (msn734506700@live.com)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# import os

import time
import gevent
from gevent import select

start = time.time()


def tic():
    """Tic."""
    return 'at %1.1f seconds' % (time.time() - start)


def gr1():
    """Gr1."""
    # Busy waits for a second, but we don't want to stick around...
    print('Started Polling: %s' % tic())
    select.select([], [], [], 2)
    print('Ended Polling: %s' % tic())


def gr2():
    """Gr2."""
    # Busy waits for a second, but we don't want to stick around...
    print('Started Polling: %s' % tic())
    select.select([], [], [], 2)
    print('Ended Polling: %s' % tic())


def gr3():
    """Gr3."""
    print("Hey lets do some stuff while the greenlets poll, %s" % tic())
    gevent.sleep(1)


gevent.joinall([
    gevent.spawn(gr1),
    gevent.spawn(gr2),
    gevent.spawn(gr3),
])
