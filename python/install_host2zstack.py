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


parser = argparse.ArgumentParser(description=u'请根据提示填写相应的参数.')
parser.add_argument('--get', metavar='get', nargs='?', type=unicode, help=u'要操作的zstack地址',
                    dest='url', default='192.168.51.10')
parser.add_argument('--start_ip', required=True, type=unicode, help=u'起始主机IP',
        dest='start_ip')
parser.add_argument('--num', required=True, type=int, help=u'添加主机个数')
parser.add_argument('--cluster_uuid', required=True, type=unicode, help=u'集群uuid')
parser.add_argument('--env', metavar='env', nargs='?', type=unicode,
        help=u'开发、生产或沙盒环境(p/s/t)!', default='s')
parser.add_argument('--zone', nargs='?', type=unicode, help=u'hz/sh/dev',
        default='hz')
args = parser.parse_args()
uri = r'http://{}:8080/zstack/api'.format(args.url)


def is_collection(obj):
    """Is collection."""
    return isinstance(obj, (list, tuple, set))


def resolve_resp_list(api, data_str):
    if isinstance(data_str, bytes):
        data_str = data_str.decode()
    # zstack 接口并不是REST api,所以其得按其返回的数据进行某种解析
    # 例如请求的json里最外层key为org.zstack.header.image.APIQueryImageMsg时
    # 返回的json中最外层的key就是org.zstack.header.image.APIQueryImageReply
    # 但并不是所有的接口都是按照这个规则来的
    # 这里是对字符串进行处理
    reply_api = '{}Reply'.format(''.join(api[:-3]))
    data = json.loads(data_str)['result']
    reply = json.loads(data)[reply_api]
    if reply['success']:
        results = reply['inventories']
    else:
        results = []
    return results

def resolve_resp_other(api, data_str):
    if isinstance(data_str, bytes):
        data_str = data_str.decode()
    # zstack 接口并不是REST api,所以其得按其返回的数据进行某种解析
    # 例如请求的json里最外层key为org.zstack.header.image.APIQueryImageMsg时
    # 返回的json中最外层的key就是org.zstack.header.image.APIQueryImageReply
    # 但并不是所有的接口都是按照这个规则来的
    # 这里是对字符串进行处理
    reply_api = '{}Reply'.format(''.join(api[:-3]))
    data = json.loads(data_str)['result']
    reply = json.loads(data)[reply_api]
    if reply['success']:
        result = reply
    else:
        result = {}
    return result


def loads_all(s):
    """载入zstack的返回值."""
    if isinstance(s, bytes):
        s = s.decode()

    def _load(_s):
        if isinstance(_s, unicode):
            _s = json.dumps(json.loads(_s))
        t = json.loads(_s)
        # list类型
        if is_collection(t):
            for i, k in enumerate(t):
                if isinstance(k, str) and (k.startswith('{') or k.startswith('[')):
                    t[i] = _load(k)
        elif isinstance(t, dict):
            for k in t:
                if isinstance(t[k], (str, unicode)) and (t[k].startswith('{') or t[k].startswith('[')):
                    t[k] = _load(t[k])
        return t

    return _load(s)

def check_params(session):
    """校验参数."""
    pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    pat = re.compile("^(192.168)|(10.21)|(10.58)\.\d{1,3}\.\d{1,3}$")
    if not pat.match(args.start_ip):
        return True
        print(u'起始主机IP非法')
        return False

    if args.num > 24:
        print('超过一个机柜最大数量限制')
        return False

    if not query_cluster(args.cluster_uuid, session):
        print('查无此集群信息')
        return False
    if args.env not in ('p', 's', 't'):
        print('环境输入错误')
        return False

    if args.zone not in ('hz', 'sh', 'dev'):
        print('区域输入错误')
        return False
    return True


def query_cluster(uuid, session):
    """Query cluster by uuid."""
    data_head = 'org.zstack.header.cluster.APIQueryClusterMsg'
    body = {
        data_head: {
            "conditions": [
                {
                    "name": "uuid",
                    "op": "=",
                    "value": uuid
                }
            ],
            "session": session
        }
    }
    r = requests.post(uri, json=body)
    if r.status_code == 200:
        results = resolve_resp_list(data_head, r.text)
        return True if results and results[0] else False
    else:
        return False


def install_host(session, params):
    """Install host."""
    start_ip = params.start_ip
    pre_pos = '.'.join(start_ip.split('.')[0:2])
    net_pos = start_ip.split('.')[2]
    end_pos = start_ip.split('.')[3]
    net_pos = int(net_pos)
    end_pos = int(end_pos)
    num = params.num
    cluster_uuid = params.cluster_uuid
    env = params.env
    zone = params.zone
    data_head = "org.zstack.kvm.APIAddKVMHostMsg"
    host = {
        "username": "tdops",
        "password": "TC+P5V+k8uie+Zyk",
        "name": "kvm-{}-{:0>3d}{:0>3d}.{}.td".format(env, net_pos, end_pos, zone),
        "description": "",
        "clusterUuid": cluster_uuid,
        "managementIp": start_ip,
        "session": session
    }
    body = {
        data_head: host
    }

    for i in range(end_pos, end_pos + num):
        ip = '{}.{}.{}'.format(pre_pos, net_pos, i)
        name = "kvm-{}-{:0>3d}{:0>3d}.{}.td".format(env, net_pos, i, zone)
        host['name'] = name
        host['managementIp'] = ip
        r = requests.post(uri, json=body)
        resp = loads_all(r.text)
        print('----------' * 10)
        print(u'第{}台机器ip:{}, name:{}'.format((i + 1 - end_pos), ip, name))
        print(u'返回结果状态为:{}'.format(r.status_code), u'返回结果为:{}'.format(resp))
        print('\n')


def main():
    """Main."""
    login_body = {"org.zstack.header.identity.APILogInByAccountMsg": {
        "accountName": "admin",
        "password": "540ae1bf0fd912d7f4db2fad48fa4396679a06b3d3ceead77832e831a0361f9a58f512a0a7dfa60bbbf6d82656411196b57dfc3014b5a069054e6c64e89b16d7",
        # "password": "b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86",
        "session": {
            "uuid": "ac28cdef1dee4d3abf066bc6dc4b1149"
        }
    }
    }
    r = requests.post(uri, json=login_body)
    print(r.content)
    if r.status_code == 200:
        resp = loads_all(r.text)
        d = resp.get("result").get("org.zstack.header.identity.APILogInReply")
        if d["success"]:
            session = {"uuid": d.get("inventory").get("uuid")}
            # 校验参数
            if not check_params(session):
                return False
            install_host(session, args)
        else:
            print("登录失败, {}".format(d))

    else:
        print('登录失败，请重新再试!')


if __name__ == '__main__':
    main()