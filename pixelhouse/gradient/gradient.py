import numpy as np
import cv2
from ..artist import Artist, constant
from ..primitives import _DEFAULT_COLOR

class fill(Artist):
    color = constant(_DEFAULT_COLOR)
    mask = constant(None)
    
    def __call__(self, cvs, t=0.0, mask=None):

        color = cvs.transform_color(self.color(t))
        cvs._img[mask] = color
