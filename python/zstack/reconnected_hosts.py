#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Do."""
# @Date    : 2017-10-10 17:50:07
# @Author  : wuyan (msn734506700@live.com)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# import os

import re
import requests
import argparse
# try:
#     import simplejson as json
# except ImportError:
#     import json
import json
uri = 'http://zstack.tongdun.cn/api/sync'



def query_vm_by_status(session, status):
    """Query vm created"""
    body = {
    "org.zstack.header.host.APIQueryHostMsg": {
        "conditions": [
          {
            "name": "status",
            "op": "=",
            "value": "Disconnected"
          }
        ],
        "sortBy": "createDate",
        "sortDirection": "desc",
        "session": session,
      }
    }
    vms_uuid = []
    r = requests.post(uri, json=body)
    if r.status_code == 200:
        result = r.json()
        vms = result['org.zstack.header.host.APIQueryHostReply']['inventories']
        for vm in vms:
            vms_uuid.append(vm.get('uuid'))
    else:
        print('查询错误，详情为{}'.format(r))
        # raise Error('查询错误，详情为{}'.format(r))
    return vms_uuid

def reconnect(instance_id, session):
    data = {
          "org.zstack.header.host.APIReconnectHostMsg": {
            "uuid": instance_id,
            "session": session
          }
        }
    r = requests.post(uri, json=data)
    print(r.content)

def main():
    """Main."""
    login_body = {"org.zstack.header.identity.APILogInByAccountMsg": {
        "accountName": "admin",
        "password": "540ae1bf0fd912d7f4db2fad48fa4396679a06b3d3ceead77832e831a0361f9a58f512a0a7dfa60bbbf6d82656411196b57dfc3014b5a069054e6c64e89b16d7",
        "session": {
          "uuid": "ac28cdef1dee4d3abf066bc6dc4b1149"
        }
    }
    }
    login_r = requests.post(uri, json=login_body)

    if login_r.status_code == 200:
        result = login_r.json()
        session = {
          'uuid': result["org.zstack.header.identity.APILogInReply"]['inventory']['uuid']
        }
        print('session: {}'.format(session))

        # Disconnected机器
        vms_uuid = query_vm_by_status(session, 'Disconnected')
        for uuid in vms_uuid:
            reconnect(uuid, session)
        print(json.dumps(result, indent=4))
    else:
        print('登录失败，请重新再试!')


if __name__ == '__main__':
    main()