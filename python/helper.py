#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-12 09:24:35
# @Author  : wuyan
# @Version : V0.1
"""帮助模块，提供一些算法，数据抽取方式."""

import os
import logging
import re
import random
import string
# import shutil
import subprocess

# from datetime import datetime


def parser(relation_list):
    """
    抽取依赖数据，返回依赖顺序列表.

    Args:
        relation_list: 格式化依赖数据列表，eg： [('A', 'C'), ('A', 'D'), ('A', 'G')】
                       释义为：A -> C, A -> D, A -> G

    Returns:
        list: 顺序依赖列表元组，eg： [('A',), ('D',), ('B',), ('G', 'C'), ('F',)]
    """
    logging.info('Begin parser table relation!')
    result = []
    pre_elements = set()
    for e0, e1 in relation_list:
        pre_elements.add(e0)
        pre_elements.add(e1)
    while relation_list:
        elements_right = set()
        for _, e1 in relation_list:
            elements_right.add(e1)

        elements_left = pre_elements - elements_right
        next_list = []
        for i, e in enumerate(relation_list):
            if not e[0] in elements_left:
                next_list.append(e)
        relation_list = next_list
        pre_elements = pre_elements - elements_left
        result.append(tuple(elements_left))
    logging.info('End parser table relation!')
    return result


def random_string(length=10, repeat=True, type_=1):
    """生成随机字符串.

    Args:
        length: 10 生成字符串的长度
        repeat: True 是否能重复
        type_: 1 全部小写字母组成
               2 全部大写字母组成
               3 全部数字字符组成
               12 1和2组成
               23 2和3组成
               13 1和3组成
               123 1和2和3

    Returns:
        string: 返回生成的字符串
    """
    string_letters = string.printable
    if type_ == 1:
        string_letters = string.ascii_lowercase
    elif type_ == 2:
        string_letters = string.ascii_uppercase
    elif type_ == 3:
        string_letters = string.digits
    elif type_ == 12:
        string_letters = string.ascii_letters
    elif type_ == 13:
        string_letters = ''.join([string.ascii_lowercase, string.digits])
    elif type_ == 23:
        string_letters = ''.join([string.ascii_uppercase, string.digits])
    elif type_ == 123:
        string_letters = ''.join([string.ascii_letters, string.digits])

    if repeat:
        strings = ''.join(random.sample(string_letters, length))
    else:
        strings = ''.join(
            [random.choice(string_letters) for i in range(length)])
    return strings


def prepare_data(abs_path, abs_file):
    """
    文件数据预处理.
    3.遍历文件，将tables及依赖数据清洗出来
    4.将ddl语句按照table_name.sql文件名存储在save_path下
    5.返回tables_relation、tables_name, save_path, dml dict

    Futures：
        读取table data行数，并记录之，为多线程执行insert sql做准备。
    """
    logging.info('Begin prepare data!')
    dml_begin_re = r'^DROP TABLE IF EXISTS `(.*)`;$'
    dml_end_re = r"^\) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='.*';$"
    dml_ref_re = r".*CONSTRAINT `.*` FOREIGN KEY .* REFERENCES `(.*)` .*"
    ddl_begin_re = r'^LOCK TABLES `(.*)` WRITE;$'
    ddl_end_re = r'UNLOCK TABLES;'
    dml = {}    # 存储dml代码
    tables_relation = []
    tables_name = []
    is_ddl, is_dml = False, False
    with open(abs_file, 'r') as f:
        dml_buffer = []
        dml_f = open(os.path.join(abs_path, 'dml.sql'), 'wt')
        for line in f:
            if re.match(dml_begin_re, line):
                is_dml, is_ddl = True, False
                # dml_buffer.append(line) # 避免写入两次
                # dml_f.write(line)
                table_name = re.match(dml_begin_re, line).group(1)
                tables_name.append(table_name)
            elif is_dml and re.match(dml_end_re, line):
                is_dml, is_ddl = False, False
                dml_buffer.append(line)
                dml_f.write(line)
                dml[table_name] = r'\n'.join(dml_buffer)
                dml_buffer = []
            elif re.match(ddl_begin_re, line):
                is_dml, is_ddl = False, True
                ddl_f = open(os.path.join(abs_path, table_name + '.sql'), 'wt')
                # ddl_f.write(line) # 避免写入两次
                # ddl_f.write(r'\n')
            elif is_ddl and re.match(ddl_end_re, line):
                is_dml, is_ddl = False, False
                ddl_f.write(line)
                # ddl_f.write(r'\n')
                ddl_f.close()

            if is_dml:
                dml_buffer.append(line)
                dml_f.write(line)
                result = re.match(dml_ref_re, line)
                if result:
                    ref_table_name = result.group(1)
                    tables_relation.append((ref_table_name, table_name))
            elif is_ddl:
                ddl_f.write(line)
                # ddl_f.write(r'\n')
        dml_f.close()
    logging.info('End prepare data!')
    return tables_relation, tables_name, abs_path, dml


def run_dml(command_, dml):
    """Run dml create tables."""
    command_ = command_.split(' ')
    command_.append(dml)
    out_bytes = os.system('mysql -uroot -p123456 test1 < /tmp/test/dml.sql')
    print(out_bytes)
    # print(out_bytes.returncode)


if __name__ == '__main__':
    # elements = [('A', 'C'), ('A', 'D'), ('A', 'G'), ('B', 'C'),
                # ('D', 'B'), ('D', 'E'), ('F', 'E'), ('G', 'F'), ('B', 'G')]
    # print(parser(elements))
    dml = r'/tmp/test/dml.sql'
    run_dml('mysql -uroot -p123456 test1 < ', r'/tmp/test/dml.sql')
