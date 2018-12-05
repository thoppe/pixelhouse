import numpy as np
import scipy
import itertools


#########################################################################
_DEFAULT_MODE = "blend"


def constant(x):
    def func(self, t=0, *args, **kwargs):
        return x

    return func


def constant_list(*x):
    def func(self, t=0, *args, **kwargs):
        return x

    return func


class Artist:
    """
    Artists are the backbone of pixelhouse. They draw what's on the screen.
    To be a proper artist, all derived classes must accept their arguments
    as functions and define a "draw" method.
    """

    mode = constant(_DEFAULT_MODE)
    args = []

    @staticmethod
    def _create_interpolation(z):
        t = np.linspace(0, 1, len(z))
        f = scipy.interpolate.interp1d(t, z)

        def func(x):
            return f(x)

        return func

    def __init__(self, *args, **kwargs):
        """
        When an artist is initiated, all of the attributes can be set
        as a function of time. These attributes can be a constant, a numpy
        array (interpolation will be used if needed), or a function.
        """

        for key, val in zip(self.args, args):
            kwargs[key] = val

        attributes = dir(self)
        for key, val in kwargs.items():

            # Can't set attributes an object doesn't have
            if key not in attributes:
                msg = f"{key} not in class {self}"
                raise AttributeError(msg)

            # If the val is callable, that's what we use
            if callable(val):
                setattr(self, key, val)

            # If the val is a numpy array
            elif isinstance(val, np.ndarray):
                interpfunc = self._create_interpolation(val)
                setattr(self, key, interpfunc)

            # Otherwise we assume it's a constant of this value
            else:
                # setattr(self, key, self._constant(val))
                setattr(self, key, constant(val))

    def __call__(self, t, *args, **kwargs):
        # Convenience method for draw
        self.draw(t, *args, **kwargs)

    def draw(self, t):
        # Virtual class, need to override
        raise NotImplementedError
