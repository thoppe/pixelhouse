from canvas import canvas
import src.easing as easing

import cv2
import os
import numpy as np
import scipy.interpolate

import imageio
from tqdm import tqdm

class animation():

    def __init__(
            self,
            duration=5, fps=5,
            width=200, height=200, extent=4
    ):
        
        self.duration = duration
        self.fps = fps
        self.artists = []

        n_frames = int(fps*duration)

        self.frames = [
            canvas(width, height, extent) for _ in
            range(n_frames)
        ]
        self.has_rendered = [False,]*len(self)
        self.timepoints = np.linspace(0, 1, len(self)+1)[:-1]

    def __len__(self):
        return len(self.frames)

    def add(self, art):
        self.artists.append(art)

    def render(self, n):
        assert(0 <= n < len(self))

        if not self.has_rendered[n]:

            t = self.timepoints[n]

            for art in self.artists:
                art(t, self.frames[n])

            self.has_rendered[n] = True

        return self.frames[n]

    def show(self, delay=50, repeat=True):
        while True:
            for n in range(len(self)):
                img = self.render(n)
                img.show(delay=delay)
            if not repeat:
                break

    def to_gif(self, f_gif):
        images = [self.render(n).img for n in range(len(self))]

        # Convert from BGR to RGB
        images = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in images]
        
        imageio.mimsave(f_gif, images, fps=self.fps*2,
                        palettesize=256,  subrectangles=True)
        fs = os.stat(f_gif).st_size
        print(f"Rendered {f_gif}, filesize {fs}")

#############################################################################

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

class circle(artist):

    x = y = constant(0.0)
    r = constant(1.0)
    color = constant([255,255,255])
    thickness = constant(-1)

    def __call__(self, t, img=None):
        
        img.circle(
            self.x(t), self.y(t), self.r(t),
            self.color(t), self.thickness(t)
        )


#############################################################################

if __name__ == "__main__":
    
    A = animation(width=375, height=375, fps=6)

    # Use a cosine to smoothly move back
    t = np.linspace(0,1,len(A))
    x = np.cos(t*2*np.pi)

    # Use an ease function to go in an out
    E = easing.QuadEaseInOut(0, 1, len(A)//2)
    x2 = np.array([E.ease(n) for n in range(len(A)//2)])
    x2 = np.hstack([x2,-(x2-1)])

    A.add(circle(x=x2, y=1, r=1.25,color=[150,250,0]))
    A.add(circle(x=x, y=-1, r=1.25,color=[100,5,255]))


    #A.to_gif("examples/moving_circles.gif")
    #A.show(delay=20, repeat=True)

    A.show(repeat=True)
