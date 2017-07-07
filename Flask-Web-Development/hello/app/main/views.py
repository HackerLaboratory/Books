#-*- coding: utf-8 -*-
'''
蓝本中的程序路由
'''
from flask import render_template, session, redirect, url_for, current_app

from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email

'''
在蓝本中编写视图函数主要有两点不同：
第一，和前面的错误处理程序一样，路由修饰器由蓝本提供
第二，url_for函数的用法不同，之前的用法中url_for的第一个参数是路由的端点名，在程序的路由中，默认为视图函数的名字，比如index视图函数的URL可使用url_for('index')获取

但在蓝本中就不同了，Flask会为蓝本中的全部端点加上一个命名空间，这样就可以在不同的蓝本中使用相同的端点名定义视图函数，而不会产生冲突
命名空间就是蓝本的名字(Blueprint构造函数的第一个参数)，所以视图函数index注册的端点名是main.index，其URL使用url_for('main.index')获取

url_for函数还支持一种简写的端点形式，在蓝本中可以省略蓝本名，例如url_for('.index')
在这种写法中，命名空间就是当前请求所在的蓝本
但跨蓝本的重定向必须使用带有命名空间的端点名
'''
@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New User',
                        'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',
                            form=form, name=session.get('name'),
                            known=session.get('known', False))

