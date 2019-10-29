#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uiautomator2 as u2
import time
from Public.BasePage import BasePage
from Public.Decorator import *
from PageObject.HomePage import HomePage
from PageObject import LoginPage
from Public.Drivers import Drivers
from Public.Report import backup_report
from Public.Test_data import get_test_data
import unittest
import os

class DynamicTest(unittest.TestCase, BasePage):
    "动态发布模块"

    @classmethod
    @setupclass
    def setUpClass(cls):
        cls.d.healthcheck()  # check server

    @classmethod
    @teardownclass
    def tearDownClass(cls):
        cls.d.app_stop("com.lietou.mishu")  # restart app
        cls.d.service("uiautomator").stop()

    @setup
    def setUp(self):
        self.d.app_start("com.lietou.mishu")  # restart app

    @teardown
    def tearDown(self):
        self.d.app_stop("com.lietou.mishu")

    # 获取职位数量
    def get_post_num(self):
        self.d(text="职位").click()
        if self.d(text="刷新职位").wait(timeout=5):
            get_version = self.d.device_info['version']
            # 系统版本兼容
            if get_version < '5.1.1':
                d = self.d.xpath(
                    "//android.view.View/android.view.View/../android.view.View/android.widget.TextView")
            else:
                d = self.d.xpath(
                    "//android.view.ViewGroup/android.view.ViewGroup/../android.view.ViewGroup/android.widget.TextView")
            for i in d.all():
                global post_num
                get_name = i.text
                if "已发布" in get_name:
                    post_num = get_name.split("已发布（")[1].split("）")
            self.d(resourceId="com.lietou.mishu:id/recruitment_main").click()
            return int(post_num[0])
        else:
            log.i("跳转 职位异常")
            return 1

    def logout(self):
        if self.d(text="我的").wait(timeout=10):
            self.d(text="我的").click()
            self.swipe_up()
            self.swipe_up()
            self.swipe_up()
            if self.d(text="设置"):
                self.d(text="设置").click()
                self.swipe_up()
                self.swipe_up()
                self.swipe_up()
                self.d(text="退出登录").click()
                self.d(text="退出").click()
            else:
                log.d("未找到")
        else:
            log.d("未找到/已登出")

    @testcase
    def test_a_recommend(self):
        try:
            if self.d(resourceId="com.lietou.mishu:id/v_hidden").wait(timeout=6):
                self.d(resourceId="com.lietou.mishu:id/v_hidden").click()
            else:
                print('正常')
            if self.d(text="您的账号已在其他设备登录，请重新登录").wait(timeout=3):
                time.sleep(5)
                self.d(text="确定").click()
            if LoginPage.LoginPage().wait_page("密码登录"):
                self.d(text="密码登录").click()
                self.d.set_fastinput_ime(True)
                LoginPage.login()
                self.d.set_fastinput_ime(False)
                if self.d(resourceId="com.lietou.mishu:id/iv_to_recruit").wait(timeout=5):
                    self.d(resourceId="com.lietou.mishu:id/iv_to_recruit").click()
                elif self.d(text="我要招人").wait(timeout=3):
                    self.d(text="我要招人").click()
                    self.d(text="完成").click()
                elif self.d(resourceId="com.lietou.mishu:id/iv_close").wait(timeout=3):
                    self.d(resourceId="com.lietou.mishu:id/iv_close").click()
                    if self.d(text="跳过，暂时不想填写").wait(timeout=3):
                        self.d(text="跳过，暂时不想填写").click()
                        if self.d(resourceId="com.lietou.mishu:id/rl_resume_root").wait(timeout=10):
                            self.d(resourceId="com.lietou.mishu:id/iv_to_recruit").click()
            tmp = 0
            # get_num = self.get_post_num()
            if self.d(text="请选择性别").wait(timeout=3):
                self.d(resourceId="com.lietou.mishu:id/select_man").click()
                self.d(text="确认").click()
            while tmp < 3:
                num = 0
                while num < 30:
                    time.sleep(3)
                    get_version = self.d.device_info['version']

                    if self.d(resourceId="com.lietou.mishu:id/user_card").wait(timeout=3):
                        self.d(resourceId="com.lietou.mishu:id/user_card").click()

                    else:
                        if get_version < '5.1.1':
                            if self.d.xpath("//android.widget.ScrollView/android.view.View"
                                            "/android.view.View/android.view.View").wait(timeout=3):
                                self.d.xpath("//android.widget.ScrollView/android.view.View"
                                             "/android.view.View/android.view.View").click()
                        else:
                            if self.d.xpath("//android.widget.ScrollView/android.view.ViewGroup"
                                            "/android.view.ViewGroup/android.view.ViewGroup").wait(timeout=3):
                                self.d.xpath("//android.widget.ScrollView/android.view.ViewGroup"
                                             "/android.view.ViewGroup/android.view.ViewGroup").click()
                    if self.d(text="立即沟通").wait(timeout=5):
                        self.d(text="立即沟通").click()
                        time.sleep(2)
                        get_post_name = self.d(resourceId="com.lietou.mishu:id/tv_talk_position").get_text()
                        self.d(resourceId="com.lietou.mishu:id/rl_multi_and_send").click()
                        if self.d(text="发送职位").wait(timeout=5):
                            self.d(text="发送职位").click()

                            # 存在点击 发送职位时，进入职位详情页的情况
                            if self.d(text="职位介绍").wait(timeout=2):
                                self.d.press("back")
                            # 当职位list增多时，需要考虑弹框显示不全的情况，滑动找控件，只执行5次
                            post_num = 0
                            while post_num < 3:
                                if self.d(text=get_post_name):
                                    self.d(text=get_post_name).click()
                                    self.d(text="确认").click()
                                    self.d(resourceId="com.lietou.mishu:id/rl_input").click()
                                    self.d(resourceId="com.lietou.mishu:id/et_chat").set_text("您好，我们在为知名互联网公司招聘**岗位，工作地点在北京/上海/深圳，觉得您的经历很匹配。如果感兴趣可以点击应聘我发给您的职位，稍后可以详细沟通")
                                    self.d.set_fastinput_ime(False)
                                    self.d(text="发送").click()
                                    break
                                else:
                                    self.d(resourceId="com.lietou.mishu:id/recycler_view").swipe("up")
                                    post_num += 1

                        self.d(resourceId="com.lietou.mishu:id/chat_left_group").click()
                        self.d(resourceId="com.lietou.mishu:id/ib_menu_back").click()
                        self.d.swipe(0.5, 0.8, 0.5, 0.55)
                        num += 1
                    elif self.d(text="继续沟通"):
                        self.d(resourceId="com.lietou.mishu:id/ib_menu_back").click()
                        self.d.swipe(0.5, 0.8, 0.5, 0.55)
                        num += 1
                    elif self.d(text="该简历设置了隐私"):
                        self.d(resourceId="com.lietou.mishu:id/ib_menu_back").click()
                        self.d.swipe(0.5, 0.8, 0.5, 0.55)
                        num += 1
                    elif self.d(text="简历不符合要求，系统已过滤"):
                        self.d(resourceId="com.lietou.mishu:id/ib_menu_back").click()
                        self.d.swipe(0.5, 0.8, 0.5, 0.55)
                        num += 1
                    elif self.d(text="未审核通过"):
                        self.d(resourceId="com.lietou.mishu:id/ib_menu_back").click()
                        self.d.swipe(0.5, 0.8, 0.5, 0.55)
                        num += 1
                    elif self.d(text="亲~请连接网络～"):
                        self.d(resourceId="com.lietou.mishu:id/ib_menu_back").click()
                        self.d.swipe(0.5, 0.8, 0.5, 0.55)
                        num += 1
                    else:
                        self.d.swipe(0.5, 0.8, 0.5, 0.55)
                        num += 1
                        continue
                self.d.swipe(0.9, 0.5, 0.2, 0.5)
                tmp += 1
            # default status
            back_num = 0
            while back_num < 5:
                self.d.swipe(0.4, 0.5, 0.9, 0.5)
                time.sleep(3)
                back_num += 1
        except EOFError as e:
            log.d(e)
            self.d.press("back")
            self.d.press("back")
            self.d.press("back")

    @testcase
    def test_b_search(self):
        try:
            if self.d(resourceId="com.lietou.mishu:id/v_hidden").wait(timeout=6):
                self.d(resourceId="com.lietou.mishu:id/v_hidden").click()
            else:
                print('正常')
            if self.d(text="您的账号已在其他设备登录，请重新登录").wait(timeout=3):
                time.sleep(5)
                self.d(text="确定").click()
            elif self.d(text="我要招人").wait(timeout=3):
                self.d(text="我要招人").click()
                self.d(text="完成").click()
            elif self.d(resourceId="com.lietou.mishu:id/iv_close").wait(timeout=3):
                self.d(resourceId="com.lietou.mishu:id/iv_close").click()
                if self.d(text="跳过，暂时不想填写").wait(timeout=3):
                    self.d(text="跳过，暂时不想填写").click()
                    if self.d(resourceId="com.lietou.mishu:id/iv_to_recruit").wait(timeout=5):
                        self.d(resourceId="com.lietou.mishu:id/iv_to_recruit").click()
            if LoginPage.LoginPage().wait_page("密码登录"):
                self.d(text="密码登录").click()
                self.d.set_fastinput_ime(True)
                LoginPage.login()
                self.d.set_fastinput_ime(False)
                if self.d(text="我要招人").wait(timeout=5):
                    self.d(text="我要招人").click()
                    self.d(text="完成").click()
                elif self.d(resourceId="com.lietou.mishu:id/iv_close").wait(timeout=3):
                    self.d(resourceId="com.lietou.mishu:id/iv_close").click()
                    if self.d(text="跳过，暂时不想填写").wait(timeout=3):
                        self.d(text="跳过，暂时不想填写").click()
                        if self.d(resourceId="com.lietou.mishu:id/rl_resume_root").wait(timeout=10):
                            self.d(resourceId="com.lietou.mishu:id/iv_to_recruit").click()
            if self.d(text="请选择性别").wait(timeout=3):
                self.d(resourceId="com.lietou.mishu:id/select_man").click()
                self.d(text="确认").click()
            if self.d(resourceId="com.lietou.mishu:id/search").wait(timeout=20):
                time.sleep(3)
                # 获取设备系统版本
                get_version = self.d.device_info['version']

                # get_num = self.get_post_num()
                post_list = {'HR': 'HRBP', 'UI': 'UI设计师', '市场': '市场专员'}
                time.sleep(2)

                # 系统版本兼容
                # if get_version < '5.1.1':
                #     if self.d.xpath("//android.view.View/android.widget.ImageView").wait(timeout=5):
                #         self.d.xpath("//android.view.View/android.widget.ImageView").click()
                # else:
                #     if self.d.xpath("//android.view.ViewGroup/android.widget.ImageView").wait(timeout=5):
                #         self.d.xpath("//android.view.ViewGroup/android.widget.ImageView").click()
                if self.d(resourceId="com.lietou.mishu:id/search").wait(timeout=3):
                    self.d(resourceId="com.lietou.mishu:id/search").click()
                for text_name in post_list.keys():
                    if self.d(text="按职位搜索").wait(timeout=3):
                        self.d(text="请输入关键词多个词请用空格隔开").set_text(text_name)
                        if get_version < '5.1.1':
                            self.d.xpath("//android.widget.ScrollView/android.view.View"
                                         "/android.view.View[contains(@index, 0)]").click()
                        else:
                            self.d.xpath("//android.widget.ScrollView/android.view.ViewGroup"
                                         "/android.view.ViewGroup[contains(@index, 0)]").click()
                    tmp = 0
                    while tmp < 5:
                        time.sleep(3)
                        get_version = self.d.device_info['version']
                        if get_version < '5.1.1':
                            self.d.xpath("//android.widget.ScrollView/android.view.View"
                                         "/android.view.View").click()
                        else:
                            self.d.xpath("//android.widget.ScrollView/android.view.ViewGroup"
                                         "/android.view.ViewGroup").click()

                        if self.d(text="立即沟通").wait(timeout=5):
                            self.d(text="立即沟通").click()

                            if self.d(resourceId="com.lietou.mishu:id/header_title").wait(timeout=3):
                                print(post_list[text_name])
                                self.d(text=post_list[text_name]).click()
                                self.d(text="确定").click()
                            time.sleep(2)
                            self.d(resourceId="com.lietou.mishu:id/rl_multi_and_send").click()
                            if self.d(text="发送职位").wait(timeout=5):
                                self.d(text="发送职位").click()
                            # 当职位list增多时，需要考虑弹框显示不全的情况，滑动找控件，只执行5次
                            post_num = 0
                            while post_num < 3:
                                if self.d(text=post_list[text_name]):
                                    self.d(text=post_list[text_name]).click()
                                    self.d(text="确认").click()
                                    self.d.set_fastinput_ime(False)
                                    self.d(resourceId="com.lietou.mishu:id/rl_input").click()
                                    self.d(resourceId="com.lietou.mishu:id/et_chat").set_text("您好，我们在为知名互联网公司招聘**岗位，工作地点在北京/上海/深圳，觉得您的经历很匹配。如果感兴趣可以点击应聘我发给您的职位，稍后可以详细沟通")
                                    self.d(text="发送").click()
                                    break
                                else:
                                    self.d(resourceId="com.lietou.mishu:id/recycler_view").swipe("up")
                                    post_num += 1

                            self.d(resourceId="com.lietou.mishu:id/chat_left_group").click()
                            self.d(resourceId="com.lietou.mishu:id/ib_menu_back").click()
                            self.d.swipe(0.5, 0.8, 0.5, 0.55)
                            tmp += 1
                        elif self.d(text="继续沟通"):
                            self.d(resourceId="com.lietou.mishu:id/ib_menu_back").click()
                            self.d.swipe(0.5, 0.8, 0.5, 0.55)
                            tmp += 1
                        elif self.d(text="该简历设置了隐私"):
                            self.d(resourceId="com.lietou.mishu:id/ib_menu_back").click()
                            self.d.swipe(0.5, 0.8, 0.5, 0.55)
                            tmp += 1
                        elif self.d(text="简历不符合要求，系统已过滤"):
                            self.d(resourceId="com.lietou.mishu:id/ib_menu_back").click()
                            self.d.swipe(0.5, 0.8, 0.5, 0.55)
                            tmp += 1
                        elif self.d(text="未审核通过"):
                            self.d(resourceId="com.lietou.mishu:id/ib_menu_back").click()
                            self.d.swipe(0.5, 0.8, 0.5, 0.55)
                            tmp += 1
                        elif self.d(text="亲~请连接网络～"):
                            self.d(resourceId="com.lietou.mishu:id/ib_menu_back").click()
                            self.d.swipe(0.5, 0.8, 0.5, 0.55)
                            tmp += 1
                        else:
                            self.d.swipe(0.5, 0.8, 0.5, 0.55)
                            tmp += 1
                            continue
                    self.d(text="取消").click()
                    time.sleep(2)
                    if self.d(resourceId="com.lietou.mishu:id/search").wait(timeout=3):
                        self.d(resourceId="com.lietou.mishu:id/search").click()
            else:
                log.d("未找到")
        except EOFError as e:
            log.d(e)
            self.d.press("back")
            self.d.press("back")
            self.d.press("back")

    @testcase
    def test_c_logout(self):
        self.logout()
        if self.d(text="手机号登录/注册").wait(timeout=3):
            log.d("退出成功")
        else:
            self.logout()
        self.d.swipe(0.2, 0.95, 0.2, 0.3)
        if self.d(resourceId="com.android.systemui:id/clear_all_progress"):
            self.d(text="清除缓存").click()
            time.sleep(2)
            self.d(resourceId="com.android.systemui:id/clear_all_progress").click()


if __name__ == "__main__":
    cases = unittest.TestSuite()
    cases.addTest(DynamicTest('test_b_search'))
    Drivers().run(cases)
    # unittest.main()