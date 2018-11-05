import numpy as np
import cv2
from ..artist import Artist, constant
from ..primitives import _DEFAULT_COLOR, _DEFAULT_SECONDARY_COLOR
import cv2

def lerp(t, y0, y1, x0=0, x1=1):
    return np.interp(t, [x0, x1], [y0, y1])

def RGBa_interpolation(t, c0, c1, alpha):
    R = lerp(t, c0[0], c1[0])
    G = lerp(t, c0[1], c1[1])
    B = lerp(t, c0[2], c1[2])
    a = lerp(t, c0[3], c1[3])*alpha
    return np.vstack([R,G,B,a]).T

def LABa_interpolation(t, c0, c1, alpha):
    # Slice off the alpha channel
    a_start, c0 = c0[3], c0[:3]
    a_final, c1 = c1[3], c1[:3]

    # Convert colors to LAB    
    C = np.array([c0,c1]).astype(np.uint8).reshape((2,1,3))
    c0, c1 = cv2.cvtColor(C, cv2.COLOR_RGB2LAB).reshape(2,3)

    # Interpolate in LAB space
    L = lerp(t, c0[0], c1[0])
    A = lerp(t, c0[1], c1[1])
    B = lerp(t, c0[2], c1[2])
    
    # Convert back to RGB
    C = np.vstack([L,A,B]).T.reshape(-1,1,3).astype(np.uint8)
    C = cv2.cvtColor(C, cv2.COLOR_LAB2RGB).reshape(-1,3)

    # Add back in the weighted alpha channel
    a = lerp(t, a_start, a_final)
    a = np.clip(a*alpha, 0, 255).astype(np.uint8)

    # Stack them all together
    C = np.hstack([C,a.reshape(-1,1)])

    return C
    

class linear_gradient(Artist):
    color0 = constant(_DEFAULT_COLOR)
    color1 = constant(_DEFAULT_COLOR)
    theta = constant(np.pi/4)

    args = ('color0', 'color1', 'theta')
    
    def __call__(self, cvs, mask, t=0.0):
        # Assume mask is of type Canvas
        mask_idx = mask.alpha > 0

        theta = self.theta(t)
        A = np.array([np.cos(theta), np.sin(theta)])

        # Project each masked grid point onto the angle mapped by theta
        xg, yg = cvs.grid_points()
        B = np.vstack([xg[mask_idx], yg[mask_idx]])

        pro = A.dot(B)
        pro -= pro.min()
        pro /= pro.max()

        c0 = cvs.transform_color(self.color0(t))
        c1 = cvs.transform_color(self.color1(t))

        # Smooth the image based off the alpha from the mask image
        alpha = (mask.alpha/255.0)[mask_idx]

        # RGBA interpolation (not great!)
        #C = RGBa_interpolation(pro, c0, c1,alpha)

        # LAB interpolation (better!)
        C = LABa_interpolation(pro, c0, c1,alpha)
        

        rhs = cvs.copy()
        rhs._img[mask_idx] = C

        cvs.overlay(rhs)

