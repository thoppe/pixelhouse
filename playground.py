# A working file to test various aspects of the module
from canvas import Canvas
from artists import circle
from pixelhouse.filter.filters import *
c = Canvas()

circle(x=-1, color='b', blend=False)(c)
circle(color='r', blend=False)(c)


c.show()
