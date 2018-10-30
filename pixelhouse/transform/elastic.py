from scipy.ndimage.interpolation import map_coordinates
from scipy.ndimage.filters import gaussian_filter
import numpy as np

import cv2
from ..artist import Artist, constant

class pull(Artist):
    x = constant(0.0)
    y = constant(0.0)
    sigma = constant(1.0)
    alpha = constant(1.0)
    mode = constant("constant")
    args = ("x", "y", "sigma", "alpha", "mode")
    
    def __call__(self, cvs, t=0.0):
        # https://gist.github.com/erniejunior/601cdf56d2b424757de5
        
        x = cvs.transform_x(self.x(t))
        y = cvs.transform_y(self.y(t))
        alpha = cvs.transform_length(self.alpha(t), is_discrete=False)
        sigma = cvs.transform_length(self.sigma(t))
        mode = self.mode(t)

        shape = cvs.shape        
        
        dx = gaussian_filter(
            [[1,2.,3,4],[2.,3,4,5]], sigma,
            mode=mode, cval=0) * alpha

        print(dx)
        exit()
        
        dy = gaussian_filter(
            (y * 2 - 1,0), sigma,
            mode=mode, cval=0) * alpha

        #print(x,y)
        #print((x*2-1,))
        #print(dx,dy)
        #exit()


        x, y, z = np.meshgrid(
            np.arange(shape[0]),
            np.arange(shape[1]),
            np.arange(shape[2])
        )


        indices = (
            np.reshape(y+dy, (-1, 1)),
            np.reshape(x+dx, (-1, 1)),
            np.reshape(z, (-1, 1)),
        )

        distored_image = map_coordinates(
            cvs.img, indices, order=3, mode='reflect')
        
        cvs._img = distored_image.reshape(cvs.shape)


        


class distort(Artist):
    sigma = constant(0.1)
    alpha = constant(10.0)
    mode = constant("constant")
    seed = constant(None)

    args = ("sigma", "alpha", "mode", "seed")
    
    def __call__(self, cvs, t=0.0):
        # https://gist.github.com/erniejunior/601cdf56d2b424757de5

        sigma = cvs.transform_length(self.sigma(t))
        alpha = cvs.transform_length(self.alpha(t), is_discrete=False)

        shape = cvs.shape
        random_state = np.random.RandomState(self.seed(t))

        mode = self.mode(t)
        
        dx = gaussian_filter(
            (random_state.rand(*shape) * 2 - 1), sigma,
            mode=mode, cval=0) * alpha
        
        dy = gaussian_filter(
            (random_state.rand(*shape) * 2 - 1), sigma,
            mode=mode, cval=0) * alpha

        x, y, z = np.meshgrid(
            np.arange(shape[1]),
            np.arange(shape[0]),
            np.arange(shape[2])
        )


        indices = (
            np.reshape(y+dy, (-1, 1)),
            np.reshape(x+dx, (-1, 1)),
            np.reshape(z, (-1, 1)),
        )

        distored_image = map_coordinates(
            cvs.img, indices, order=3, mode='reflect')
        
        cvs._img = distored_image.reshape(cvs.shape)

