#-*- coding: utf-8 -*-
import unittest
from flask import current_app
from app import create_app, db

class BasicsTestCase(unittest.TestCase):
    #setUp在测试前执行
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    #tearDown在测试后执行
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    #测试函数以test_开头
    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_testing(self):
        self.assertTrue(current_app.config['TESTING'])

