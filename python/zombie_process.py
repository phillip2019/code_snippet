#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-08 13:27:51
# @Author  : wuyan
# @Version : $Id$

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import time


def main():
    """Main."""
    pid = os.fork()
    if 0 > pid:
        print('fork err:')  # fork failed
    elif 0 == pid:
        print('I am in child process, and child exit!')  # child process
        exit(0)
    else:
        print('Child process pid={}'.format(pid))
        print('I am in parent process, sleep for '
              ' 1 minute...ZZ...')  # parent process
        pid, status = os.wait()
        time.sleep(100)
        print('pid={}, status={}'.format(pid, status))
        print('I am in process, and parent exit!')
        exit(0)


if __name__ == '__main__':
    main()
