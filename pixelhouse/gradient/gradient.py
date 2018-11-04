import numpy as np
import cv2
from ..artist import Artist, constant
from ..primitives import _DEFAULT_COLOR, _DEFAULT_SECONDARY_COLOR

class LocalCoordinateArtist(Artist):
    pass

class linear_gradient(LocalCoordinateArtist):
    color0 = constant(_DEFAULT_COLOR)
    color1 = constant(_DEFAULT_COLOR)
    theta = constant(np.pi/4)

    args = ('color0', 'color1', 'theta')
    
    def __call__(self, cvs, t=0.0, mask=None):

        theta = self.theta(t)
        A = np.array([np.cos(theta), np.sin(theta)])

        # Project each masked grid point onto the angle mapped by theta
        xg, yg = cvs.grid_points()
        B = np.vstack([xg[mask], yg[mask]])

        pro = A.dot(B)
        pro -= pro.min()
        pro /= pro.max()

        c0 = cvs.transform_color(self.color0(t))
        c1 = cvs.transform_color(self.color1(t))

        # RGBA interpolation (not great!)
        R = np.interp(pro, [0,1], [c0[0], c1[0]])
        G = np.interp(pro, [0,1], [c0[1], c1[1]])
        B = np.interp(pro, [0,1], [c0[2], c1[2]])
        A = np.interp(pro, [0,1], [c0[3], c1[3]])

        C = np.clip(np.vstack([R,G,B,]).T, 0, 255).astype(np.uint8)

        #color = cvs.transform_color(self.color(t))
        
        cvs._img[mask, :3] = C
