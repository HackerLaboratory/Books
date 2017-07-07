# -*- coding: utf-8 -*-
#程序包用来保存程序中的所有代码、模板和静态文件

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

'''
在单个文件中开发程序很方便，但却有一个很大的缺点，因为程序在全局作用域中创建，所以无法动态修改配置
运行脚本时，程序示例已经创建，再修改配置为时已晚
这一点对于单元测试尤为重要，因为有时为了提高测试覆盖度，必须在不同的配置环境中运行程序

这个问题的解决方法是延迟创建程序实例，把创建过程移到可显式调用的工厂函数中
这种方法不仅可以给脚本留出配置程序的时间，还能够创建多个程序实例，这些实例有时在测试中非常有用
程序的工厂函数在app包的构造文件中定义

构造文件导入了大多数正在使用的Flask扩展
由于尚未初始化所需的程序实例，所以没有初始化扩展，创建扩展类时没有向构造函数传入参数
creata_app函数就是程序的工厂函数，接受一个参数，是程序使用的配置名
配置类在config.py中定义，其中保存的配置可以使用Flask app.config配置对象提供的from_object方法直接导入程序
至于配置对象，则可以通过名字从config字典中选择
程序创建并配置好之后，就能初始化扩展了
'''
def create_app(config_name):
    app = Flask(__name__)
    #根据config.py中配置初始化Flask
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    #蓝本在工厂函数create_app中注册到程序上
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

