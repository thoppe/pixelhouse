from nose.tools import *
import pixelhouse as ph

class Filter_AnyEffect_Test:

    """ Ensuring other transforms work by checking if something was changed.
    Most basic test, and does not guarantee correctness.
    """

    def setup(self):
        kwargs = {
            "width": 200,
            "height": 200,
            "extent": 4.0,
            "bg": "black",
            "shift": 8,
        }

        self.source = ph.Canvas(**kwargs)
        self.source += ph.circle(x=1, y=-0.5, color=[50, 75, 100, 100])
        self.target = self.source.copy()
        
    def teardown(self):
        assert_true(~(self.source.img == self.target.img).all())

    def gaussian_blur_test(self):
        self.target += ph.filters.gaussian_blur()
        
    def instagram_test(self):
        self.target += ph.filters.instafilter('1977')
