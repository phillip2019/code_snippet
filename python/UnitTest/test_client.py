#!/usr/bin/python
# -*- coding: utf-8 -*-v
"""Do."""
# @Date    : 2018-01-15 10:18:59
# @Author  : wuyan (msn734506700@live.com)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import pytest
import unittest
from unittest import mock
import client


class TestClient(unittest.TestCase):
    def test_success_request(self):
        success_send = mock.Mock(return_value='200')
        client.send_request = success_send
        self.assertEqual(client.visit_ustack(), '200')

    def test_fail_request(self):
        """Test fail request."""
        fail_send = mock.Mock(return_value='404')
        client.send_request = fail_send
        self.assertEqual(client.visit_ustack(), '404')

    def test_call_send_request_with_right_arguments(self):
        """Test call back."""
        client.send_request = mock.Mock()
        client.visit_ustack()
        self.assertEqual(client.send_request.called, True)
        call_args = client.send_request.call_args
        self.assertIsInstance(call_args[0][0], str)

    def test_success_request_patch(self):
        status_code = '200'
        success_send = mock.Mock(return_value=status_code)
        with mock.patch('client.send_request', success_send):
            from client import visit_ustack
            self.assertEqual(visit_ustack(), status_code)

    def test_fail_request_with_patch(self):
        status_code = '404'
        fail_send = mock.Mock(return_value=status_code)
        with mock.patch('client.send_request', fail_send):
            from client import visit_ustack
            self.assertEqual(visit_ustack(), status_code)

    def test_fail_request_with_patch_object(self):
        status_code = '200'
        success_send = mock.Mock(return_value=status_code)
        with mock.patch.object(client, 'send_request', success_send):
            from client import visit_ustack
            self.assertEqual(visit_ustack(), status_code)

    def test_fail_request_with_patch_object2(self):
        status_code = '300'
        fail_send = mock.mock(return_value='404')
        self.assertEqual(client.visit_ustack(), status_code)


def func(x):
    return x + 1

def test_func_success():
    assert func(4) == 5

def test_func_fail():
    assert func(3) == 5

def log_global_env_facts(f):
    if pytest.config.pluginmanager.hasplugin('junitxml'):
        my_junit = getattr(pytest.config, '_xml', None)
        