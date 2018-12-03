from nose.tools import *
import pixelhouse as ph


class AnyDraw_Test:
    """
    Utility testing class. Has a special setup and teardown to check if
    _anything_ was done to the self.canvas
    """

    def setup(self):
        kwargs = {
            "width": 200,
            "height": 200,
            "extent": 4.0,
            "bg": "black",
            "shift": 8,
        }
        self.canvas = ph.Canvas(**kwargs)

    def teardown(self):
        assert_true(self.canvas.img.sum() > 0)


class AnyEffect_Test:
    """
    Utility testing class. Has a special setup and teardown to check if
    the starting and ending canvas are the same. Useful for checking
    transforms and filters.
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
        self.source += ph.rectangle(x=-1, y=0.5, color=[70, 75, 100, 100])
        self.target = self.source.copy()

    def teardown(self):
        assert_true(~(self.source.img == self.target.img).all())
