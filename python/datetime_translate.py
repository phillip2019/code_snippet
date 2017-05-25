#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-25 19:02:47
# @Author  : wuyan (msn734506700@live)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import pytz

from datetime import datetime
from pytz import timezone


# tz = pytz.timezone('Asia/Shanghai')
# user_ts = int(datetime.utcnow()

utc_now = datetime.utcnow()
print(utc_now)
zh_cn_timezone = timezone('Asia/Shanghai')
loc_d = utc_now.replace(tzinfo=pytz.utc).astimezone(zh_cn_timezone)
# zh_cn = loc_d.astimezone(utc_now)
print(zh_cn_timezone.normalize(loc_d))
print(dir(loc_d))
print(loc_d.strftime('%Y-%m-%d %H:%M:%S'))
# print(zh_cn.strftime('%Y-%m-%d %H:%M:%S'))