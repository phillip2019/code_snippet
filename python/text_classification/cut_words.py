#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

# 对训练集 测试集文本都进行切词处理，对测试集数据打上主题标签
# 保存至文件
import os
import jieba


def save_file(save_path, content):
    with open(save_path, 'a', encoding='utf-8', errors='ignore') as fp:
        fp.write(content)


# 读取文件
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.readlines()
    return str(content)


# 抽取测试的主题关键词
def extract_theme(content):
    themes = []
    tags = jieba.analyse.extract_tags(content, topK=3, withWeight=True, allowPOS=('n', 'ns', 'v', 'vn'), withFlag=True)
    for i in tags:
        themes.append(i[0].word)
    return str(themes)


def cast_words(origin_path, save_path, theme_tag):
    """
    :param origin_path:  原始文本路径
    :param save_path: 切词后文本路径
    :param theme_tag: 标签主题
    :return:
    """
    # 原文档所在路径
    file_lists = os.listdir(origin_path)

    for dir_1 in file_lists:
        # 原始文件路径
        file_path = os.path.join(origin_path, dir_1)
        # 切词后文件路径
        seg_path = os.path.join(save_path, dir_1)

        if not os.path.exists(seg_path):
            os.makedirs(seg_path)

        detail_paths = os.listdir(file_path)
        # 找到文件夹下具体文件路径
        for detail_path in detail_paths:
            full_path = os.path.join(file_path, detail_path)
            file_content = read_file(full_path)
            file_content = file_content.strip()

            # 删除换行
            # file_content = file_content.replace('\r\n', ' ')
            file_content = file_content.replace("\r", '')\
                                    .replace('\n', '') \
                                    .replace(r'\u3000', '') \
                                    .replace(r'& nbsp', '') \
                                    .replace("\'", "") \
                                    .replace('')
            # 为文件内容分词
            content_seg = jieba.cut(file_content)

            if theme_tag is not None:
                print('文件路径: {}'.format(os.path.join(theme_tag, detail_path)))
                # theme为该文章主题关键词
                theme = extract_theme(' '.join(content_seg))
                print('文章主题关键词: {}'.format(theme))
                # 将训练集文章的主题关键词保存到标签存储路径
                save_path(os.path.join(theme_tag, detail_path), theme)

            # 将处理后的文件保存到分词后语料目录
            save_path(os.path.join(seg_path, detail_path, ' '.join(content_seg)))


if __name__ == '__main__':
    # 对训练集进行分词
    train_words_path = 'train_words'
    train_save_path = 'train_segments'
    cast_words(train_words_path, train_save_path, theme_tag=None)

    # 对测试集进行分词，抽取文章主题标签
    test_words_path = 'test_words'
    test_save_path = 'test_segments'
    # 存放测试集文章主题标签路径
    theme_tag_path = 'theme_tag'
    cast_words(test_words_path, test_save_path, theme_tag=theme_tag_path)
