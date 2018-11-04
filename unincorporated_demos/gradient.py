# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Canvas, circle
from pixelhouse.gradient import linear_gradient 

sx = 400

c1 = Canvas(width=sx, height=sx, bg='white')
circle(color='purple')(c1)

c2 = Canvas(width=sx, height=sx, bg='purple')
linear_gradient(color0='black', color1=[255,255,255,55])(c2, mask=c1)

c2.show()
