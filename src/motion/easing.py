'''
Easing functions modified from:

https://github.com/semitable/easing-functions
GNU General Public License v3.0

'''

import math
import numpy as np
from .bezier import bezierMotionCurve


class EasingBase:

    def __init__(self, start=0, stop=1, duration=1):
        self.start = start
        self.stop = stop

    def __call__(self, T):        
        _, a = self.func(T)
        return self.stop * a + self.start * (1 - a)
    
    @classmethod
    def func(cls, t):
        raise NotImplementedError


class BezierEase(EasingBase):

    def __init__(self, x0=0.45, y0=0.25, x1=0.55, y1=0.75, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.f = bezierMotionCurve(x0, y0, x1, y1)
   
    def func(self, t):
        return self.f(t)
  

class SmoothEaseIn(BezierEase):
    
    def __init__(self, dx=0.1, *args, **kwargs):
        kwargs.update({
            'x0':0.45,
            'x1':0.55,
            'y0':0.25-dx,
            'y1':0.75+dx,
        })

        super().__init__(*args, **kwargs)

