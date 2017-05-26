#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-26 16:51:29
# @Author  : wuyan (msn734506700@live)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# import os

from collections import deque
from datetime import datetime
import Queue
import threading


class ActorScheduler(object):
    def __init__(self):
        self._actors = {}           # Mapping of names to actors
        self._msg_queue = deque()   # Message queue

    def new_actor(self, name, actor):
        """Admit a newly started actor to the scheduler and give it a name."""
        self._actors[name] = actor
        # 两种写法，一种向队列添加空任务，交给actor执行，可能浪费执行时间，另外一种自动执行生成器，调到执行步骤
        actor.next()
        # self._msg_queue.append((actor, None))

    def send(self, name, msg):
        """Send a message to a named actor."""
        actor = self._actors.get(name)
        if actor:
            self._msg_queue.append((actor, msg))

    def run(self):
        """Run as long as there are pending messages."""
        while self._msg_queue:
            actor, msg = self._msg_queue.popleft()
            try:
                actor.send(msg)
            except StopIteration:
                pass


class ThreadCounter(threading.Thread):
    """Threaded Url Grab."""
    def __init__(self, counter, print_queue):
        super(ThreadCounter, self).__init__()
        # self.queue = queue
        self.counter = counter
        self.print_queue = print_queue

    def run(self):
        while self.counter > 0:

            # fetch num from queue
            # num = self.queue.get()

            # place chunk into out queue
            self.print_queue.put(self.counter)
            self.counter -= 1

            # signals to queue job is done
            # self.queue.task_done()


class ThreadPrinter(threading.Thread):
    """Print the num from queue."""
    def __init__(self, queue):
        super(ThreadPrinter, self).__init__()
        self.queue = queue

    def run(self):
        while True:
            num = self.queue.get()
            print('Threading got:', num)
            self.queue.task_done()


def printer():
    while True:
        msg = yield
        print('Got:', msg)


def counter(sched):
    while True:
        # Receive the current count
        n = yield
        if n == 0:
            break
        # Send to the printer task
        sched.send('printer', n)

        # Send the next count to the counter task (recursive)
        sched.send('counter', n - 1)


COUNTER_NUM = 100000

# Example use
if __name__ == '__main__':
    b_time = datetime.now()
    sched = ActorScheduler()
    # Create the initial actors
    sched.new_actor('printer', printer())
    sched.new_actor('counter', counter(sched))

    # Send an initial message to the counter to initiate
    sched.send('counter', COUNTER_NUM)
    sched.run()
    e_time = datetime.now()
    print('Yield cost %s %s' % ((e_time - b_time), '#' * 30))

    b2_time = datetime.now()
    # task_queue = Queue.Queue()
    print_queue = Queue.Queue()
    # for i in xrange(COUNTER_NUM, 0, -1):
        # task_queue.put(i)
    ts = []
    t_counter = ThreadCounter(COUNTER_NUM, print_queue)
    ts.append(t_counter)
    t_printer = ThreadPrinter(print_queue)
    ts.append(t_printer)
    for t in ts:
        t.setDaemon(True)
        t.start()
    # task_queue.join()
    print_queue.join()
    e2_time = datetime.now()
    print('Threading cost %s %s' % ((e2_time - b2_time), '#' * 30))
