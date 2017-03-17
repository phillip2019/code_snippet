# !/usr/bin/python
# -*- coding: utf-8 -*-
u"""这是一个测试windows系统python内存使用量脚本."""

import os
from wmi import WMI

"""
    依赖项较多，请安装好以下几项
    1.wmi pip install wmi
    2.pywin32
    3.pypiwin32 pip install pypiwin32
"""


def memory():
    u"""调用wmi服务，获取进程内存量使用情况."""
    w = WMI('.')
    result = w.query("SELECT WorkingSet FROM Win32_PerfRawData_PerfProc_Process WHERE IDProcess=%d" % os.getpid())
    return int(result[0].WorkingSet)


if __name__ == '__main__':
    memory()
