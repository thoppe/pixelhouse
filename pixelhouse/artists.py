import numpy as np
import scipy
import canvas
import cv2
import itertools

_DEFAULT_COLOR = 'white'
_DEFAULT_THICKNESS = -1
_DEFAULT_BLEND = True
_DEFAULT_ANTIALIASED = True

#########################################################################
def constant(x):
    def func(self, t=0):
        return x
    return func

class artist():
    '''
    Artists are the backbone of pixelhouse. They draw what's on the screen.
    To be a proper artist, all derived classes must accept their arguments
    as functions.
    '''

    # Basic attributes common to all artists
    x = constant(0.0)
    y = constant(0.0)
    color = constant(_DEFAULT_COLOR)
    thickness = constant(_DEFAULT_THICKNESS)
    blend = constant(_DEFAULT_BLEND)
    antialiased = constant(_DEFAULT_ANTIALIASED)

    
    @staticmethod
    def _constant(x):
        def func(t):
            return x
        return func

    @staticmethod
    def _create_interpolation(z):
       t = np.linspace(0, 1, len(z))
       f = scipy.interpolate.interp1d(t, z)
       def func(x):
           return f(x)
       return func

    def __init__(self,  **kwargs):
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

    def basic_transforms(self, cvs, t):
        x = cvs.transform_x(self.x(t))
        y = cvs.transform_y(self.y(t))
        thickness = cvs.transform_thickness(self.thickness(t))
        color = cvs.transform_color(self.color(t))
        lineType = cvs.get_lineType(self.antialiased(t))

        return x, y, thickness, color, lineType




#############################################################################
# Class artists below
#############################################################################

class circle(artist):

    r = constant(1.0)

    def __call__(self, cvs, t=0.0):
        x, y, thickness, color, lineType = self.basic_transforms(cvs, t)
        r = cvs.transform_length(self.r(t))
        
        args = (x,y), r, color, thickness, lineType
        cvs.cv2_draw(cv2.circle, args, blend=self.blend(t))

class rectangle(artist):

    x1 = constant(1.0)
    y1 = constant(1.0)

    def __call__(self, cvs, t=0.0):
        x, y, thickness, color, lineType = self.basic_transforms(cvs, t)
        x1 = cvs.transform_x(self.x1(t))
        y1 = cvs.transform_y(self.y1(t))

        args = (x,y), (x1, y1), color, thickness, lineType
        cvs.cv2_draw(cv2.rectangle, args, blend=self.blend(t))


class line(artist):

    x1 = constant(1.0)
    y1 = constant(1.0)
    thickness = constant(0.1)

    def __call__(self, cvs, t=0.0):
        x, y, thickness, color, lineType = self.basic_transforms(cvs, t)
        x1 = cvs.transform_x(self.x1(t))
        y1 = cvs.transform_y(self.y1(t))

        args = (x,y), (x1, y1), color, thickness, lineType
        cvs.cv2_draw(cv2.line, args, blend=self.blend(t))

class ellipse(artist):

    a = constant(2.0)
    b = constant(1.0)
    
    rotation = constant(0.0)
    angle_start = constant(0.0)
    angle_end = constant(2*np.pi)

    def __call__(self, cvs, t=0.0):
        x, y, thickness, color, lineType = self.basic_transforms(cvs, t)

        a = cvs.transform_length(self.a(t))
        b = cvs.transform_length(self.b(t))
        
        rotation = cvs.transform_angle(self.rotation(t))
        angle_start = cvs.transform_angle(self.angle_start(t))
        angle_end = cvs.transform_angle(self.angle_end(t))

        args = ((x,y), (a, b),
                rotation, angle_start, angle_end, color, thickness, lineType)

        cvs.cv2_draw(cv2.ellipse, args, blend=self.blend(t))

if __name__== "__main__":
    c = canvas.Canvas()

    circle(x=1,color='r')(c,t=0.5)
    circle(x=-1,color='b')(c)
    rectangle(x=-3,y=-3,color='g')(c)
    line(x=-3,y=-3,color='g')(c)
    ellipse(color='purple')(c)

    c.show()

    
