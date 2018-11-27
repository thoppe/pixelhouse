from nose.tools import *

from pixelhouse import Canvas, Animation
from pixelhouse import circle, line, ellipse, rectangle, text, polyline


class Canvas_Test:
    def blank_doesnt_modify_in_place_test(self):

        """ blank_doesnt_modify_in_place_test:
            If the canvas has not had anything painted on it, its sum is 0
            If the canvas has been blanked out, its sum is 0
            Otherwise, its sum should be > 0
        """

        canvas = Canvas()
        assert_true(canvas.img.sum() == 0)
        canvas += circle()
        assert_true(canvas.img.sum() > 0)
        canvas.blank()
        assert_true(canvas.img.sum() > 0)
        assert_true(canvas.blank().img.sum() == 0)
