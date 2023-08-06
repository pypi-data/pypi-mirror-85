# -*- coding: UTF-8 -*-


from testbase.conf import settings
from oed_native_lib.OEDWindow import OEDWindow

class OEDXWindow(OEDWindow):

    '''
    跨平台 Window类
    '''
    def __init__(self,OEDApp,**kwds):
        OEDWindow.__init__(self,OEDApp,**kwds)


    def updateLocator(self, locators):
        if settings.PLATFORM == "Android" or settings.PLATFORM == "h5":
            super(OEDXWindow,self).update_locator(locators)
        else:
            super(OEDXWindow, self).updateLocator(locators)

    def wait_for_exist(self, timeout=10, interval=0.5):
        if settings.PLATFORM == "h5":
            self.Activity = "com.tencent.mobileqq.activity.QQBrowserActivity"
        try:
            return super(OEDXWindow,self).wait_for_exist(timeout,interval)
        except Exception:
            return False