# -*- coding: utf-8 -*-
u"""多进程爬虫例子."""
from functools import partial
from multiprocessing.pool import Pool
from itertools import chain
from time import time

from download import setup_download_dir, get_links, download_link


def main():
    """main."""
    ts = time()

    url1 = 'http://www.toutiao.com/a6333981316853907714'
    url2 = 'http://www.toutiao.com/a6334459308533350658'
    url3 = 'http://www.toutiao.com/a6313664289211924737'
    url4 = 'http://www.toutiao.com/a6334337170774458625'
    url5 = 'http://www.toutiao.com/a6334486705982996738'
    download_dir = setup_download_dir('process_imgs')
    links = list(chain(
        get_links(url1),
        get_links(url2),
        get_links(url3),
        get_links(url4),
        get_links(url5),
    ))

    download = partial(download_link, download_dir)
    with Pool(8) as p:
        p.map(download, links)
    print(u'一共下载了 {} 张图片'.format(len(links)))
    print(u'Took {}s'.format(time() - ts))

if __name__ == '__main__':
    main()
"""
一共下载了 253 张图片
Took 58.69389724731445s
"""
