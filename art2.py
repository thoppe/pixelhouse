import numpy as np
import scipy
import canvas
import cv2
import itertools


_default_color = 'white'


#########################################################################
    
class artist():

    '''
    Artists are the backbone of pixelhouse. They draw what's on the screen.
    To be a proper artist, all derived classes must accept their arguments
    as functions.
    '''
    
    @staticmethod
    def _constant(x):
        def func(t):
            return x
        return func

    @staticmethod
    def _create_interpolation(y):
       t = np.linspace(0, 1, len(y))
       f = scipy.interpolate.interp1d(t, y)
       def func(x):
           return f(x)
       return func

    def __init__(self,**kwargs):
        '''
        When an artist is initiated, all of the attributes can be set
        as a function of time. These attributes can be a constant, a numpy
        array (interpolation will be used if needed), or a function.
        '''


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
                setattr(self, key, self._constant(val))

    def __call__(self, t):
        # Virtual class, need to override
        raise NotImplementedError


'''
def circle(c, x=0, y=0, r=1, color=_default_color,
        thickness=-1, antialiased=True, blend=True, layer=None):

    x, y = c.transform_coordinates(x, y)
    r = c.transform_length(r)
    thickness = c.transform_length(thickness)
    lineType = c.get_lineType(antialiased)
    color=c.transform_color(color)

    args = (x,y), r, color, thickness, lineType
    c.append(cv2.circle, args, blend=blend, layer=None)
'''


#############################################################################
def constant(x):
    def func(self, t):
        return x
    return func

class animated_circle(artist):

    x = constant(0.0)
    y = constant(0.0)
    r = constant(1.0)
    color = constant(_default_color)
    thickness = constant(-1)

    def __call__(self, t, cvs):

        blend = 0
        layer = None
        antialiased = True

        x, y = c.transform_coordinates(self.x(t), self.y(t))
        r = c.transform_length(self.r(t))
        thickness = c.transform_length(self.thickness(t))
        color=c.transform_color(self.color(t))
        lineType = c.get_lineType(antialiased)

        args = (x,y), r, color, thickness, lineType

        cvs.append(cv2.circle, args, blend)


if __name__== "__main__":
    c = canvas.canvas()

    #c.append(0.0, animated_circle())
    animated_circle()(0.0, c)

    c.show()
    
