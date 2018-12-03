from scipy.ndimage.interpolation import map_coordinates
from scipy.ndimage.filters import gaussian_filter
import numpy as np

import cv2
from ..artist import Artist, constant


class ElasticTransform(Artist):
    @staticmethod
    def transform(cvs, dy, dx, coords, mode, order=2):

        xg, yg, zg = coords

        indices = (
            np.reshape(yg + dy, (-1, 1)),
            np.reshape(xg + dx, (-1, 1)),
            np.reshape(zg, (-1, 1)),
        )

        distored_image = map_coordinates(
            cvs.img, indices, order=order, mode=mode
        )

        cvs.img = distored_image.reshape(cvs.shape)


class pull(ElasticTransform):
    x = constant(0.0)
    y = constant(0.0)
    alpha = constant(1.0)
    mode = constant("nearest")
    args = ("x", "y", "sigma", "alpha", "mode")

    def draw(self, cvs, t=0.0):
        # https://gist.github.com/erniejunior/601cdf56d2b424757de5

        x = float(cvs.transform_x(self.x(t)))
        y = float(cvs.transform_y(self.y(t)))
        alpha = cvs.transform_length(self.alpha(t), is_discrete=False)

        coords = cvs.grid_coordinates()

        theta = np.arctan2(coords[1] - y, coords[0] - x)
        dx = alpha * np.cos(theta)
        dy = alpha * np.sin(theta)

        self.transform(cvs, dy, dx, coords, self.mode(t))


class distort(ElasticTransform):
    sigma = constant(0.1)
    alpha = constant(10.0)
    mode = constant("nearest")
    seed = constant(None)

    args = ("sigma", "alpha", "mode", "seed")

    def draw(self, cvs, t=0.0):
        # https://gist.github.com/erniejunior/601cdf56d2b424757de5

        sigma = cvs.transform_length(self.sigma(t))
        alpha = cvs.transform_length(self.alpha(t), is_discrete=False)
        mode = self.mode(t)

        shape = cvs.shape
        random_state = np.random.RandomState(self.seed(t))

        coords = cvs.grid_coordinates()

        dx = random_state.rand(*shape) * 2 - 1
        dy = random_state.rand(*shape) * 2 - 1

        dx = gaussian_filter(dx, sigma, mode=mode)
        dy = gaussian_filter(dy, sigma, mode=mode)

        self.transform(cvs, dy * alpha, dx * alpha, coords, self.mode(t))


class motion_lines(ElasticTransform):
    alpha = constant(0.15)
    theta = constant(0.0)
    mode = constant("constant")
    args = ("alpha", "mode")

    def draw(self, cvs, t=0.0):
        alpha = cvs.transform_length(self.alpha(t), is_discrete=False)

        theta = self.theta(t)
        mode = self.mode(t)

        coords = cvs.grid_coordinates()

        y = cvs.inverse_transform_y(coords[1].astype(float))
        x = cvs.inverse_transform_y(coords[0].astype(float))

        dx = np.cos(theta) * np.abs(x)
        dy = np.sin(theta) * np.abs(y)

        self.transform(cvs, alpha * dy, alpha * dx, coords, self.mode(t))


class wave(ElasticTransform):

    wavelength = constant(0.25)
    amplitude = constant(0.02)
    offset = constant(0.0)
    theta = constant(0.0)
    mode = constant("nearest")
    seed = constant(None)

    args = ("wavelength", "amplitude", "theta", "seed")

    def draw(self, cvs, t=0.0):

        coords = cvs.grid_coordinates()

        y = cvs.inverse_transform_y(coords[1].astype(float))
        x = cvs.inverse_transform_x(coords[0].astype(float))

        theta = self.theta(t)
        w = self.wavelength(t) / (2 * np.pi)

        a = cvs.transform_length(self.amplitude(t), is_discrete=False)

        qx = a * np.cos(x / w + self.offset(t))
        qy = a * np.cos(y / w + self.offset(t))

        # Only square waves for now
        qx[qx > 0] = a
        qx[qx <= 0] = -a

        qy[qy > 0] = a
        qy[qy <= 0] = -a

        dx = np.cos(theta) * qy
        dy = np.sin(theta) * qx

        # Order 0 can be used as this is a glitch effect
        self.transform(cvs, dy, dx, coords, self.mode(t), order=0)
