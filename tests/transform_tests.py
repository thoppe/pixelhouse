from nose.tools import *

import pixelhouse as ph
from pixelhouse import circle, line, ellipse, rectangle, text, polyline
from pixelhouse.transform import scale


class Transform_Test:

    """ Ensuring transforms work
    """

    def setup(self):
        self.canvas = ph.Canvas(width=200, height=200)
        self.canvas += rectangle(
            **{"x": 0.5, "y": 0.25, "x1": 0.75, "y1": 0.75}
        )

    def scale_up_test(self):

        """ scale_up_test:
            After scaling by 2x, it should be 400 pixels.
        """

        assert_true(self.canvas.width == 200)
        assert_true(self.canvas.height == 200)
        self.canvas(scale(fx=2, fy=2))
        assert_true(self.canvas.width == 400)
        assert_true(self.canvas.height == 400)

    def scale_down_test(self):

        """ scale_down_test:
            After scaling by .5x, it should be 100 pixels.
        """

        assert_true(self.canvas.width == 200)
        assert_true(self.canvas.height == 200)
        self.canvas(scale(fx=0.5, fy=0.5))
        assert_true(self.canvas.width == 100)
        assert_true(self.canvas.height == 100)


class Transform_AnyEffect_Test:

    """ Ensuring other transforms work by checking if something was changed.
    Most basic test, and does not guarantee correctness.
    """

    def setup(self):
        kwargs = {
            "width": 200,
            "height": 200,
            "extent": 4.0,
            "bg": "black",
            "shift": 8,
        }

        self.source = ph.Canvas(**kwargs)
        self.source += ph.circle(x=1, y=-0.5, color=[50, 75, 100, 100])
        self.target = self.source.copy()

    def teardown(self):
        assert_true(~(self.source.img == self.target.img).all())

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
