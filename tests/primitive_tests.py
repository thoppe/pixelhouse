from nose.tools import *

from utils import AnyDraw_Test
import pixelhouse as ph
import itertools

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

class Primitive_Error_Catching_Test():

    @raises(NotImplementedError)
    def polyline_gradient_test(self):
        g = ph.gradient.linear('r', 'g')
        canvas = ph.Canvas()
        canvas += ph.polyline(gradient=g)

    @raises(FileNotFoundError)
    def font_file_missing_test(self):
        canvas = ph.Canvas()
        canvas += ph.text(font="missing_font.otf")    
        
    @raises(ValueError)
    def text_vpos_error_test(self):
        canvas = ph.Canvas()
        canvas += ph.text(vpos="not_a_position")

    @raises(ValueError)
    def text_hpos_error_test(self):
        canvas = ph.Canvas()
        canvas += ph.text(hpos="not_a_position")
        

class Primitive_Text_Options_Test():

    def text_vpos_test(self):
        C0 = ph.Canvas()
        C1 = ph.Canvas()
        C2 = ph.Canvas()
        
        C0 += ph.text(vpos="center")
        C1 += ph.text(vpos="upper")
        C2 += ph.text(vpos="lower")

        # Now check that none of them are equal
        for x, y in itertools.combinations([C0, C1, C2], r=2):
            assert_false((x.img == y.img).all())
    
    def text_hpos_test(self):
        C0 = ph.Canvas()
        C1 = ph.Canvas()
        C2 = ph.Canvas()
        
        C0 += ph.text(hpos="center")
        C1 += ph.text(hpos="left")
        C2 += ph.text(hpos="right")

        # Now check that none of them are equal
        for x, y in itertools.combinations([C0, C1, C2], r=2):
            assert_false((x.img == y.img).all())
    
    def text_gradient_test(self):
        pal = ph.palette(15)

        C0 = ph.Canvas()
        C0 += ph.text(color=pal[0])

        C1 = ph.Canvas()
        C1 += ph.text(color=pal[1])
        
        g = ph.gradient.linear(pal[0], pal[1])

        #C2 = ph.Canvas()
        #C2 += ph.text(gradient=g)

        # Now check that none of them are equal
        #for x, y in itertools.combinations([C0, C1, C2], r=2):
        #    assert_false((x.img == y.img).all())
