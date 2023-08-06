# -*- coding: UTF-8 -*-

'''Ke App类
'''

from qt4a.androidapp import AndroidApp
import time
from testbase.conf import settings


class OEDApp(AndroidApp):
    '''
    '''
    package_name = settings.PACKAGE_NAME
    start_activity = settings.START_ACTIVITY

    def __init__(self, device, kill_process=True, start_activity=True, clear_data=True, choose_user_guide=False):
        super(OEDApp, self).__init__(self.__class__.package_name, device)

        if settings.DEBUG:
            kill_process = False
            start_activity = False
            clear_data = False

        self.re_install = True
        self.choose_user_guide = choose_user_guide

        # 辅导的debug包也进行了控件Id混淆
        if hasattr(settings, 'QT4A_USE_INT_VIEW_ID') and settings.QT4A_USE_INT_VIEW_ID:
            self._use_int_view_id = True
        else:
            pass

        if kill_process:
            self._device.kill_process(self.__class__.package_name)

        if clear_data:
            self._device.clear_data(self.__class__.package_name)
        else:
            self.re_install = False

        self.grant_all_runtime_permissions()

        if start_activity:
            self.start()

    def start(self):
        '''启动应用
        '''
        self._device.start_activity(self.__class__.package_name + '/' + self.__class__.start_activity)
        time.sleep(3)

