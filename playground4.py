# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Artist
from pixelhouse import Canvas, Animation, circle, motion,rectangle, line, ellipse
from pixelhouse.transform.simple import translate, rotate
from pixelhouse.transform.elastic import distort, pull, motion_lines

#A = Canvas(width=300, height=300)
#A = Animation(width=300, height=300, fps=25)
A = Animation(width=400, height=400)

A(circle(r=0.5, color='darkorange'))
A(circle(r=0.4, color='w', mode='direct'))

z = motion.easeInOutQuad(0, 2*np.pi, len(A))()

A(motion_lines(0.2, theta=z))
A(motion_lines(0.2))

A(rotate(z))


A.show()
