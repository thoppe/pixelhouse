from scipy.ndimage.interpolation import map_coordinates
from scipy.ndimage.filters import gaussian_filter
import numpy as np

import cv2
from ..artist import Artist, constant

class pull(Artist):
    x = constant(0.0)
    y = constant(0.0)
    sigma = constant(0.01)
    alpha = constant(1.0)
    mode = constant("constant")
    args = ("x", "y", "sigma", "alpha", "mode")
    
    def __call__(self, cvs, t=0.0):
        # https://gist.github.com/erniejunior/601cdf56d2b424757de5
        
        x = cvs.transform_x(self.x(t))
        y = cvs.transform_y(self.y(t))
        alpha = cvs.transform_length(self.alpha(t), is_discrete=False)
        sigma = cvs.transform_length(self.sigma(t), is_discrete=False)
        mode = self.mode(t)

        shape = cvs.shape        
        
        xg, yg, zg = np.meshgrid(
            np.arange(shape[1]),
            np.arange(shape[0]),
            np.arange(shape[2])
        )

        #print(cvs.transform_x(xg.astype(np.float64), False))
        #exit()

        dist_pixels = np.sqrt((xg-x)**2 + (yg-y)**2)
        dist = dist_pixels * (cvs.extent/cvs.width)
        amp = np.exp(-dist/sigma**2)
        
        theta = np.arctan2(yg-y, xg-x)
        dx = alpha*amp*np.cos(theta)
        dy = alpha*amp*np.sin(theta)

        indices = (
            np.reshape(yg+dy, (-1, 1)),
            np.reshape(xg+dx, (-1, 1)),
            np.reshape(zg, (-1, 1)),
        )

        distored_image = map_coordinates(
            cvs.img, indices, order=3, mode=mode)
        
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

        xg, yg, zg = np.meshgrid(
            np.arange(shape[1]),
            np.arange(shape[0]),
            np.arange(shape[2])
        )

        displacement_x = random_state.rand(*shape) * 2 - 1
        displacement_y = random_state.rand(*shape) * 2 - 1

        dx = gaussian_filter(
            displacement_x, sigma, mode=mode, cval=0) * alpha
        
        dy = gaussian_filter(
            displacement_y, sigma, mode=mode, cval=0) * alpha


        indices = (
            np.reshape(yg+dy, (-1, 1)),
            np.reshape(xg+dx, (-1, 1)),
            np.reshape(zg, (-1, 1)),
        )

        distored_image = map_coordinates(
            cvs.img, indices, order=3, mode=mode)
        
        cvs._img = distored_image.reshape(cvs.shape)

