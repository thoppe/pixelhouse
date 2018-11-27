from utils import AnyDraw_Test
import pixelhouse as ph

class Primitive_AnyDraw_Test(AnyDraw_Test):
    """
    Right now, we just make sure the commands do not fail and draw something.
    The output images could be checked against a hash in the future.
    """

    def circle_test(self):
        self.canvas += ph.circle()

    def ellipse_test(self):
        self.canvas += ph.ellipse()

    def polyline_test(self):
        self.canvas += ph.polyline()

    def line_test(self):
        self.canvas += ph.line()

    def rectange_test(self):
        self.canvas += ph.rectangle()

    def text_test(self):
        self.canvas += ph.text()
