import numpy as np
import cv2
from ..artist import Artist, constant
import warnings

class translate(Artist):
    dx = constant(0.5)
    dy = constant(0.0)
    
    def __call__(self, cvs, t=0.0):
        dx = cvs.transform_length(self.dx(t))
        dy = cvs.transform_length(self.dy(t))
        
        M = np.float32([[1,0,dx],[0,1,dy]])
        cvs._img =  cv2.warpAffine(cvs.img, M, cvs.shape[:2])
    
