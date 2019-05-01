import numpy as np
import cv2
from ..artist import Artist, constant
import warnings


class gaussian_blur(Artist):
    blur_x = constant(0.2)
    blur_y = constant(0.2)

    args = ("blur_x", "blur_y")

    def draw(self, cvs, t=0.0):
        bx = cvs.transform_kernel_length(self.blur_x(t))
        by = cvs.transform_kernel_length(self.blur_y(t))
        kernel = (bx, by)

        cvs.img = cv2.GaussianBlur(cvs.img, kernel, 0)


class glow(Artist):

    glow_x = constant(2.0)
    glow_y = constant(1.0)
    n = constant(5)
    art = None
    
    args = ("art", "glow_x", "glow_y", "n")

    def draw(self, cvs, t=0.0):

        cvs += self.art

        if self.n(t)==0:
            return True

        gx, gy = self.glow_x(t), self.glow_y(t)

        print(gx, gy)

        

        with cvs.layer() as C:
            for i in range(self.n(t)):
                
                C += gaussian_blur(self.glow_x(t), self.glow_y(t))
                C += self.art
    
