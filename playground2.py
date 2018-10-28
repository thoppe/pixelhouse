# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Canvas, Animation, circle, rectangle
from pixelhouse.filter import gaussian_blur
from pixelhouse.filter import instafilter

c1 = Canvas(width=400, height=400, bg='white')
c1.load('pixelhouse/filter/insta/samples/Normal.jpg')

#circle(x=0, color='r')(c1)
F = instafilter('Ludwig')
F(c1)

c1.show()
