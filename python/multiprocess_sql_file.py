#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-11 20:00:19
# @Author  : wuyan
# @Version : V0.1

import os
import logging
import shutil
import subprocess
from datetime import datetime
from helper import prepare_data, parser, random_string


temp_dir = r'/tmp'
file_name = r'/Users/xiaowei.song/Downloads/mysqldata/201703092245.sql'


def main():
    """
    1./tmp 生成一个随机目录save_path
    2.目标文件的拷贝，在save_path生成一个副本
    """
    # TODO(wuyan)为了开发过程中减少环境的处理，先自动删除生成的目录
    # os.system(r'rm -fr /tmp/test')
    subprocess.run(['rm', '-fr', r'/tmp/test'])

    time_b = datetime.utcnow()
    path = random_string(10, repeat=True, type_=1)

    # TODO(wuyan) 开发过程中，定死目录名，实际release将删除此
    path = 'test'

    abs_path = os.path.join(temp_dir, path)
    abs_file = os.path.join(abs_path, os.path.basename(file_name))
    while os.path.exists(abs_path):
        path = random_string(10, repeat=True, type_=1)
        abs_path = os.path.join(temp_dir, path)

    os.mkdir(abs_path)

    logging.basicConfig(filename=os.path.join(abs_path, 'app.log'),
                        level=logging.INFO,
                        format='%(levelname)s:%(asctime)s:%(message)s')
    logging.info('生成的临时目录为:{}！'.format(abs_path))

    shutil.copy(file_name, abs_file)
    logging.info('拷贝文件副本成功！')
    tables_relation, tables_name, abs_path, dml = prepare_data(abs_path,
                                                               abs_file)

    print(tables_relation)
    print('#' * 40)
    tables_relation = parser(tables_relation)
    time_e = datetime.utcnow()
    print(time_e - time_b)


if __name__ == '__main__':
    main()
    # pass
