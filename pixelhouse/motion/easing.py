"""
Base easing functions modified from: https://easings.net/
"""

import math
import numpy as np
from .bezier import bezierMotionCurve

class EasingBase:
    def __init__(self, start=0, stop=1): #, duration=1.0):
        self.start = start
        self.stop = stop

    def __call__(self, t):
        a = self.func(t)
        return self.start * (1 - a) + self.stop * a

    def func(self, t):
        raise NotImplementedError

class Linear(EasingBase):
    def func(self, t): return t


class BezierEase(EasingBase):
    def __init__(self, start=0, stop=1):
        super().__init__(start, stop)
        
        # Lazy loading of the Bezier curve so we can quickly create objects
        # note that x0, y0, x1, y1 must be set in the derived class
        self.f = None

    def get_params(self):
        '''
        Return a set of arguments to construct the easing.
        '''
        return (self.x0, self.y0, self.x1, self.y1)
        
    def func(self, t):
        if self.f is None:
            self.f = bezierMotionCurve(self.x0, self.y0, self.x1, self.y1)
        print(self, self.x0, self.y0, self.x1, self.y1)
        
        return self.f(t)

class easeInSine(BezierEase): x0, y0, x1, y1 = 0.47, 0, 0.745, 0.715
class easeOutSine(BezierEase): x0, y0, x1, y1 = 0.39, 0.575, 0.565, 1
class easeInOutSine(BezierEase): x0, y0, x1, y1 = 0.445, 0.05, 0.55, 0.95
class easeInQuad(BezierEase): x0, y0, x1, y1 = 0.55, 0.085, 0.68, 0.53
class easeOutQuad(BezierEase): x0, y0, x1, y1 = 0.25, 0.46, 0.45, 0.94
class easeInOutQuad(BezierEase): x0, y0, x1, y1 = 0.455, 0.03, 0.515, 0.955
class easeInCubic(BezierEase): x0, y0, x1, y1 = 0.55, 0.055, 0.675, 0.19
class easeOutCubic(BezierEase): x0, y0, x1, y1 = 0.215, 0.61, 0.355, 1
class easeInOutCubic(BezierEase): x0, y0, x1, y1 = 0.645, 0.045, 0.355, 1
class easeInQuart(BezierEase): x0, y0, x1, y1 = 0.895, 0.03, 0.685, 0.22
class easeOutQuart(BezierEase): x0, y0, x1, y1 = 0.165, 0.84, 0.44, 1
class easeInOutQuart(BezierEase): x0, y0, x1, y1 = 0.77, 0, 0.175, 1
class easeInQuint(BezierEase): x0, y0, x1, y1 = 0.755, 0.05, 0.855, 0.06
class easeOutQuint(BezierEase): x0, y0, x1, y1 = 0.23, 1, 0.32, 1
class easeInOutQuint(BezierEase): x0, y0, x1, y1 = 0.86, 0, 0.07, 1
class easeInExpo(BezierEase): x0, y0, x1, y1 = 0.95, 0.05, 0.795, 0.035
class easeOutExpo(BezierEase): x0, y0, x1, y1 = 0.19, 1, 0.22, 1
class easeInOutExpo(BezierEase): x0, y0, x1, y1 = 1, 0, 0, 1
class easeInCirc(BezierEase): x0, y0, x1, y1 = 0.6, 0.04, 0.98, 0.335
class easeOutCirc(BezierEase): x0, y0, x1, y1 = 0.075, 0.82, 0.165, 1
class easeInOutCirc(BezierEase): x0, y0, x1, y1 = 0.785, 0.135, 0.15, 0.86
class easeInBack(BezierEase): x0, y0, x1, y1 = 0.6, -0.28, 0.735, 0.045
class easeOutBack(BezierEase): x0, y0, x1, y1 = 0.175, 0.885, 0.32, 1.275
class easeInOutBack(BezierEase): x0, y0, x1, y1 = 0.68, -0.55, 0.265, 1.55


#########################################################################
# Custom Easing functions
#########################################################################


class offsetEase(BezierEase):
    def __init__(self, dx=0.0, dy=0.1, baseEase="easeInSine", *args, **kwargs):        
        ease = globals()[baseEase](*args, **kwargs)
        x0, y0, x1, y1 = ease.get_params()
        
        x0 -= dx
        x1 += dx
        y0 -= dy
        y1 += dy

        super().__init__(x0, x1, y0, y1, *args, **kwargs)

def easeReturn(easing_func, start, stop, frames):
    """
    Returns an easing run that finishes halfway through and returns.
    """
    raise NotImplementedError
    
    if isinstance(easing_func, str):
        easing_func = globals()[easing_func]

    n0 = frames // 2
    n1 = frames - n0

    x0 = easing_func(start, stop, n0)()
    x1 = easing_func(stop, start, n1)()

    return np.hstack([x0, x1])

