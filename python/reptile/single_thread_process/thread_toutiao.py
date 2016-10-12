# -*- coding: utf-8 -*-
u"""多线程爬虫例子."""
from queue import Queue
from threading import Thread
from time import time
from itertools import chain

from download import setup_download_dir, get_links, download_link


class DownloadWorker(Thread):
    u"""多任务下载."""

    def __init__(self, queue):
        """__init__."""
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        """Run body."""
        while True:
            # Get the work from the queue and expand the tuple
            item = self.queue.get()
            if item is None:
                break
            directory, link = item
            download_link(directory, link)
            self.queue.task_done()


def main():
    u"""执行入口."""
    ts = time()

    url1 = 'http://www.toutiao.com/a6333981316853907714'
    url2 = 'http://www.toutiao.com/a6334459308533350658'
    url3 = 'http://www.toutiao.com/a6313664289211924737'
    url4 = 'http://www.toutiao.com/a6334337170774458625'
    url5 = 'http://www.toutiao.com/a6334486705982996738'
    download_dir = setup_download_dir('thread_imgs_32')
    # Create a queue to communicate with the worker threads
    queue = Queue()

    links = list(chain(
        get_links(url1),
        get_links(url2),
        get_links(url3),
        get_links(url4),
        get_links(url5),
    ))

    # Create 8 worker threads
    for x in range(8):
        worker = DownloadWorker(queue)
        # Setting daemon to True will let the main thread exit even though the
        # workers are blocking
        worker.daemon = True
        worker.start()

    # Put the tasks into the queue as a tuple
    for link in links:
        queue.put((download_dir, link))

    # Causes the main thread to wait for the queue to finish processing all
    # the tasks
    queue.join()
    print(u'一共下载了 {} 张图片'.format(len(links)))
    print(u'Took {}s'.format(time() - ts))


if __name__ == '__main__':
    main()

"""
一共下载了 253 张图片
Took 57.710124015808105s
"""
