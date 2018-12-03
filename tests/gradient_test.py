from nose.tools import *

from utils import AnyDraw_Test
import pixelhouse as ph
import numpy as np

class Gradient_Test:
    def draw_with_gradient_test(self):
        """ draw_with_gradient_test:
            Draw discrete gradient and check both colors are present
            in the corners.
        """
        C = ph.Canvas()
        g = ph.gradient.linear(['r', 'b'], interpolation='discrete')
        C += ph.rectangle(C.xmin, C.ymin, C.xmax, C.ymax,
                          gradient=g)

        assert_true((C.transform_color('r') == C.img[0,0]).all())
        assert_true((C.transform_color('b') == C.img[-1,-1]).all())

    @raises(KeyError)
    def check_API_missing_mode_test(self):
        g = ph.gradient.linear(['r', 'b'], interpolation='dsjsdlfkjsd')
        C = ph.Canvas()
        C += ph.circle(gradient=g)

    def check_draw_if_offscreen_is_ok_test(self):
        g = ph.gradient.linear(['r', 'b'])
        C = ph.Canvas()
        C += ph.circle(x=C.xmax+20, y=C.ymax+20, r=1, gradient=g)

        # Check that nothing was drawn
        assert((C.img[:,:,:3] == C.transform_color(C.bg)[:3]).all())


class Gradient_API_Test(AnyDraw_Test):
        
    def check_API_LAB_test(self):
        """ Check if the API for LAB interpolation works.
        """
        g = ph.gradient.linear(['r', 'b'], interpolation='LAB')
        self.canvas += ph.circle(gradient=g)

    def check_API_RGB_test(self):
        """ Check if the API for RGB interpolation works.
        """
        g = ph.gradient.linear(['r', 'b'], interpolation='RGB')
        self.canvas += ph.circle(gradient=g)

    def check_API_discrete_test(self):
        """ Check if the API for RGB interpolation works.
        """
        g = ph.gradient.linear(['r', 'b'], interpolation='discrete')
        self.canvas += ph.circle(gradient=g)

        
