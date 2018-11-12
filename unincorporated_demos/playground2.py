# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Artist
from pixelhouse import Canvas, Animation, circle, motion
from pixelhouse.transform.simple import translate, rotate
from pixelhouse.transform.elastic import distort

A = Canvas()
A = Animation(duration=2, fps=15)

A += circle(color='w')
A += circle(-1, 0, 0.25, color='purple')

theta = motion.easeReturn('easeInOutQuad', 0, np.pi, len(A))
A += rotate(theta)

z = motion.easeReturn('easeInOutQuad', 0, 10, len(A))
A += distort(seed=42, sigma=0.05, alpha=z)

A.show()
