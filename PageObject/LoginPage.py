#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import threading
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


lock = threading.Lock()
dict_list = ['15143504986:Ab1111', '17099439121:lili789xiang',
             '17099439110:jessie689', '18939824530:baobao68028665',
             '17099439171:776788', '13630759454:jianxun890',
             '17099438995:maple258', '13269093824:jianxun2017']


def login():
    global dict_list
    # 进程锁，设置全局变量，多进程执行时，都从全局变量中获取数据
    lock.acquire()
    random_list = dict_list[random.randint(0, len(dict_list)) - 1]
    # 避免取出账号重复
    dict_list.remove(random_list)
    username = random_list.split(":")[0]
    password = random_list.split(":")[1]
    page = LoginPage()
    page.input_username(username)
    page.input_password(password)
    page.login_click()
    lock.release()


if __name__ == '__main__':
    login()