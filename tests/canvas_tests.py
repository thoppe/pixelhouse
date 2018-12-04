from nose.tools import *

import numpy as np
import pixelhouse as ph

class Canvas_Test:
    def blank_doesnt_modify_in_place_test(self):

        """ blank_doesnt_modify_in_place_test:
            If the canvas has not had anything painted on it, its sum is 0
            If the canvas has been blanked out, its sum is 0
            Otherwise, its sum should be > 0
        """

        canvas = ph.Canvas()
        assert_true(canvas.img.sum() == 0)
        canvas += ph.circle()
        assert_true(canvas.img.sum() > 0)
        canvas.blank()
        assert_true(canvas.img.sum() > 0)
        assert_true(canvas.blank().img.sum() == 0)
        
    def hstack_test(self):

        """ hstack_test:
            Draw an image, stack it, and make sure it's the same as the
            numpy operation.
        """

        C1 = ph.Canvas()
        C2 = ph.Canvas()
        
        C1 += ph.circle()
        C2 += ph.rectangle()

        # Make sure something was drawn
        assert_true(C1.img.sum() != 0)
        assert_true(C2.img.sum() != 0)

        X = ph.hstack([C1, C2])
        
        img_stack = np.hstack([C1.img, C2.img])
        assert_true(np.isclose(img_stack, X.img).all())

        
        
    def vstack_test(self):

        """ vstack_test:
            Draw an image, stack it, and make sure it's the same as the
            numpy operation.
        """

        C1 = ph.Canvas()
        C2 = ph.Canvas()
        
        C1 += ph.circle()
        C2 += ph.rectangle()

        # Make sure something was drawn
        assert_true(C1.img.sum() != 0)
        assert_true(C2.img.sum() != 0)

        X = ph.vstack([C1, C2])
        
        img_stack = np.vstack([C1.img, C2.img])
        assert_true(np.isclose(img_stack, X.img).all())
        
    def gridstack_test(self):

        """ dstack_test:
            Draw an image, stack it, and make sure it's the same as the
            numpy operation.
        """

        C1 = ph.Canvas()
        C2 = ph.Canvas()
        C3 = ph.Canvas()
        
        C1 += ph.circle()
        C2 += ph.rectangle()
        C3 += ph.circle(x=1)

        # Make sure something was drawn
        assert_true(C1.img.sum() != 0)
        assert_true(C2.img.sum() != 0)
        assert_true(C3.img.sum() != 0)

        X = ph.gridstack([[C1, C2], [C2, C3]])
        
        img_stack = np.vstack(
            [np.hstack([C1.img, C2.img]), np.hstack([C2.img, C3.img])])
        
        assert_true(np.isclose(img_stack, X.img).all())
