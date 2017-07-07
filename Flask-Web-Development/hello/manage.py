#!/usr/bin/env python
#-*- coding: utf-8 -*-
#顶级文件夹中的manage.py文件用于启动程序
#先赋予其可执行权限：chmod u+x manage.py
#直接执行./manage.py runserver 执行脚本启动服务器

import os
from app import create_app, db
from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context = make_shell_context))
manager.add_command('db', MigrateCommand)

#为了运行单元测试，可以在manager.py脚本中添加一个自定义命令
#然后执行python manage.py test即可运行单元测试

#manager.command修饰器让自定义命令变得简单
#修饰函数名就是命令名，函数的文档字符串会显示在帮助消息中
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()

