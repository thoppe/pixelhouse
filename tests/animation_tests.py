from nose.tools import *

import pixelhouse as ph
import numpy as np


class Animation_Test:
    def simple_all_frames_the_same_test(self):

        """ simple_all_frames_the_same_test:
            Draw a circle and make sure all frames are the same
        """

        canvas = ph.Animation()
        canvas += ph.circle()
        canvas.render_all()

        for rhs in canvas.frames[1:]:
            assert_true((rhs.img == canvas.frames[0].img).all())

    def something_moved_test(self):

        """ something_moved_test:
            Draw a circle and make sure it moved
        """

        canvas = ph.Animation()

        x = np.linspace(0, 1, 10)
        canvas += ph.circle(x=x)
        canvas.render_all()

        for rhs in canvas.frames[1:]:
            assert_true((rhs.img != canvas.frames[0].img).any())
