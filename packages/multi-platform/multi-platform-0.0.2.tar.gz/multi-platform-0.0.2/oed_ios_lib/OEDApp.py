# -*- coding:utf-8 -*-
'''Ke App类
'''

from qt4i.app import App
from testbase.conf import settings
import time

class OEDApp(App):
    '''KeApp 负责被测应用的启动和初始化
    '''

    def __init__(self, device, app_name=settings.APP_BUNDLE_ID, trace_template=None, trace_output=None,
                 clear_data=False, choose_user_guide=False, **params):
        '''APP应用（启动APP）
        
        :param device         : Device的实例对象
        :type device          : Device
        :param app_name       : APP的BundleID（例如：com.tencent.sng.test.gn）
        :type app_name        : str
        :param trace_template : trace模板（专项测试使用，功能测试默认为None即可）
        :type trace_template  : str
        :param trace_output   : teace存储路径（专项测试使用，功能测试默认为None即可）
        :type trace_output    : str
        :param clear_data   : 是否清理App数据（暂时没实现）
        :type clear_data    : boolean
        '''

        App.__init__(self, device, app_name, trace_template, trace_output, **params)
        self.choose_user_guide = choose_user_guide
        self.re_install = True
        self.set_environment()
        self.start()

        time.sleep(5)



    def set_environment(self):
        '''初始化自动处理Alert弹框应对规则
        
        :param: none
        :returns: none
        '''
        # 此规则用于处理预期内容但难以预期弹出时机的Alert框（注意国际化多国语言的情况）。
        # 配置策略后，只要Alert框命中策略，即按策略处理。例如指定点击取消或确定按钮。
        self.rules_of_alert_auto_handle = [

            # 推送通知
            {
                'message_text': '推送通知|Notifications',  # 支持正则表达式
                'button_text': '^好$|^Allow$|^允许$'  # 支持正则表达式
            },

            # ios10推送通知
            {
                'message_text': '发送通知|Notifications',  # 支持正则表达式
                'button_text': '^好$|^Allow$|^允许$'  # 支持正则表达式
            },

            # 测试账号Alert框（测试账号会弹出，曾经出现连弹多次）
            {
                'message_text': '测试号码',  # 支持正则表达式
                'button_text': '^确定$'  # 支持正则表达式
            },

            # 授权APP访问位置
            {
                'message_text': '位置|Location',
                'button_text': '^好$|^Allow$|^允许$'
            },

            # 授权APP访问相册
            {
                'message_text': '照片|Photos',
                'button_text': '^允许$|^好$|^OK$'
            },

            # 授权APP访问麦克风
            {
                'message_text': '麦克风',
                'button_text': '^允许$|^好$|^OK$'
            },

            # 授权APP访问相机                              
            {
                'message_text': '相机',
                'button_text': '^允许$|^好$|^OK$'
            },

            # 用于处理退出登录 (屏蔽退出登录的自动处理)
            {
                'message_text': '退出当前帐号',
            },

        ]

        # 此开关打开，用于处理不可预期内容且不可预期时机的Alert框
        # 如果Alert框命中上方的策略，则此项配置将被跳过。
        self.flag_alert_auto_handled = False
