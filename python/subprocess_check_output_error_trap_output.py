#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-19 09:43:55
# @Author  : wuyan
# @Version : V0.1

import os
import sys
import subprocess

try:
    output = subprocess.check_output(
        'echo to stdout; echo to stderr 1>&2',
        shell=True,
        stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as err:
    print('ERROR:', err)
else:
    print('Have {} bytes in output: {!r}'.format(
        len(output),
        output.decode('utf-8')))
print(sys.version_info)