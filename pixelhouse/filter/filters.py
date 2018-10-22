import numpy as np
import cv2

def gaussian_blur(c, pixel_x=51, pixel_y=1):
    kernel = (pixel_x, pixel_y)
    c._img = cv2.GaussianBlur(c.img, kernel, 0)
    return c
    
