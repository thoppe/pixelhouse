from nose.tools import *

from pixelhouse import Canvas, Animation
from pixelhouse import circle, line, ellipse, rectangle, text, polyline
from pixelhouse.transform import scale

class Transform_Test:

    """ Ensuring transforms work
    """

    def setup(self):
        self.canvas = Canvas(width=200, height=200)
        self.canvas += rectangle(**{
                'x': .5,
                'y': .25,
                'x1': .75,
                'y1': .75,
            })

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
        self.canvas(scale(fx=.5, fy=.5))
        assert_true(self.canvas.width == 100)
        assert_true(self.canvas.height == 100)
