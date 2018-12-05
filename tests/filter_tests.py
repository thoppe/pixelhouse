from nose.tools import *
import pixelhouse as ph

from utils import AnyEffect_Test
import numpy as np


class Filter_AnyEffect_Test(AnyEffect_Test):

    """ Ensuring other transforms work by checking if something was changed.
    Most basic test, and does not guarantee correctness.
    """

    def gaussian_blur_test(self):
        self.target += ph.filters.gaussian_blur()

    def instagram_test(self):
        self.target += ph.filters.instafilter("1977")

class Instagram_Specific_Test():

    @raises(KeyError)
    def missing_filter_test(self):
        canvas = ph.Canvas()
        canvas += ph.filters.instafilter("not_a_filter")

    def zero_weight_test(self):
        C0 = ph.Canvas()
        C0 += ph.circle(color=[20,30,40,50])

        C1 = C0.copy()
        C1 += ph.filters.instafilter("1977", weight=0)

        # Check that they are equal
        assert_true(np.isclose(C0.img, C1.img).all())
        
