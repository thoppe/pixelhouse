import numpy as np
import collections
from scipy.misc import comb

"""
Adapeted from https://github.com/reptillicus/Bezier
"""


def bernstein_poly(i, n, t):
    """
     The Bernstein polynomial of n, i as a function of t
    """

    return comb(n, i) * (t ** (n - i)) * (1 - t) ** i


class bezierMotionCurve:
    """
    Bezier curve with endpoints set at (0,0) and (1,1)
    """

    def __init__(self, x1, y1, x2, y2):
        points = np.array([(0, 0), (x1, y1), (x2, y2), (1, 1)])
        self.xPoints = np.array([p[0] for p in points])
        self.yPoints = np.array([p[1] for p in points])
        self.nPoints = 4

    def __call__(self, t):
        if not isinstance(t, collections.Iterable):
            t = np.array([t])

        polynomial_array = np.array(
            [
                bernstein_poly(i, self.nPoints - 1, t)
                for i in range(0, self.nPoints)
            ]
        )

        xvals = np.dot(self.xPoints, polynomial_array)
        yvals = np.dot(self.yPoints, polynomial_array)

        return xvals, yvals
