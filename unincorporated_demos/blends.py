# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Canvas, circle
from pixelhouse.gradient import linear_gradient 

sx = 400


c0 = Canvas(width=sx, height=sx, bg='white')
circle(x=-3,r=0.25)(c0)

c1 = Canvas(width=sx, height=sx, bg='white')
circle()(c1)


c2 = Canvas(width=sx, height=sx, bg='purple')
linear_gradient(color0='white', color1=[255,255,155,0])(c2, mask=c1)
linear_gradient(color0='red', color1='green')(c2, mask=c0)

c2.show()
