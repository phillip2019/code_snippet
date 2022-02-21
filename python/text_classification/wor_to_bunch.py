#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import pickle
import time
from sklearn.datasets.base import Bunch

'''
label: 文章类型
filepath: 文章路径
contents:  分词后的文章
'''
def read_file(file_path):
    """
    :param file_path: 文章路径
    :return:
    """
    with open(file_path, "r", encoding= 'utf-8',errors='ignore') as fp:
        content = fp.readlines()
    return str(content)


def word_to_bunch(train_save_path, train_bunch_path):
    bunch = Bunch(label=[], filepath=[], contents=[])
    all_labels = os.listdir(train_save_path)

    for label in all_labels:
        detail_path = train_save_path + label + '/'

        all_details = os.listdir(detail_path)

        for all_detail in all_details:
            file_detail_path = detail_path + all_detail     # 文件具体路径
            bunch.label.append(label)                       #文章类型
            # print(bunch.label)
            bunch.filepath.append(file_detail_path)         #文章所在路径
            # print(bunch.filepath)
            contents = read_file(file_detail_path)
            # print(contents)                               #文章内容
            bunch.contents.append(contents)
            # print(bunch.contents)   #

    with open(train_bunch_path, "wb+") as fp:
         pickle.dump(bunch, fp)
    print("创建完成")


if __name__ == "__main__":
    # 对训练集进行分词
    train_save_path = './train_segments/'
    train_bunch_path = "train_bunch_bag.dat"
    word_to_bunch(train_save_path, train_bunch_path)
    # 对测试集进行分词，抽取文章主题标签
    test_save_path = './test_segments/'
    test_bunch_path = "test_bunch_bag.dat"
    word_to_bunch(test_save_path, test_bunch_path)