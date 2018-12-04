from nose.tools import *

import pixelhouse as ph
import numpy as np

class Easing_Test:
    def start_test(self):

        """ Check if the start position works
        """
        b = ph.motion.easeInQuad(start=3)
        assert_true(b(0) == 3)
        
    def stop_test(self):

        """ Check if the stop position works
        """
        b = ph.motion.easeInQuad(0,3)
        assert_true(b(1) == 3)
        
    def numpy_test(self):

        """ Check if we can pass a numpy array, take the identity
        easing (the linear) one.
        """
        z = np.linspace(0, 1, 100)
        b = ph.motion.Linear(0,1)
        assert_true((b(z)==z).all())
        
    def neg_test(self):

        """ Check some of the arithmetic on the easing function.
        """
        z = np.linspace(0, 1, 100)
        b = -ph.motion.Linear(0,1)
        
        assert(np.allclose(b(z),-z))

    def add_test(self):

        """ Check some of the arithmetic on the easing function.
        """
        z = np.linspace(0, 1, 100)
        b = 2+ph.motion.Linear(0,1)+3
        
        assert(np.allclose(b(z),2+z+3))

    def sub_test(self):

        """ Check some of the arithmetic on the easing function.
        """
        z = np.linspace(0, 1, 10)
        b = ph.motion.Linear(0,1) - 3
        assert(np.allclose(b(z),z-3))
        
    def mul_test(self):

        """ Check some of the arithmetic on the easing function.
        """
        z = np.linspace(0, 1, 100)
        b = 2*ph.motion.Linear(0,1)*3

        assert(np.allclose(b(z),2*z*3))

    def div_test(self):

        """ Check some of the arithmetic on the easing function.
        """
        z = np.linspace(0, 1, 100)
        b = ph.motion.Linear(0,1)/3.0
        
        assert(np.allclose(b(z),z/3))

    def out_of_range_test(self):

        """ Evaluate the easing outside of the expected range works like mod.
        """
        b = ph.motion.easeInQuad(0,3)
        pt = 0.2

        assert( np.allclose(b(pt),b(1+pt)) )
        assert( np.allclose(b(1-pt),b(-pt)) )
        
    def out_of_range_numpy_test(self):

        """ Evaluate the easing outside of the expected range works like mod.
        """
        z = np.linspace(.01, .99, 27)
        b = ph.motion.easeInQuad(0,3)

        assert( np.allclose(b(z),b(1+z)) )
        assert( np.allclose(b(1-z),b(-z)) )
        
    def get_params_test(self):
        """ Test if the params for easeInQuad come out as expected.
        """
        b = ph.motion.easeInQuad(0,3)

        params = (0.55, 0.085, 0.68, 0.53)
        assert_true(all([p0==p1 for p0, p1 in zip(params, b.get_params())]))

    def flip_test(self):
        """ Test if "flip" is working by evaluating the start and end
        and checking if they both end at zero.
        """
        b = ph.motion.easeInQuad(0,3, flip=True)
        assert_true(b(0) == 0)
        assert_true(b(1) == 0)
        

    @raises(NotImplementedError)
    def init_from_base_class_test(self):
        """ You shouldn't be able to init from the base class.
        """
        b = ph.motion.easing.EasingBase()
        b(.2)
