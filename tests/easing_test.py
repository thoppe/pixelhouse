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

