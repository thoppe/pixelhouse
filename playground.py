# A working file to test various aspects of the module
from canvas import canvas
from pixelhouse.filter.filters import *
c = canvas()

c.circle(-1, color='b', blend=False)
c.circle(color='r', blend=False)


c.show()
