#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

from Public.BasePage import BasePage
from Public.Decorator import *
from uiautomator2 import UiObjectNotFoundError


class LoginPage(BasePage):
    @teststep
    def wait_page(self, get_text):
        try:
            if self.d(text='%s' % get_text).wait(timeout=10):
                return True
            else:
                return False
        except Exception:
            raise Exception('Not in LoginPage')

    @teststep
    def input_username(self, text):
        self.d(resourceId="com.lietou.mishu:id/username") \
            .set_text(text)

    @teststep
    def input_password(self, text):
        self.d(resourceId="com.lietou.mishu:id/password") \
            .set_text(text)

    @teststep
    def login_click(self):
        self.d(resourceId='com.lietou.mishu:id/login').click()

    @teststep
    def logout(self):
        self.d(text="我的").click()
        self.swipe_up()
        self.d(text="设置").click()
        self.d(text="退出登录").click()


def login():
    dict_list = [{'15134670784': 'xh1234567'}, {'15134663409': 'yunyun123'}, {'13846644342': 'huihui809'},
                 {'13846630749': 'weiwei123'}, {'14702868363': '1234565'}, {'13624586924': 'jhst67890'},
                 {'13059833467': 'zhangzhang123'}, {'15201351540': 'wu123456'}, {'18518378462': 'lyb007150'}]
    num_list = dict_list[random.randint(0, len(dict_list)) - 1]
    username = list(num_list.keys())[0]
    password = list(num_list.values())[0]
    page = LoginPage()
    page.input_username(username)
    page.input_password(password)
    page.login_click()


if __name__ == '__main__':
    login()