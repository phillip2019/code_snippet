#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Do."""
# @Date    : 2017-05-31 16:12:07
# @Author  : wuyan (msn734506700@live.com)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import urllib2
import simplejson as json


import gevent.monkey
gevent.monkey.patch_socket()

import gevent  # noqa


def fetch(pid):
    """Fetch."""
    try:
        response = urllib2.urlopen('http://api.map.baidu.com',
                                   timeout=2)
    except Exception as e:
        print(e)
    else:
        result = response.read()
        json_result = json.loads(result)
        datetime = json_result['datetime']

        print('Process %s: %s' % (pid, datetime))
        return json_result['datetime']


def synchronous():
    """Sync io."""
    for i in range(1, 10):
        fetch(i)


def asynchronous():
    """Async io."""
    threads = []
    for i in range(1, 10):
        threads.append(gevent.spawn(fetch, i))
    gevent.joinall(threads)


print('Synchronous:')
synchronous()

print('Asynchronous:')
asynchronous()
