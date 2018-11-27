import numpy as np
import cv2
from ..artist import Artist, constant


class scale(Artist):
    fx = constant(0.5)
    fy = constant(None)
    args = ("fx", "fy")

    def draw(self, cvs, t=0.0):

        fx, fy = self.fx(t), self.fy(t)
        if fy is None:
            fy = fx

        cvs.img = cv2.resize(cvs.img, (0, 0), fx=fx, fy=fy)


class translate(Artist):
    x = constant(0.5)
    y = constant(0.0)
    args = ("x", "y")

    def draw(self, cvs, t=0.0):
        x = cvs.transform_length(self.x(t))
        y = cvs.transform_length(self.y(t))
        bg = cvs.transform_color(cvs.bg)

        M = np.float32([[1, 0, x], [0, 1, y]])
        cvs.img = cv2.warpAffine(cvs.img, M, cvs.shape[:2], borderValue=bg)


class rotate(Artist):

    """ Rotates a canvas by a given amount.
        I hope you like radians.
        Example: canvas(rotate(1.5708)) rotates by 90 degrees
    """

    theta = constant(np.pi / 4)
    x = constant(0.0)
    y = constant(0.0)
    args = ("theta", "x", "y")

    def draw(self, cvs, t=0.0):
        theta = cvs.transform_angle(self.theta(t))
        x = cvs.transform_x(self.x(t))
        y = cvs.transform_y(self.y(t))
        bg = cvs.transform_color(cvs.bg)

        cols, rows = cvs.shape[:2]
        M = cv2.getRotationMatrix2D((x, y), theta, 1)
        cvs.img = cv2.warpAffine(cvs.img, M, (cols, rows), borderValue=bg)
