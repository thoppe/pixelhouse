"""
Base easing functions modified from: https://easings.net/
"""

import math
import numpy as np
import copy
from .bezier import bezierMotionCurve
from scipy.interpolate import interp1d


class EasingBase:
    def __init__(self, start=0, stop=1, translate=0.0, scale=1.0):
        self.start = start
        self.stop = stop
        self.translate = 0.0
        self.scale = 1.0

    def copy(self):
        # Returns a deep copy of the Easing
        return copy.deepcopy(self)

    def __neg__(self):
        rhs = self.copy()
        rhs.scale *= -1
        return rhs

    def __add__(self, val):
        rhs = self.copy()
        rhs.translate += val
        return rhs

    def __radd__(self, val):
        return self + val

    def __sub__(self, val):
        rhs = self.copy()
        rhs.translate -= val
        return rhs

    def __mul__(self, val):
        rhs = self.copy()
        rhs.scale *= val
        return rhs

    def __rmul__(self, val):
        return self * val

    def __truediv__(self, val):
        rhs = self.copy()
        rhs.scale /= val
        return rhs

    def __call__(self, t):
        a = self.func(t)

        value = self.start * (1 - a) + self.stop * a
        return self.scale * (self.translate + value)

    def func(self, t):
        raise NotImplementedError


class BezierEase(EasingBase):
    def __init__(self, start=0, stop=1, flip=None, phase=0.0, *args, **kwargs):
        super().__init__(start, stop, *args, **kwargs)

        # Lazy loading of the Bezier curve so we can quickly create objects
        # note that x0, y0, x1, y1 must be set in the derived class
        self.f = None

        self.phase = phase
        self.flip = flip

        if flip is True:
            self.flip = interp1d([0, 0.5, 1.0], [0, 1, 0])

    def get_params(self):
        """
        Return a set of arguments to construct the easing.
        """
        return (self.x0, self.y0, self.x1, self.y1)

    def func(self, t):
        t += self.phase

        # If t is STRICTLY greater than 1, take the mod
        if isinstance(t, np.ndarray):
            t[t > 1] = np.mod(t[t > 1], 1.0)
            t[t < 0] = np.mod(t[t < 0], 1.0)
        else:
            if t > 1 or t < 0:
                t %= 1.0

        if self.f is None:
            self.f = bezierMotionCurve(self.x0, self.y0, self.x1, self.y1)

        if self.flip:
            t = self.flip(t)

        return self.f(t)


#########################################################################
# Named Easing functions
#########################################################################


class Linear(EasingBase):
    def func(self, t):
        return t


class easeInSine(BezierEase):
    x0, y0, x1, y1 = 0.47, 0, 0.745, 0.715


class easeOutSine(BezierEase):
    x0, y0, x1, y1 = 0.39, 0.575, 0.565, 1


class easeInOutSine(BezierEase):
    x0, y0, x1, y1 = 0.445, 0.05, 0.55, 0.95


class easeInQuad(BezierEase):
    x0, y0, x1, y1 = 0.55, 0.085, 0.68, 0.53


class easeOutQuad(BezierEase):
    x0, y0, x1, y1 = 0.25, 0.46, 0.45, 0.94


class easeInOutQuad(BezierEase):
    x0, y0, x1, y1 = 0.455, 0.03, 0.515, 0.955


class easeInCubic(BezierEase):
    x0, y0, x1, y1 = 0.55, 0.055, 0.675, 0.19


class easeOutCubic(BezierEase):
    x0, y0, x1, y1 = 0.215, 0.61, 0.355, 1


class easeInOutCubic(BezierEase):
    x0, y0, x1, y1 = 0.645, 0.045, 0.355, 1


class easeInQuart(BezierEase):
    x0, y0, x1, y1 = 0.895, 0.03, 0.685, 0.22


class easeOutQuart(BezierEase):
    x0, y0, x1, y1 = 0.165, 0.84, 0.44, 1


class easeInOutQuart(BezierEase):
    x0, y0, x1, y1 = 0.77, 0, 0.175, 1


class easeInQuint(BezierEase):
    x0, y0, x1, y1 = 0.755, 0.05, 0.855, 0.06


class easeOutQuint(BezierEase):
    x0, y0, x1, y1 = 0.23, 1, 0.32, 1


class easeInOutQuint(BezierEase):
    x0, y0, x1, y1 = 0.86, 0, 0.07, 1


class easeInExpo(BezierEase):
    x0, y0, x1, y1 = 0.95, 0.05, 0.795, 0.035


class easeOutExpo(BezierEase):
    x0, y0, x1, y1 = 0.19, 1, 0.22, 1


class easeInOutExpo(BezierEase):
    x0, y0, x1, y1 = 1, 0, 0, 1


class easeInCirc(BezierEase):
    x0, y0, x1, y1 = 0.6, 0.04, 0.98, 0.335


class easeOutCirc(BezierEase):
    x0, y0, x1, y1 = 0.075, 0.82, 0.165, 1


class easeInOutCirc(BezierEase):
    x0, y0, x1, y1 = 0.785, 0.135, 0.15, 0.86


class easeInBack(BezierEase):
    x0, y0, x1, y1 = 0.6, -0.28, 0.735, 0.045


class easeOutBack(BezierEase):
    x0, y0, x1, y1 = 0.175, 0.885, 0.32, 1.275


class easeInOutBack(BezierEase):
    x0, y0, x1, y1 = 0.68, -0.55, 0.265, 1.55


#########################################################################
# Custom Easing functions
#########################################################################
