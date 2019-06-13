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
        get_version = self.d.device_info['version']
        # 系统版本兼容
        if get_version < '5.1.1':
            d = self.d.xpath(
                "//android.view.View/android.view.View/../android.view.View/android.widget.TextView")
        else:
            d = self.d.xpath(
                "//android.view.ViewGroup/android.view.ViewGroup/../android.view.ViewGroup/android.widget.TextView")
        for i in d.all():
            get_name = i.text
            if "已发布" in get_name:
                post_num = get_name.split("已发布（")[1].split("）")
        self.d(resourceId="com.lietou.mishu:id/recruitment_main").click()
        return int(post_num[0])

    @testcase
    def test_a_recommend(self):
        if self.d(resourceId="com.lietou.mishu:id/v_hidden"):
            self.d(resourceId="com.lietou.mishu:id/v_hidden").click()
        else:
            if LoginPage.LoginPage().wait_page("密码登录"):
                self.d(text="密码登录").click()
                self.d.set_fastinput_ime(True)
                LoginPage.login()
                self.d.set_fastinput_ime(False)
            tmp = 0
            get_num = self.get_post_num()
            while tmp < get_num:
                num = 0
                while num < 10:
                    time.sleep(10)
                    get_version = self.d.device_info['version']
                    if get_version < '5.1.1':
                        if self.d.xpath("//android.widget.ScrollView/android.view.View"
                                        "/android.widget.ScrollView/android.view.View"
                                        "/android.view.View").wait(timeout=3):
                            self.d.xpath("//android.widget.ScrollView/android.view.View"
                                         "/android.widget.ScrollView/android.view.View"
                                         "/android.view.View").click()
                    else:
                        if self.d.xpath("//android.widget.ScrollView/android.view.ViewGroup"
                                        "/android.widget.ScrollView/android.view.ViewGroup"
                                        "/android.view.ViewGroup").wait(timeout=3):
                            self.d.xpath("//android.widget.ScrollView/android.view.ViewGroup"
                                         "/android.widget.ScrollView/android.view.ViewGroup"
                                         "/android.view.ViewGroup").click()
                    if self.d(text="立即沟通").wait(timeout=2):
                        self.d(text="立即沟通").click()
                        time.sleep(2)
                        get_post_name = self.d(resourceId="com.lietou.mishu:id/tv_talk_position").get_text()
                        self.d(resourceId="com.lietou.mishu:id/rl_multi_and_send").click()
                        self.d(text="发送职位").click()
                        # 当职位list增多时，需要考虑弹框显示不全的情况，滑动找控件，只执行5次
                        post_num = 0
                        while post_num < 3:
                            if self.d(text=get_post_name):
                                self.d(text=get_post_name).click()
                                self.d(text="确认").click()
                                self.d(resourceId="com.lietou.mishu:id/rl_input").click()
                                self.d(resourceId="com.lietou.mishu:id/et_chat").set_text("您好，觉得您的经历很匹配，可以把您的简历委托给我吗")
                                self.d.set_fastinput_ime(False)
                                self.d(text="发送").click()
                                break
                            else:
                                self.d(resourceId="com.lietou.mishu:id/recycler_view").swipe("up")
                                post_num += 1

                        self.d(resourceId="com.lietou.mishu:id/chat_left_group").click()
                        self.d(resourceId="com.lietou.mishu:id/ib_menu_back").click()
                        num += 1
                    elif self.d(text="继续沟通"):
                        self.d(resourceId="com.lietou.mishu:id/ib_menu_back").click()
                        self.d.swipe(0.5, 0.8, 0.5, 0.55)
                        num += 1
                    elif self.d(text="该简历设置了隐私"):
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
            while back_num < get_num + 2:
                self.d.swipe(0.4, 0.5, 0.9, 0.5)
                back_num += 1

    @testcase
    def test_b_search(self):
        if self.d(className="android.widget.HorizontalScrollView", instance=1).wait(timeout=20):
            time.sleep(3)
            # 获取设备系统版本
            get_version = self.d.device_info['version']

            get_num = self.get_post_num()
            post_list = []
            for num in range(get_num):
                if get_version < '5.1.1':
                    post_location = self.d.xpath("//android.widget.HorizontalScrollView/android.view.View"
                                                 "/android.view.View/android.view.View[contains(@index, %d)]"
                                                 "/android.widget.TextView" % num)
                else:
                    post_location = self.d.xpath("//android.widget.HorizontalScrollView/android.view.ViewGroup"
                                                 "/android.view.ViewGroup/android.view.ViewGroup[contains(@index, %d)]"
                                                 "/android.widget.TextView" % num)
                post_list.append(str(post_location.get_text()))
            time.sleep(2)

            # 系统版本兼容
            if get_version < '5.1.1':
                self.d.xpath("//android.view.View/android.widget.ImageView").click()
            else:
                self.d.xpath("//android.view.ViewGroup/android.widget.ImageView").click()

            for text_name in post_list:
                self.d(text=text_name).click()
                tmp = 0
                while tmp < 10:
                    time.sleep(10)
                    get_version = self.d.device_info['version']
                    if get_version < '5.1.1':
                        self.d.xpath("//android.widget.ScrollView/android.view.View"
                                     "/android.view.View").click()
                    else:
                        self.d.xpath("//android.widget.ScrollView/android.view.ViewGroup"
                                     "/android.view.ViewGroup").click()

                    if self.d(text="立即沟通").wait(timeout=2):
                        self.d(text="立即沟通").click()
                        time.sleep(2)
                        # 当职位list增多时，需要考虑弹框显示不全的情况，滑动找控件，只执行5次
                        post_num = 0
                        while post_num < 3:
                            if self.d(text=text_name):
                                self.d(text=text_name).click()
                                self.d(text="确认").click()
                                self.d.set_fastinput_ime(False)
                                self.d(resourceId="com.lietou.mishu:id/rl_input").click()
                                self.d(resourceId="com.lietou.mishu:id/et_chat").set_text("您好，觉得您的经历很匹配，可以把您的简历委托给我吗")
                                self.d(text="发送").click()
                                break
                            else:
                                self.d(resourceId="com.lietou.mishu:id/recycler_view").swipe("up")
                                post_num += 1

                        self.d(resourceId="com.lietou.mishu:id/chat_left_group").click()
                        self.d(resourceId="com.lietou.mishu:id/ib_menu_back").click()
                        self.d(text="清空").click()
                        self.d(text="取消").click()
                        time.sleep(2)
                        # 系统版本兼容
                        if get_version < '5.1.1':
                            self.d.xpath("//android.view.View/android.widget.ImageView").click()
                        else:
                            self.d.xpath("//android.view.ViewGroup/android.widget.ImageView").click()
                        tmp += 1
                    elif self.d(text="继续沟通"):
                        self.d(resourceId="com.lietou.mishu:id/ib_menu_back").click()
                        self.d.swipe(0.5, 0.8, 0.5, 0.55)
                        tmp += 1
                    elif self.d(text="该简历设置了隐私"):
                        self.d(resourceId="com.lietou.mishu:id/ib_menu_back").click()
                        self.d.swipe(0.5, 0.8, 0.5, 0.55)
                        tmp += 1
                    else:
                        self.d.swipe(0.5, 0.8, 0.5, 0.55)
                        tmp += 1
                        continue
                self.d(text="取消").click()
                time.sleep(2)
                # 系统版本兼容
                if get_version < '5.1.1':
                    self.d.xpath("//android.view.View/android.widget.ImageView").click()
                else:
                    self.d.xpath("//android.view.ViewGroup/android.widget.ImageView").click()

        else:
            log.i("未找到")

    @testcase
    def test_c_message(self):
        if self.d(className="android.widget.HorizontalScrollView", instance=1).wait(timeout=20):
            self.d(text="消息").click()
            message_list = ['可以', '好的', '好', '可以啊']
            num = 0
            while num < 5:
                for elem in self.d(resourceId="com.lietou.mishu:id/tv_content"):
                    get_message = elem.get_text()
                    if get_message in message_list:
                        elem.click()
                        self.d.set_fastinput_ime(False)
                        self.d(resourceId="com.lietou.mishu:id/rl_input").click()
                        self.d(resourceId="com.lietou.mishu:id/et_chat").set_text("那您方便发我一份简历吗？")
                        self.d(text="发送").click()
                        self.d(resourceId="com.lietou.mishu:id/chat_left_group").click()

                self.d.swipe(0.5, 0.8, 0.5, 0.3)
                num += 1
            self.d(text="推荐").click()
        else:
            log.i("未找到")


if __name__ == "__main__":
    cases = unittest.TestSuite()
    cases.addTest(DynamicTest('test_b_search'))
    Drivers().run(cases)
    # unittest.main()