from nose.tools import *

from pixelhouse import Canvas, Animation
from pixelhouse import circle, line, ellipse, rectangle, text, polyline
#from pixelhouse.color import matplotlib_colors, ColorLoversPalette
#from pixelhouse.filter import instafilter
#from pixelhouse.transform import scale
#import pixelhouse.motion as motion


class Primitive_Test:
    '''
    Right now, we just make sure the commands do not fail. The
    output images _could_ be checked against a hash.
    '''

    @classmethod
    def setup_class(cls):
        pass

    def circle_test(self):
        C = Canvas()
        C += circle()
        assert_true(C._img.sum() > 0)

    def ellipse_test(self):
        C = Canvas()
        C += ellipse()
        assert_true(C._img.sum() > 0)

    def polyline_test(self):
        C = Canvas()
        C += polyline()
        assert_true(C._img.sum() > 0)

    def line_test(self):
        C = Canvas()
        C += line()
        assert_true(C._img.sum() > 0)

    def rectange_test(self):
        C = Canvas()
        C += rectangle()
        assert_true(C._img.sum() > 0)

    def text_test(self):
        C = Canvas()
        C += text()
        assert_true(C._img.sum() > 0)
