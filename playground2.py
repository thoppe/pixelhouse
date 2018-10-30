# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Artist
from pixelhouse import Canvas, Animation, circle, motion
from pixelhouse.transform.simple import translate, rotate
from pixelhouse.transform.elastic import distort

c1 = Canvas(width=400, height=400)
A = Animation(duration=2, fps=15)

#circle(x=0, color='w')(c1)
#translate()(c1)
#circle(x=-1, r=0.25, color='purple')(c1)
#rotate()(c1)
#distort(seed=42, sigma=0.03)(c1)


A(circle(x=0, color='w'))
A(circle(x=-1, r=0.25, color='purple'))

#theta = motion.offsetEase(lag, stop=2*np.pi, duration=len(A))()
theta = motion.easeReturn('easeInOutQuad', 0, np.pi, len(A))
A(rotate(theta=theta))

z = motion.easeReturn('easeInOutQuad', 0, 10, len(A))
A(distort(seed=42, sigma=0.05, alpha=z))

A.show()
#c1.show()
#print(c1.shape)
