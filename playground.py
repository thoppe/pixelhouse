# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Canvas, Animation, circle
from pixelhouse.filter import gaussian_blur

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
