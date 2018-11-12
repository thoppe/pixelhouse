# A working file to test various aspects of the module
import numpy as np
from pixelhouse import  Canvas, Animation
from pixelhouse import circle, motion, rectangle, line, ellipse
from pixelhouse.transform.simple import translate, rotate
from pixelhouse.transform.elastic import distort, pull

#A = Canvas(width=300, height=300)
#A = Animation(width=300, height=300, fps=25)
A = Animation(width=300, height=300)

# Draw grid lines
dx = 4
for i in np.arange(-dx, dx, 0.5):
    A += line(i,-dx,i,dx,thickness=0)
    A += line(-dx,i,dx,i,thickness=0)

z = motion.easeInOutQuad(1, -1, len(A))()
x = motion.easeInOutQuad(1, -1, len(A))()
A += pull(x, 0.25, alpha=z, mode='constant')

A.show()
