#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Do."""
# @Date    : 2018-02-16 08:14:36
# @Author  : wuyan (msn734506700@live.com)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# import os
import itchat
import time

itchat.auto_login(True)

SINCERE_WISH = u'🎉🎉🎉新年到，宋小韦给{}及您家人拜年啦！祝新春快乐，万事如意，财源滚滚，身体健康，2018发发发！🐶 年旺旺旺！'

blacklist = [u'火龙果', u'赣南脐橙-招代理18816472208', u'赣南脐橙（寻乌橙）', u'~浪漫☆樱花 🌸', u'任时光（接花呗套现、流量）', u'一周进步-小冰|明天中午12点后拉群',
            u'李杰', u'钟杰', u'郑威', u'钟文杰', u'罗文飞', u'赖哥']

# itchat.send(SINCERE_WISH.format('宋小韦'), 'filehelper')

friendList = itchat.get_friends(update=True)[1:]
for friend in friendList:
#     # print(friend)
#     # 如果是演示目的，把下面的方法改为print即可
    if friend['DisplayName'] not in blacklist:
        pring(friend['DisplayName'])
        print(SINCERE_WISH.format(friend['DisplayName'] and friend['NickName']), friend['UserName'])
        # itchat.send(SINCERE_WISH.format(friend['DisplayName'] and friend['NickName']), friend['UserName'])
#     print(friend.get('NickName'))
#     # print(SINCERE_WISH.format(friend['DisplayName'] or friend['NickName']), friend['UserName'], friend.get('Signature'), friend.get('NickName'))
    time.sleep(.5)
itchat.auto_login(hotReload=True)

