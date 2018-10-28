# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Canvas, circle, Animation
from pixelhouse.filter import instafilter

c1 = Canvas(bg='w')
c1.load('pixelhouse/filter/insta/samples/Normal.jpg').rescale(0.25)
circle(r=0.50, color='r')(c1)
F = instafilter('Ludwig', weight=0.80)
F(c1)
c1.show()

'''
A = Animation()
x = np.linspace(-1, 1, 100)
c = circle(x=x, r=1.5, color='r')
f = instafilter('Ludwig', weight=(x+1)/2)
A.add(c)
A.add(f)
A.show()
'''
