#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-19 09:43:55
# @Author  : wuyan
# @Version : V0.1

import os
import time
import datetime

import threading
import concurrent
from concurrent.futures import ThreadPoolExecutor
import logging
from logging import handlers

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

url = 'mysql+pymysql://root:123456@192.168.6.84:3306/nimitz'
# url = 'mysql+pymysql://root:123456@127.0.0.1:3306/nimitz'
engine = create_engine(url, pool_recycle=20, pool_size=10, pool_timeout=30)

query = 'SELECT NOW();'

session_factory = sessionmaker(bind=engine)

logging.basicConfig()


class MyFormatter(logging.Formatter):
    converter = datetime.datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            t = ct.strftime(datefmt)
            s = "%s.%03d" % (t, record.msecs)
            return s

LOG_MAX = 1024 * 1024 * 10  # 10M
BACKUP_COUNT = 5
log_dir = os.path.join(os.path.expanduser('~'), 'output/nimitz')
log_format = MyFormatter('%(asctime)s %(filename)s:%(lineno)d %(levelname)s %(message)s',
                         '%m-%d %H:%M:%S')

handler = handlers.RotatingFileHandler(os.path.join(log_dir, 'log.log'), 
    maxBytes=LOG_MAX, 
    backupCount=BACKUP_COUNT)
handler.setFormatter(log_format)
logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
# session = engine
session2 = scoped_session(session_factory)
session2.execute('SET @@global.wait_timeout=10')
# session2.execute('SET @@session.wait_timeout=10')
# session2.execute('SET @@global.max_connections=17')


def thread_fun():
    try:
        t = threading.current_thread()
        session = scoped_session(session_factory)
        # logger.info(dir(session.connection()))
        logger.info("thread ID {}, session ID {}".format(id(t), id(session)))
        logger.info('Q1 {}'.format(session.execute(query).fetchall()))
        # session.commit()
        time.sleep(4)
    except Exception:
        logger.error('Q1', exc_info=True)
        session and session.rollback()
    else:
        pass

    result = None
    try:
        result = session.execute(query).fetchall()
        logger.info("thread ID {}, session ID {}".format(id(t), id(session)))
    except Exception:
        logger.error('Q2', exc_info=True)
    else:
        session and session.rollback()
        logger.info('Q2 {}'.format(result))


if __name__ == '__main__':
    pool = ThreadPoolExecutor(15)
    exectors = []
    for i in xrange(45):
        t = pool.submit(thread_fun)
        exectors.append(t)

    for future in concurrent.futures.as_completed(exectors):
        print(future)

    print(dir(session2))
    print(session2.is_active)
    session2.execute('SET @@global.wait_timeout=28800')
    session2.execute('SET @@global.max_connections=151')
    # session2.commit()
    # session2.remove()
    print('begin %s' % session2.is_active)
    session2.rollback()
    time.sleep(15)
    print('end %s' % session2.is_active)
    print(session2.execute(query).fetchall())

# while False:
#     session.execute('SET wait_timeout=3')
#     print('Q1', session.execute(query).fetchall())
#     print(id(session))
#     session.commit()
#     time.sleep(3)
#     print(id(session))
#     print('Q2', session.execute(query).fetchall())
