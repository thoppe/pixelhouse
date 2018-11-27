from nose.tools import *
import pixelhouse as ph
from utils import AnyEffect_Test

class Filter_AnyEffect_Test(AnyEffect_Test):

    """ Ensuring other transforms work by checking if something was changed.
    Most basic test, and does not guarantee correctness.
    """
    def gaussian_blur_test(self):
        self.target += ph.filters.gaussian_blur()
        
    def instagram_test(self):
        self.target += ph.filters.instafilter('1977')
