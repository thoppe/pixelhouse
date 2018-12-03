import numpy as np
import collections

from scipy.special import binom
from scipy.interpolate import interp1d


def Bernstein(n, k):
    """Bernstein polynomial."""
    coeff = binom(n, k)

    def _bpoly(x):
        return binom(n, k) * x ** k * (1 - x) ** (n - k)

    return _bpoly


def Bezier(points, sample_points=200):
    """Build Bezier curve from points."""
    N = len(points)
    t = np.linspace(0, 1, sample_points)
    curve = np.zeros((sample_points, 2))
    for ii in range(N):
        curve += np.outer(Bernstein(N - 1, ii)(t), points[ii])
    return curve


"""
Adapted from https://github.com/reptillicus/Bezier
https://gist.github.com/Juanlu001/7284462
"""


class bezierMotionCurve:
    """
    Bezier curve with endpoints set at (0,0) and (1,1)
    """

    def __init__(self, x1, y1, x2, y2, sample_points=200):
        points = np.array([(0.0, 0), (x1, y1), (x2, y2), (1, 1)])
        x, y = Bezier(points, sample_points=sample_points).T

        self.func = interp1d(x, y, kind="quadratic")

    def __call__(self, t):
        return self.func(t)
