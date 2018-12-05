from nose.tools import *
from utils import AnyEffect_Test

import pixelhouse as ph
from pixelhouse import circle, line, ellipse, rectangle, text, polyline


class Transform_Test:

    """ Ensuring transforms work
    """

    def setup(self):
        self.canvas = ph.Canvas(width=200, height=200)
        self.canvas += rectangle(x=0.5, y=0.25, x1=0.75, y1=0.75)

    def scale_up_test(self):

        """ scale_up_test:
            After scaling by 2x, it should be 400 pixels.
        """

        assert_true(self.canvas.width == 200)
        assert_true(self.canvas.height == 200)
        self.canvas(ph.transform.scale(fx=2, fy=2))
        assert_true(self.canvas.width == 400)
        assert_true(self.canvas.height == 400)

    def scale_down_test(self):

        """ scale_down_test:
            After scaling by .5x, it should be 100 pixels.
        """
        assert_true(self.canvas.width == 200)
        assert_true(self.canvas.height == 200)
        self.canvas(ph.transform.scale(fx=0.5, fy=0.5))
        assert_true(self.canvas.width == 100)
        assert_true(self.canvas.height == 100)


class Transform_AnyEffect_Test(AnyEffect_Test):

    """ Ensuring transforms work by checking if something was changed.
    Most basic test, and does not guarantee correctness.
    """

    def scale_test(self):
        self.target += ph.transform.scale(fx=0.25)

    def rotate_test(self):
        self.target += ph.transform.rotate(theta=1.57)

    def translate_test(self):
        self.target += ph.transform.translate(x=0.1)

    def pull_test(self):
        self.target += ph.transform.pull()

    def distort_test(self):
        self.target += ph.transform.distort()

    def motion_lines_test(self):
        self.target += ph.transform.motion_lines()

    def wave_test(self):
        self.target += ph.transform.wave()
