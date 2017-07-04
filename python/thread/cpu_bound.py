#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Do."""
# @Date    : 2017-06-01 22:52:20
# @Author  : wuyan (msn734506700@live.com)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# import os

from multiprocessing import Process
from multiprocessing.dummy import Process as Thr
from gevent import monkey;  monkey.patch_all()  # noqa
import gevent


def run(i):
    """Run."""
    lists = range(i)
    list(set(lists))


if __name__ == "__main__":
    # 多进程
    for i in range(30):      # 10-2.1s 20-3.8s 30-5.9s
        t = Process(target=run, args=(5000000,))
        t.start()

    # # 多线程
    # for i in range(30):    # 10-3.8s  20-7.6s  30-11.4s
    #     t = Thr(target=run, args=(5000000,))
    #     t.start()

    # # 协程
    # # 10-4.0s 20-7.7s 30-11.5s
    # jobs = [gevent.spawn(run, 5000000) for i in range(30)]
    # gevent.joinall(jobs)
    # for i in jobs:
    #     i.join()

    # # 单线程
    # for i in range(30):  # 10-3.5s  20-7.6s 30-11.3s
    #     run(5000000)
