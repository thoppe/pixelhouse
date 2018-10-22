import numpy as np
import scipy
import canvas
import cv2
import itertools


_default_color = 'white'


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




#############################################################################
def canvas_transform(fn):
    '''
    Decorator to apply to artists. These transforms will be applied 
    automatically if the artist has the attribute. i.e. "x" will be 
    transformed if it exists within the class.
    '''
    transforms = {
            'x' : 'transform_x',
            'y' : 'transform_y',
            'r' : 'transform_length',
            'color' : 'transform_color',
            'thickness' : 'transform_thickness',
            'antialiased' : 'get_lineType',
    }
    
    def wrapper(art, cvs, t=0.0, **kw):

        for key, func_name in transforms.items():
            if hasattr(art, key):
                func = getattr(cvs, func_name)
                key_func = getattr(art, key)
                kw[key] = func(key_func(t))

        return fn(art, cvs, t, **kw)
    
    return wrapper

class circle(artist):

    x = constant(0.0)
    y = constant(0.0)
    r = constant(1.0)
    color = constant(_default_color)
    thickness = constant(-1)
    blend = constant(True)
    antialiased = constant(True)

    def __call__(self, cvs, t=0.0):

        x = cvs.transform_x(self.x(t))
        y = cvs.transform_y(self.y(t))
        r = cvs.transform_length(self.r(t))
        thickness = cvs.transform_length(self.thickness(t))
        lineType = cvs.get_lineType(self.antialiased(t))
        color=cvs.transform_color(self.color(t))
        
        args = (x,y), r, color, thickness, lineType
        cvs.cv2_draw(cv2.circle, args, blend=self.blend(t))

class rectangle(artist):

    x0 = constant(0.0)
    y0 = constant(0.0)
    x1 = constant(1.0)
    y1 = constant(1.0)
    color = constant(_default_color)
    thickness = constant(-1)
    blend = constant(True)
    antialiased = constant(True)

    def __call__(self, cvs, t=0.0):
        x0 = c.transform_x(self.x0(t))
        x1 = c.transform_x(self.x1(t))
        y0 = c.transform_y(self.y0(t))
        y1 = c.transform_y(self.y1(t))

        thickness = c.transform_length(self.thickness(t))
        lineType = c.get_lineType(self.antialiased(t))
        color=c.transform_color(self.color(t))

        args = (x0,y0), (x1, y1), color, thickness, lineType
        cvs.cv2_draw(cv2.rectangle, args, blend=self.blend(t))

if __name__== "__main__":
    c = canvas.canvas()

    circle(x=1,color='r')(c,t=0.5)
    circle(x=-1,color='b')(c)

    rectangle(x0=-3,y0=-3,color='g')(c)

    c.show()
    
