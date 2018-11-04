# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Canvas, circle
from pixelhouse.gradient.gradient import fill 

c1 = Canvas(width=400, height=400, bg='white')
circle(color='purple')(c1)


c2 = Canvas(width=400, height=400, bg='white')
fill(color='red')(c2, mask=c1.mask)


#c2._img[c.mask] = [155,155,155,255]
#print(c.img)
#exit()

c2.show()
