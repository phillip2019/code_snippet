#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Do."""
# @Date    : 2018-01-15 10:04:09
# @Author  : wuyan (msn734506700@live.com)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os

import unittest
from unittest import mock

# class Mock(spec=None, side_effec=None, return_value=DEFAULT, wraps=None, name=None, spec_set=None, **kwargs):

import requests


def send_request(url):
    """Send request."""
    r = requests.get(url)
    return r.status_code


def visit_ustack():
    """Visit ustack."""
    return send_request('https://www.google.com')
