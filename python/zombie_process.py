#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-08 13:27:51
# @Author  : xiaowei.song (xiaowei.song@tongdun.cn)
# @Version : $Id$

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import time
import traceback


def main():
	pid = os.fork()
	if 0 > pid:
		print('fork err:')  # fork failed
	elif 0 == pid:
		print('I am in child process, and child exit!')  # child process
		exit(0)
	else:
		print('I am in parent process, sleep for 1 minute...ZZ...')  # parent process
		time.sleep(60)
		print('I am in process, and parent exit!')
		exit(0)


if __name__ == '__main__':
	main()