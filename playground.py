# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Canvas, Animation, circle
from pixelhouse.filter import gaussian_blur

c1 = Canvas(width=400, height=400)
circle(x=0, color=[255,255,255])(c1)

c2 = c1.blank()
circle(x= 1, color='r')(c2)

c3 = c1.blank()
circle(x=-1, y=0, color='r')(c3)

c4 = c1.blank()
circle(x=0, y=-2, r=0.85,color='r')(c4)

#c1.combine(c2, 'saturate')
#c1.combine(c3, 'desaturate')
c1.combine(c4, 'overlay')
c1.show()
'''
c = Canvas()
A = Animation()

z1 = circle(x=-1, color='b', blend=False)
z2 = circle(color='r', blend=False)

b = np.linspace(0,4,100)
z3 = gaussian_blur(blur_x=b, blur_y=0)

A.add(z1)
A.add(z2)
A.add(z3)
A.show()

c.show()
'''
