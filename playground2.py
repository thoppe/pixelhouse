# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Artist
from pixelhouse import Canvas, Animation, circle, motion
from pixelhouse.transform.simple import translate, rotate
from pixelhouse.transform.elastic import distort

A = Canvas()
A = Animation(duration=2, fps=15)

A(circle(x=0, color='w'))
A(circle(x=-1, r=0.25, color='purple'))

theta = motion.easeReturn('easeInOutQuad', 0, np.pi, len(A))
print(theta)
A(rotate(theta=theta))

z = motion.easeReturn('easeInOutQuad', 0, 10, len(A))
print(z)
A(distort(seed=42, sigma=0.05, alpha=z))


A.show()
#c1.show()
#print(c1.shape)
