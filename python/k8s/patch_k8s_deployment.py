#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Do."""
# @Date    : 2019-01-04 17:24:33
# @Author  : wuyan (msn734506700@live.com)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import json
import re
import subprocess

import copy

lxcfs_volume_mounts = [
              {
                "name": "lxcfs-cpuinfo",
                "mountPath": "/proc/cpuinfo"
              },
              {
                "name": "lxcfs-diskstats",
                "mountPath": "/proc/diskstats"
              },
              {
                "name": "lxcfs-meminfo",
                "mountPath": "/proc/meminfo"
              },
              {
                "name": "lxcfs-stat",
                "mountPath": "/proc/stat"
              },
              {
                "name": "lxcfs-swaps",
                "mountPath": "/proc/swaps"
              },
              {
                "name": "lxcfs-uptime",
                "mountPath": "/proc/uptime"
              }
            ]

lxcfs_volume = [
{
            "name": "lxcfs-cpuinfo",
            "hostPath": {
              "path": "/var/lib/lxcfs-cpuinfo/cpuinfo{}",
              "type": ""
            }
          },
          {
            "name": "lxcfs-diskstats",
            "hostPath": {
              "path": "/var/lib/lxcfs/proc/diskstats",
              "type": ""
            }
          },
          {
            "name": "lxcfs-meminfo",
            "hostPath": {
              "path": "/var/lib/lxcfs/proc/meminfo",
              "type": ""
            }
          },
          {
            "name": "lxcfs-stat",
            "hostPath": {
              "path": "/var/lib/lxcfs/proc/stat",
              "type": ""
            }
          },
          {
            "name": "lxcfs-swaps",
            "hostPath": {
              "path": "/var/lib/lxcfs/proc/swaps",
              "type": ""
            }
          },
          {
            "name": "lxcfs-uptime",
            "hostPath": {
              "path": "/var/lib/lxcfs/proc/uptime",
              "type": ""
            }
          }
]


class Deployment(object):

    def __init__(self):
        self.patch_list = []
        self.namespace = ""
        self.name = ""
        self.json = ""
        self.cpu = 0
        self.spec = None

    def load_json(self, s):
        try:
            j = json.loads(s)
            self.name = j.get('metadata', {}).get('name')
            self.namespace = j.get('metadata', {}).get('namespace')
            self.json = j
            self.cpu = j.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])[0].get('resources', {}).get('limits', {}).get('cpu', 0)
            self.spec = j.get('spec')
        except Exception as e:
            print('解析字符串出现问题，请检查，之后再试', e)

    def patch_deployment_lxcfs_volume(self):
        self.add_lxcfs()

        command = "kubectl patch deployment {} --type json --patch '{}' -n {}".format(self.name, json.dumps(self.patch_list), self.namespace)
        # print(command)
        return_code = subprocess.call(command, shell=True)
        if return_code != 0:
            return False
        return True

    def add_lxcfs(self):
        volume_mounts_op = {
                "op": "replace",
                "path": "/spec/template/spec/containers/0/volumeMounts",
                "value": [
                    {
                        "mountPath": "/.containers",
                        "name": "homer-logdir"
                    }
                ]
            }
        volume_op = {
                "op": "replace",
                "path": "/spec/template/spec/volumes",
                "value": [
                    {
                        "hostPath": {
                            "path": "/var/log/containers",
                            "type": ""
                        },
                        "name": "homer-logdir"
                    }
                ]
        }

        spec = self.spec.get('template', {}).get('spec', {})
        volume_mounts = spec['containers'][0].get('volumeMounts', [])
        volumes = spec.get('volumes', [])

        lxcfs_volume_cp = copy.deepcopy(lxcfs_volume)
        lxcfs_volume_mounts_cp = copy.deepcopy(lxcfs_volume_mounts)

        host_path = lxcfs_volume_cp[0].get('hostPath')
        cpu_path_info = host_path.get('path').format(self.cpu)
        host_path['path'] = cpu_path_info

        lxcfs_volume_cp.extend(volumes)
        lxcfs_volume_mounts_cp.extend(volume_mounts)

        volume_mounts_op["value"] = lxcfs_volume_mounts_cp
        volume_op["value"] = lxcfs_volume_cp
        self.patch_list = [volume_mounts_op, volume_op]
        self.patch_list = [volume_mounts_op, volume_op]

    def get_dep_json(self):
        cmd = 'kubectl get deployment/{} -o json -n {}'.format(self.name, self.namespace)
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        result, _ = res.communicate()
        return result


class Do(object):
    def __init__(self):
        self.dps = []
        self.success = []
        self.failed = []

    def get_dps_list(self):
        cmd = 'kubectl get deployment --all-namespaces=true'
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        result = res.stdout.readlines()
        for i, r in enumerate(result):
            if i == 0:
                continue
            line = re.split('[ ]+', r)
            d = Deployment()
            d.namespace = line[0]
            d.name = line[1]
            self.dps.append(d)

    def action(self):
        for d in self.dps:
            s = d.get_dep_json()
            d.load_json(s)
            r = d.patch_deployment_lxcfs_volume()
            if r:
                self.success.append(d)
            else:
                self.failed.append(d)

    def print_f(self):
        if len(self.failed) > 0:
            for f in self.failed:
                print('\n')
                print('-' * 20)
                print(json.dumps(f.json, ensure_ascii=False, indent=4))
                print('\n')
                print('\n')

if __name__ == '__main__':
    do = Do()
    do.get_dps_list()
    do.action()
    do.print_f()

