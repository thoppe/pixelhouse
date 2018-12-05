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

    def check_extent_test(self):

        """ check_extent_test:
            Check the extent/sides and make sure the properties function
        """

        A = ph.Animation(200, 100, extent=2.0)

        assert_equal(A.xmin, -2)
        assert_equal(A.xmax, 2)

        assert_equal(A.ymax, -1)
        assert_equal(A.ymin, 1)

        assert_equal(A.aspect_ratio, 2)

    def iadd_test(self):

        """ iadd_test:
            Add two animations together, check if the duration is twice as long.
        """

        A1 = ph.Animation()
        A2 = ph.Animation()

        A3 = A1.blank()
        A3 += A2

        assert_equal(A3.duration, A1.duration + A2.duration)

    @raises(TypeError)
    def iadd_wrong_type_test(self):

        """ iadd_wrong_type_test:
            Add animation to an int, expect TypeError
        """
        A = ph.Animation()
        A += 7

    def layer_test(self):
        """ layer_test:
            Tests ONLY if the API is working, not a complete test.
        """

        A = ph.Animation()
        A += ph.circle(color="r")
        with A.layer() as AX:
            AX += ph.circle(y=1, color="b")
            AX += ph.transform.translate(x=1)

        A.render_all()
