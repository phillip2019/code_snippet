#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Do."""
# @Date    : 2017-06-19 18:55:54
# @Author  : wuyan (msn734506700@live.com)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# import os
# gunicorn -w 9 -b 0.0.0.0:5000 --timeout 500 flask_server:app
import time

from flask import Flask

app = Flask('app')


@app.route('/')
def test():
    """Test."""
    time.sleep(3)
    return 'OK'


if __name__ == '__main__':
    app.run()
