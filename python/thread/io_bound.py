#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Io bound compare example."""
# @Date    : 2017-05-28 21:45:01
# @Author  : wuyan (msn734506700@live.com)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# import os
import ssl
import time
import threading
import urllib2
from gevent import monkey
monkey.patch_all()

import gevent  # noqa

# 忽略ssl校验，避免抛出CERTIFICATE_VERIFY_FAILED错误
ssl._create_default_https_context = ssl._create_unverified_context


def urllib2_(url):
    """Urllib open."""
    try:
        urllib2.urlopen(url, timeout=10).read()
        # time.sleep(10)
    except Exception, e:
        print(e)


def gevent_(urls):
    """Open task with gevent."""
    jobs = [gevent.spawn(urllib2_, url) for url in urls]
    gevent.joinall(jobs, timeout=5)
    for i in jobs:
        i.join()


def thread_(urls):
    """Open task with thread."""
    a = []
    for url in urls:
        t = threading.Thread(target=urllib2_, args=(url,))
        a.append(t)
    for i in a:
        i.start()
    for i in a:
        i.join()


if __name__ == "__main__":
    urls = ["https://127.0.0.1"] * 100
    t1 = time.time()
    gevent_(urls)
    t2 = time.time()
    print('gevent-time:%s' % (t2 - t1))
    t3 = time.time()
    thread_(urls)
    t4 = time.time()
    print('thread-time:%s' % (t4 - t3))
