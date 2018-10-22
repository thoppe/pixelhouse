import numpy as np
import cv2
from ..artists import Artist, constant
import warnings

class gaussian_blur(Artist):
    blur_x = constant(1)
    blur_y = constant(1)
    
    def __call__(self, cvs, t=0.0):
        bx = self.blur_x(t)
        by = self.blur_y(t)
        kernel = (bx, by)        
                
        cvs._img = cv2.GaussianBlur(cvs.img, kernel, 0)
    
