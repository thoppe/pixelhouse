from scipy.ndimage.interpolation import map_coordinates
from scipy.ndimage.filters import gaussian_filter
import numpy as np

import cv2
from ..artist import Artist, constant

class distort(Artist):
    sigma = constant(0.1)
    alpha = constant(10.0)
    mode = constant("constant")
    seed = constant(None)

    args = ("sigma", "alpha", "mode", "seed")
    
    def __call__(self, cvs, t=0.0):

        sigma = cvs.transform_length(self.sigma(t))
        alpha = cvs.transform_length(self.alpha(t), is_discrete=False)
        # https://gist.github.com/erniejunior/601cdf56d2b424757de5
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

