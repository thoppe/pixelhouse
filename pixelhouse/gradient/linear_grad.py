import itertools
import numpy as np
import cv2
from ..artist import Artist, constant, constant_list
from ..primitives import _DEFAULT_COLOR, _DEFAULT_SECONDARY_COLOR
from ..color import interpolation


class linear(Artist):
    colors = constant_list(_DEFAULT_COLOR, _DEFAULT_SECONDARY_COLOR)
    transparency = constant_list(None, None)
    theta = constant(0.0)
    interpolation = constant("LAB")

    args = ("colors", "transparency", "theta", "interpolation")

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

        # Read/transform the colors, apply transparency if needed

        colors = []
        ITR = itertools.zip_longest(
            self.colors(t), self.transparency(t), fillvalue=None
        )

        for c, z in ITR:
            cval = cvs.transform_color(c).copy()
            if z is not None:
                cval[-1] = (np.clip(z, 0, 1) * 255).astype(np.uint8)
            colors.append(cval)

        theta = self.theta(t)
        A = np.array([np.cos(theta), np.sin(theta)])

        # Project each masked grid point onto the angle mapped by theta
        xg, yg = cvs.grid_points()
        B = np.vstack([xg[mask_idx], yg[mask_idx]])

        pro = A.dot(B)
        pro -= pro.min()
        pro /= pro.max()

        # Smooth the image based off the alpha from the mask image
        alpha = (mask.alpha / 255.0)[mask_idx]

        imode = self.interpolation(t)
        if imode == "LAB":
            C = interpolation.LABa_interpolation(pro, alpha, colors)
        elif imode == "RGB":
            C = interpolation.RGBa_interpolation(pro, alpha, colors)
        elif imode == "discrete":
            C = interpolation.discrete_interpolation(pro, alpha, colors)
        else:
            raise KeyError(f"Unknown interpolation {imode}")

        # Blend the new shape in
        rhs = cvs.copy()
        rhs.img[mask_idx] = C
        cvs.blend(rhs)
