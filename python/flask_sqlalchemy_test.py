#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-09 09:28:57
# @Author  : wuyan

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# import os
import time
from contextlib import contextmanager
from random import randint

from celery import Celery
from flask import Flask
from sqlalchemy import (Column, Integer, String, Boolean,
                        DateTime, ForeignKey, Text, SmallInteger)
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from flask_sqlalchemy import SQLAlchemy

app = Flask('app')

db = SQLAlchemy()

app.config.update(
    # SQLALCHEMY_DATABASE_URI='sqlite:////tmp/test.db',
    SQLALCHEMY_DATABASE_URI='mysql://root:123456@192.168.6.84/nimitz?charset=utf8',
    CELERY_BROKER_URL='redis://10.57.2.108:6379/0',
    CELERY_RESULT_BACKEND='redis://10.57.2.108:6379/1',
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['pickle', 'json', 'msgpack', 'yaml'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
)

db.init_app(app)

Base = db.Model


@contextmanager
def session():
    s = scoped_session(sessionmaker(bind=engine))
    s.expire_on_commit = False
    try:
        yield s
    finally:
        global_maker.remove()


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    email = Column(String(200))
    realname = Column(String(200))
    is_admin = Column(Boolean)
    is_block = Column(Boolean)
    md5password = Column(String(200))
    last_login_time = Column(DateTime)
    create_time = Column(DateTime)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.user_id)


class Project(Base):
    __tablename__ = 'project'
    project_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    owner_id = Column(Integer, ForeignKey('user.user_id'))
    version = Column(String(200))
    message = Column(Text)
    create_time = Column(DateTime)
    status = Column(String(20), index=True)
    mode = Column(String(20))  # 发布 / 回滚
    cluster = Column(String(20))
    publish_time = Column(DateTime)
    test_time = Column(DateTime)
    publish_type = Column(SmallInteger)
    project_members = relationship('ProjectMember', backref=__tablename__)
    project_apps = relationship('ProjectApp', backref='project_apps')
    user = relationship('User', foreign_keys=user_id)
    owner = relationship('User', foreign_keys=owner_id)
    batch = Column(SmallInteger)


class ProjectMember(Base):
    __tablename__ = 'project_member'
    project_member_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.project_id'))
    user_id = Column(Integer, ForeignKey('user.user_id'))
    is_developer = Column(SmallInteger)
    is_tester = Column(SmallInteger)
    is_reviewer = Column(SmallInteger)
    user = relationship('User', foreign_keys=user_id)


class AppMember(Base):
    __tablename__ = 'app_member'
    app_member_id = Column(Integer, primary_key=True)
    app_id = Column(Integer, ForeignKey('app.app_id'))
    user_id = Column(Integer, ForeignKey('user.user_id'))
    is_developer = Column(SmallInteger)
    is_tester = Column(SmallInteger)
    is_manager = Column(SmallInteger)
    is_owner = Column(SmallInteger)
    is_pe = Column(SmallInteger)
    user = relationship('User', foreign_keys=user_id)


class App(Base):
    __tablename__ = 'app'
    app_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    principal_id = Column(Integer, ForeignKey('user.user_id'))
    app_name = Column(String(200))
    scm_repo = Column(String(200))
    machine_configure = Column(String(500))
    machine_amount = Column(Integer)
    is_web = Column(Boolean)
    is_publish = Column(Boolean)
    need_public_ip = Column(Boolean)
    need_domain = Column(Boolean)
    default_template = Column(String(100))
    business_template = Column(String(100))
    programming_lang = Column(String(50))
    status = Column(String(20))
    user = relationship('User', foreign_keys=user_id)
    principal = relationship('User', foreign_keys=principal_id)
    script = Column(Text)
    publish_config = Column(Text)
    test_config = Column(Text)


class ProjectApp(Base):
    __tablename__ = 'project_app'
    project_app_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.project_id'))
    app_id = Column(Integer, ForeignKey('app.app_id'))
    branch = Column(String(100))
    zone = Column(String(20))
    status = Column(String(20))
    check_point = Column(String(50))  # 发布时设立检查点
    release_order = Column(SmallInteger)
    publish_template_id = Column(SmallInteger)
    app = relationship('App', foreign_keys=app_id)
    project = relationship('Project', foreign_keys=project_id)


class Release(Base):
    __tablename__ = 'release'
    release_id = Column(Integer, primary_key=True)
    project_app_id = Column(Integer, ForeignKey('project_app.project_app_id'))
    status = Column(String(20))
    create_time = Column(DateTime)
    environment = Column(String(100))
    deployment_id = Column(String(30))
    current_order = Column(SmallInteger)
    image_number = Column(SmallInteger)
    valid = Column(Boolean)
    # publish_plans = relationship('PublishPlan', backref='publish_plan')
    project_app = relationship('ProjectApp', foreign_keys=project_app_id)


class ReleaseNode(Base):
    __tablename__ = 'release_node'
    release_node_id = Column(Integer, primary_key=True)
    release_id = Column(Integer, ForeignKey('release.release_id'))
    id = Column(Integer)
    host = Column(String(15))
    port = Column(String(5))
    identity = Column(String(20))
    password = Column(String(100))
    application = Column(String(100))
    environment = Column(String(100))
    cluster = Column(String(200))
    status = Column(String(20))



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
