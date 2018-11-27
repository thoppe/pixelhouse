import numpy as np
import cv2
from ..artist import Artist, constant
import warnings


class gaussian_blur(Artist):
    blur_x = constant(0.1)
    blur_y = constant(0.1)

    args = ("blur_x", "blur_y")

    def draw(self, cvs, t=0.0):
        bx = cvs.transform_kernel_length(self.blur_x(t))
        by = cvs.transform_kernel_length(self.blur_y(t))
        kernel = (bx, by)

        cvs.img = cv2.GaussianBlur(cvs.img, kernel, 0)
