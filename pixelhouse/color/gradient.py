import numpy as np
import cv2
from ..artist import Artist, constant
from ..primitives import _DEFAULT_COLOR, _DEFAULT_SECONDARY_COLOR
from . import RGBa_interpolation, LABa_interpolation


class linear_gradient(Artist):
    color0 = constant(_DEFAULT_COLOR)
    color1 = constant(_DEFAULT_COLOR)
    theta = constant(np.pi / 4)
    interpolation = constant("LAB")

    args = ("color0", "color1", "theta", "interpolation")

    def __call__(self, cvs, t=0.0, mask=None):
        """
        Assume the mask is of type Canvas. 
        Interpolation can be LAB or RGB.
        Theta controls the angle along the shape.

        If mask is None, return True to show that a gradient exists
        """
        if mask is None:
            return True

        mask_idx = mask.alpha > 0

        # If the mask_idx is 0, image is off the canvas
        if not mask_idx.sum():
            return True

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
        alpha = (mask.alpha / 255.0)[mask_idx]

        imode = self.interpolation(t)
        if imode == "LAB":
            C = LABa_interpolation(pro, c0, c1, alpha)
        elif imode == "RGB":
            # RGBA interpolation (not great!)
            C = RGBa_interpolation(pro, c0, c1, alpha)
        else:
            raise KeyError(f"Unknown interpolation {imode}")

        # Blend the new shape in
        rhs = cvs.copy()
        rhs._img[mask_idx] = C
        cvs.blend(rhs)
