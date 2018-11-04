# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Canvas, circle
from pixelhouse.gradient.gradient import linear_gradient 

sx = 400

c1 = Canvas(width=sx, height=sx, bg='white')
circle(color='purple')(c1)

c2 = Canvas(width=sx, height=sx, bg='white')

linear_gradient(color0='black')(c2, mask=c1)

#c2._img[c.mask] = [155,155,155,255]
#print(c.img)
#exit()

c2.show()
