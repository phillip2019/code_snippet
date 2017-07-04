#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Do."""
# @Date : 2017-06-19 18:58:33
# @Author  : wuyan (msn734506700@live.com)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# import os
from datetime import datetime

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
# from tornado.concurrent import Future
from tornado import gen, httpclient


define("port", default=8000, help="run on the given port", type=int)


@gen.coroutine
def get_url(url):
    """Download the page at `url` and parse it for links.

    Returned links have had the fragment after `#` removed, and have been made
    absolute so, e.g. the URL 'gen.html#tornado.gen.coroutine' becomes
    'http://www.tornadoweb.org/en/stable/gen.html'.
    """
    try:
        print('Request date:{} url:{}'.format(datetime.now(), url))
        response = yield httpclient.AsyncHTTPClient().fetch(url)
        print('fetched %s' % url)

        html = response.body if isinstance(response.body, str) \
            else response.body.decode()
        print('Response date:{}, html:{}'.format(datetime.now(), html))
    except Exception as e:
        print('Exception: %s %s' % (e, url))
        raise gen.Return([])


# @gen.coroutine
# def main(count):
#     """Count.

#     [description]

#     Args:
#         count: [description]
#     """
#     url = 'http://127.0.0.1:5000/'
#     for _ in range(count):
#         r = get_url(url)


class IndexHandler(tornado.web.RequestHandler):
    """Index Handler."""

    def get(self):
        """Get."""
        start_time = datetime.now()
        greeting = self.get_argument('greeting', 'Hello')
        # main(3)
        # futures = [yield get_url(url) for _ in range(3)]
        # for f in futures:
        #     yield f
        url = 'http://127.0.0.1:5000/'
        for _ in range(3):
            get_url(url)
        print('Total time:{}'.format(datetime.now() - start_time))
        self.write(greeting + ', friendly user!')


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
