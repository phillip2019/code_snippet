#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-09 09:28:57
# @Author  : wuyan

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# import os
import time
from random import randint

from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask('app')

db = SQLAlchemy()

app.config.update(
    SQLALCHEMY_DATABASE_URI='sqlite:////tmp/test.db',
    CELERY_BROKER_URL='redis://10.57.2.108:6379/0',
    CELERY_RESULT_BACKEND='redis://10.57.2.108:6379/1',
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['pickle', 'json', 'msgpack', 'yaml'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
)

db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


def make_celery(app):
    celery = Celery(app.import_name,
                    backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


celery = make_celery(app)


@celery.task(name='app.add_together')
def add_together(a, b):
    return a + b


THOUSAND = 1000


def add_task(x):
    while True:
        print("I am working")
        time.sleep(1)
        add_together.delay(randint(0, THOUSAND), randint(0, THOUSAND))
        print("I am working end!")


@app.route("/")
def test():
    add_together.delay(randint(0, THOUSAND), randint(0, THOUSAND))


if __name__ == '__main__':
    # app.run()
    pass
