from nose.tools import *
import pixelhouse as ph


class Primitive_AnyDraw_Test:
    """
    Right now, we just make sure the commands do not fail and draw _something_.
    The output images _could_ be checked against a hash in the future.
    """

    def setup(self):
        self.C = ph.Canvas(
            width=200, height=200, extent=4.0, bg="black", shift=8
        )

    def teardown(self):
        assert_true(self.C.img.sum() > 0)

    def circle_test(self):
        self.C += ph.circle()

    def ellipse_test(self):
        self.C += ph.ellipse()

    def polyline_test(self):
        self.C += ph.polyline()

    def line_test(self):
        self.C += ph.line()

    def rectange_test(self):
        self.C += ph.rectangle()

    def text_test(self):
        self.C += ph.text()
