# A working file to test various aspects of the module
from pixelhouse import Canvas, circle
from pixelhouse.filter import gaussian_blur

c = Canvas()

circle(x=-1, color='b', blend=False)(c)
circle(color='r', blend=False)(c)
gaussian_blur(blur_x=0)(c)

c.show()
