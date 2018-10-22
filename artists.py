import numpy as np
import scipy
import canvas
import cv2


_default_color = 'white'
        
def circle(c, x=0, y=0, r=1, color=_default_color,
        thickness=-1, antialiased=True, blend=True, layer=None):

    x, y = c.transform_coordinates(x, y)
    r = c.transform_length(r)
    thickness = c.transform_length(thickness)
    lineType = c.get_lineType(antialiased)
    color=c.transform_color(color)

    args = (x,y), r, color, thickness, lineType
    c.append(cv2.circle, args, blend=blend, layer=None)


def rectangle(c, x0=0, y0=0, x1=1, y1=1, color=_default_color,
              thickness=-1, antialiased=True, blend=True, layer=None):

    x0, y0 = c.transform_coordinates(x0, y0)
    x1, y1 = c.transform_coordinates(x1, y1)
    thickness = c.transform_length(thickness)
    lineType = c.get_lineType(antialiased)
    color=c.transform_color(color)

    args = (x0,y0), (x1, y1), color, thickness, lineType
    c.append(cv2.rectangle, args, blend=blend, layer=layer)

def line(c, x0=0, y0=0, x1=1, y1=1, color=_default_color,
         thickness=1, antialiased=True, blend=True, layer=None):

    x0, y0 = c.transform_coordinates(x0, y0)
    x1, y1 = c.transform_coordinates(x1, y1)
    thickness = c.transform_length(thickness)
    lineType = c.get_lineType(antialiased)
    color=c.transform_color(color)

    args = (x0,y0), (x1, y1), color, thickness, lineType
    c.append(cv2.line, args, blend=blend, layer=None)

def ellipse(c, x=0, y=0,
            major_length=1, minor_length=1,
            rotation=0,
            angle_start=0,
            angle_end=2*np.pi,
            color=_default_color,
            thickness=-1,
            antialiased=True,
            blend=True,
            layer=None,
):
    # Angles measured in radians

    x, y = c.transform_coordinates(x, y)
    major_length = c.transform_length(major_length)
    minor_length = c.transform_length(minor_length)
    thickness = c.transform_length(thickness)
    lineType = c.get_lineType(antialiased)
    color=c.transform_color(color)

    rotation_degree = c.transform_angle(rotation)
    start_degree = c.transform_angle(angle_start)
    end_degree = c.transform_angle(angle_end)


    args = ((x,y), (major_length, minor_length),
            rotation_degree, start_degree, end_degree,
            color, thickness, lineType)

    c.append(cv2.ellipse, args, blend=blend, layer=layer)


def background(c, color=_default_color):
    ### This doesn't work yet!
    raise NotImplementedError


class artist():
    
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

    def __init__(self, **kwargs):
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


#############################################################################

def constant(x):
    def func(self, t):
        return x
    return func

class animated_circle(artist):

    x = y = constant(0.0)
    r = constant(1.0)
    color = constant([255,255,255])
    thickness = constant(-1)

    def __call__(self, t, img=None):
        
        circle(
            img,
            self.x(t), self.y(t), self.r(t),
            self.color(t), self.thickness(t)
        )

class animated_ellipse(artist):

    x = y = constant(0.0)
    major_length = constant(1.0)
    minor_length = constant(1.0)
    rotation = constant(0.0)
    angle_start = constant(0.0)
    angle_end = constant(2*np.pi)

    color = constant([255,255,255])
    thickness = constant(-1)

    def __call__(self, t, img=None):
        
        ellipse(
            img,
            x=self.x(t),
            y=self.y(t),
            major_length=self.major_length(t),
            minor_length=self.minor_length(t),
            angle_start=self.angle_start(t),
            angle_end=self.angle_end(t),
            color=self.color(t),
            thickness=self.thickness(t),
        )

class animated_line(artist):

    x0 = y0 = constant(0.0)
    x1 = y1 = constant(1.0)

    color = constant([255,255,255])
    thickness = constant(0.1)

    def __call__(self, t, img=None):
        
        line(
            img,
            self.x0(t), self.y0(t),
            self.x1(t), self.y1(t), 
            self.color(t), self.thickness(t)
        )

