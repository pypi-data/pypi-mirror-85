# -*- coding: utf-8 -*-

from qt4a.andrcontrols import ControlNotFoundError
from metislib.controls import MtControl
import time

from testbase.conf import settings

if settings.PLATFORM == 'iOS':
    from qt4i.icontrols import Element
    class Element(Element):
        def __init__(self, root, locator, **ext):
            super(Element,self).__init__(root,locator,**ext)

        def click(self, offset_x=None, offset_y=None):
            super(Element,self).click(offset_x,offset_y)

        @property
        def text(self):
            return self.value

        @text.setter
        def text(self, text):
            '''设置value(输入，支持中文)
            '''
            self.value = text

class MtControl(MtControl):
    def __init__(self, root, id, locator=None, name=None, instance=None):
        super(MtControl,self).__init__(root,id,locator,name,instance)

    def wait_for_exist(self, timeout=10, interval=0.5):
        '''等待控件出现
         '''
        time0 = time.time()
        while time.time() - time0 < timeout:
            if self.exist(): return True
            time.sleep(interval)
        raise ControlNotFoundError('控件：%s 未找到' % self._id)
