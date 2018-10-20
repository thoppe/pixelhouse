# A working file to test various aspects of the module
from canvas import canvas, circle
from pixelhouse.filter.filters import *
c = canvas()

circle(c, -1, color='b', blend=False)
circle(c, color='r', blend=False)


c.show()
