# -*- coding: utf-8 -*-
u"""多线程爬虫例子."""
import os
import requests

from pathlib import Path

from bs4 import BeautifulSoup


def get_links(url):
    u"""结合 requests 和 bs4 解析出网页中的全部图片链接，返回一个包含全部图片链接的列表."""
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    for img in soup.find_all('div', class_='img-wrap'):
            if img.attrs.get('data-src'):
                yield img.attrs.get('data-src')


def download_link(directory, link):
    u"""把图片下载到本地."""
    img_name = '{}.jpg'.format(os.path.basename(link))
    download_path = directory / img_name
    r = requests.get(link)
    with download_path.open('wb') as fd:
            fd.write(r.content)


def setup_download_dir(directory):
    u"""设置文件夹，文件夹名为传入的 directory 参数，若不存在会自动创建."""
    download_dir = Path(directory)
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir
