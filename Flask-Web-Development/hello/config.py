#-*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

#基础配置
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <xumenger@126.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass

#开发环境配置
class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'stmp.126.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or  \
                    'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

#测试环境配置
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or  \
                    'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

##生产环境配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or  \
                    'sqlite:///' + os.path.join(basedir, 'data.sqlite')

#config字典中配置了不同的配置环境，还注册了一个默认配置
config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        
        'default': DevelopmentConfig}
