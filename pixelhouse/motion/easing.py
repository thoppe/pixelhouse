"""
Base easing functions modified from: https://easings.net/
"""

import math
import numpy as np
from .bezier import bezierMotionCurve


class EasingBase:
    def __init__(self, start=0, stop=1, duration=1.0):
        self.start = start
        self.stop = stop
        self.duration = duration

    def __call__(self):
        t = np.linspace(0, 1, self.duration)
        _, a = self.func(t)
        return self.stop * (1 - a) + self.start * a

    @classmethod
    def func(cls, t):
        raise NotImplementedError


class BezierEase(EasingBase):
    def __init__(
        self, x0=0.45, y0=0.25, x1=0.55, y1=0.75, start=0, stop=1, duration=1
    ):

        super().__init__(start, stop, duration)
        self.f = bezierMotionCurve(x0, y0, x1, y1)

    def func(self, t):
        return self.f(t)


def BezierClassFactory(x0, y0, x1, y1):
    class B(BezierEase):
        def __init__(self, start=0, stop=1, duration=1):
            super().__init__(x0, y0, x1, y1, start, stop, duration)

    return B


named_easings = {
    "easeInSine": (0.47, 0, 0.745, 0.715),
    "easeOutSine": (0.39, 0.575, 0.565, 1),
    "easeInOutSine": (0.445, 0.05, 0.55, 0.95),
    "easeInQuad": (0.55, 0.085, 0.68, 0.53),
    "easeOutQuad": (0.25, 0.46, 0.45, 0.94),
    "easeInOutQuad": (0.455, 0.03, 0.515, 0.955),
    "easeInCubic": (0.55, 0.055, 0.675, 0.19),
    "easeOutCubic": (0.215, 0.61, 0.355, 1),
    "easeInOutCubic": (0.645, 0.045, 0.355, 1),
    "easeInQuart": (0.895, 0.03, 0.685, 0.22),
    "easeOutQuart": (0.165, 0.84, 0.44, 1),
    "easeInOutQuart": (0.77, 0, 0.175, 1),
    "easeInQuint": (0.755, 0.05, 0.855, 0.06),
    "easeOutQuint": (0.23, 1, 0.32, 1),
    "easeInOutQuint": (0.86, 0, 0.07, 1),
    "easeInExpo": (0.95, 0.05, 0.795, 0.035),
    "easeOutExpo": (0.19, 1, 0.22, 1),
    "easeInOutExpo": (1, 0, 0, 1),
    "easeInCirc": (0.6, 0.04, 0.98, 0.335),
    "easeOutCirc": (0.075, 0.82, 0.165, 1),
    "easeInOutCirc": (0.785, 0.135, 0.15, 0.86),
    "easeInBack": (0.6, -0.28, 0.735, 0.045),
    "easeOutBack": (0.175, 0.885, 0.32, 1.275),
    "easeInOutBack": (0.68, -0.55, 0.265, 1.55),
}

for key, vals in named_easings.items():
    locals()[key] = BezierClassFactory(*vals)

#########################################################################
# Custom Easing functions
#########################################################################


class offsetEase(BezierEase):
    def __init__(self, dx=0.0, dy=0.1, baseEase="easeInSine", *args, **kwargs):
        x0, x1, y0, y1 = named_easings[baseEase]
        x0 -= dx
        x1 += dx
        y0 -= dy
        y1 += dy

        super().__init__(x0, x1, y0, y1, *args, **kwargs)


def easeReturn(easing_func, start, stop, frames):
    """
    Returns an easing run that finishes halfway through and returns.
    """
    if isinstance(easing_func, str):
        easing_func = globals()[easing_func]

    n0 = frames // 2
    n1 = frames - n0

    x0 = easing_func(start, stop, n0)()
    x1 = easing_func(stop, start, n1)()

    return np.hstack([x0, x1])
