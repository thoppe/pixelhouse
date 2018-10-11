import cv2
import functools
import collections
import inspect
import numpy as np


def parametrized_decorator(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer

@parametrized_decorator
def explicit_default_arguments(gn, fn):
    
    def wrapped(self, *args, **kwargs):
        
        params = collections.OrderedDict(
            inspect.signature(fn).parameters)

        del params["self"]

        # Set the default arguments
        for k, v in params.items():
            params[k] = params[k].default

        # Set the positional arguments
        for k, arg in zip(params.keys(), args):
            params[k] = arg

        # Set the keyword arguments
        for k,v in kwargs.items():
            params[k] = v

        return gn(self, **params)
        
    return wrapped


def transform_coordinates(fn):
    
    @explicit_default_arguments(fn)
    def wrapped(self, **kwargs):
        x, y = kwargs['x'], kwargs['y']
        
        x *= self.width / 2.0
        x /= self.extent
        x += self.width / 2

        y *= -self.height / 2.0
        y /= self.extent
        y += self.height / 2

        kwargs['x'] = int(x)
        kwargs['y'] = int(y)
        
        return fn(self, **kwargs)
    
    return wrapped

@parametrized_decorator
def transform_lengths(fn, *variable_names):
    
    @explicit_default_arguments(fn)
    def wrapped(self, *args, **kwargs):
        print("HERE", args, kwargs)
        for name in variable_names:
            if name not in kwargs:
                raise KeyError(f"Decorator expects {name}")
            
            print(name, kwargs)
        exit()
        return fn(self, **kwargs)
    
    return wrapped


'''
@parametrized_decorator
def transform_lengths(fn, *adjusted_variables):

    def wrapped(self, r=2, *args, **kwargs):

        for q in adjusted_variables:
            print(q, args, kwargs)
        print("WRAPPED", args, kwargs, adjusted_variables)
        
        
        exit()
        
        x *= self.width / 2.0
        x /= self.extent
        x += self.width / 2

        y *= -self.height / 2.0
        y /= self.extent
        y += self.height / 2

        return fn(self, x=int(x), y=int(y), *args, **kwargs)
    return wrapped
'''

class canvas():
    '''
    Canvas object for quad drawings. Extent measures along the x-axis.
    '''

    def __init__(
            self,
            width=400,
            height=200,
            extent=4.0,
            name='quadImage',
    ):
        self.img = np.zeros((height, width, 3), np.uint8)
        self.name = name
        self.extent = extent
        

    def __repr__(self):
        return f"Quad Image {self.height}x{self.width}, extent {self.extent}"

    @property
    def height(self):
        return self.img.shape[0]

    @property
    def width(self):
        return self.img.shape[1]

    def show(self):
        cv2.imshow(self.name, self.img)
        cv2.waitKey(0)

    @transform_lengths('r')
    @transform_coordinates
    def circle(self, x=0, y=0, r=20, color=[255,255,255]):
        print("RADIUS", r)
        cv2.circle(self.img, (x, y), r, color, -1)

c = canvas()
img = c.circle(1, y=2)

#c.show()


