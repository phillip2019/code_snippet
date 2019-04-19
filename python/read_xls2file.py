#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Do."""
# @Date    : 2019-04-15 13:36:56
# @Author  : wuyan (msn734506700@live.com)
# @Version : V0.1

import pandas as pd
import base64
import re
import argparse

parser = argprse.ArgumentParser(description='Process Java enum file.')
parser.add_argument('-sf', '--src_file', metavar='source file', type=str, dest='sf', nargs=1,
                    required=True, help='source java file for the translate.')

parser.add_argument('-dcf', '--dict_file', metavar='excel dictionary file', type=str, dest='dcf',
                    required=True, nargs=1, action='store', help='excel dictionary file, must full path.')

parser.add_argument('-df', '--dest_file', metavar='destination file', type=str, dest='df', nargs=1,
                    required=True, help='destination file for the translate.')

parser.add_argument("-v", "--version", action='version', version='%(prog)s 1.0')

args = parser.parse_args()

# SUCCESS(0, "成功"),
# AUTH_FAILED(-2, "授权获取失败"),
RE_PATTERN = re.compile('[ ]*([A-Z_]+)\(([-\d]+),[ ]*"([\u4E00-\u9FFF\w\W]+)"\),')


def read_file2format(filename, codes_d):
    java_code_dict = []
    with open(filename, encoding='UTF-8') as f:
        for line in f:
            if line.strip() and not any(line.strip().startswith(e) for e in ['/', '*']):
                line_code = line.strip()
                # t = re.match('/[/(/)]/', line_code)
                # tmp = line_code.replace('(', ',').replace(')', ',')
                # tmp = tmp.split(',')
                match_groups = re.match(RE_PATTERN, line_code)
                symbol, code, msg_zh = match_groups
                msg_zh = msg_zh.replace('"', '').strip()
                msg = codes_d.get(hash_code_msg_zh(code, msg_zh))
                line = '{}({}, "{}", "{}"),\n'.format(symbol, code, msg, msg_zh)
            java_code_dict.append(line)
    return java_code_dict


def read_xlsx(filename):
    ex = pd.read_excel(filename, sheet_name=u'工作表 1 - codes', index_col=False)
    data = pd.DataFrame(ex)
    codes_dict = {}
    for d in data.itertuples(name="RowData"):
        # print(d[0], d[1], d[2], d[3], d[4], d[5])
        if d[1] != 'code':
            key = hash_code_msg_zh(d[1], d[2])
            codes_dict[key] = d[5]
    return codes_dict


def write2file(filename, data):
    with open(filename, encoding='utf-8', mode='w+') as f:
        for d in data:
            f.writelines(d)
    print('success')


def hash_code_msg_zh(code, msg):
    return str(code) + msg


def main():
    # java文件路径
    # '/Users/xiaowei.song/Desktop/t.java'
    sf = args.sf
    # 字典路径
    # '/Users/xiaowei.song/资料/tongdun/爬虫/授权爬取codes  message_MC.xlsx'
    dict_file = args.dcf
    # 生成文件路径
    # '/Users/xiaowei.song/Desktop/t'
    df = args.sf

    code_dict_data = read_xlsx(dict_file)
    fmt_str = read_file2format(sf, code_dict_data)
    write2file(df, fmt_str)


if __name__ == '__main__':
    main()
