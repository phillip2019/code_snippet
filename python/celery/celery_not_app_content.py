#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Do."""
# @Date    : 2017-06-21 13:37:10
# @Author  : wuyan (msn734506700@live.com)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# import os

from celery import Celery
from celery.app.log import Logging

from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import (SQLAlchemy)
import logging
# from logging import getLogger


def create_db():
    """DB Factory."""
    return SQLAlchemy()


celery = Celery('tasks')
db = SQLAlchemy()


@celery.task
def beat_query():
    """Beat."""
    # logger = getLogger(__name__)
    with app.app_context():
        print('1111')
        logger('2222')
        result = db.session.execute('select count(1) from user')
        logger.info(result)
    return 255


def create_app():
    """App Factory."""
    app = Flask('app')
    app.config.update({
        'SQLALCHEMY_DATABASE_URI':
        'mysql://root:123456@localhost/test?charset=utf8',
        'DEBUG': True,
        'BROKER_URL': 'redis://localhost:6379',
        'CELERY_TIMEZONE': 'Asia/Shanghai',
        'CELERY_ENABLE_UTC': True,
        'CELERY_IMPORTS': ('celery_not_app_content',),
        'CELERYBEAT_SCHEDULE': {
            'beat_query': {
                'task': 'celery_not_app_content.beat_query',
                'schedule': timedelta(seconds=10),
                'args': (),
            }
        }})
    # CELERY_IMPORTS = ("tasks",)})
    celery.conf.update(app.config)
    Logging._setup = False
    db = create_db()
    db.init_app(app)
    handler = logging.handlers.TimedRotatingFileHandler('flask.log', when='d',
                                                        backupCount=7)
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - '
        '%(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    return app


app = create_app()
logger = app.logger
logger.info('hello world')

if __name__ == '__main__':
    app.run(debug=True)
