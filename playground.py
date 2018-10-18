# A working file to test various aspects of the module
from canvas import canvas
from src.filter.filters import *
c = canvas()

c.circle()
gaussian_blur(c)
c.show()
