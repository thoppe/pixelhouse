# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Canvas
from pixelhouse.filter import instafilter

c1 = Canvas()
c1.load('pixelhouse/filter/insta/samples/Normal.jpg').rescale(0.25)
F = instafilter('Ludwig')
F(c1)

c1.show()
