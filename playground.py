# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Canvas, Animation, circle, rectangle
from pixelhouse.filter import gaussian_blur

c1 = Canvas(width=400, height=400, bg='purple')
circle(x=0, color='w')(c1)

c2 = c1.blank()
circle(x=0, y=2, r=0.7, color='r')(c2)

c3 = c1.blank('w')
circle(x=0, y=-2, r=0.7,color='k')(c3)

gaussian_blur(blur_x=1)(c1)

circle(x=0, color='w')(c1)
circle(x=0, y=2, r=0.7, color='r')(c2)

c1.combine(c3)
c1.combine(c2)
c1.show()
