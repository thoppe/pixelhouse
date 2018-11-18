# A working file to test various aspects of the module
import numpy as np
import pixelhouse as ph
from pixelhouse import Canvas, Animation, circle, motion


A = Canvas()
A = Animation(duration=2, fps=15)

A += circle(color="w")
A += circle(-1, 0, 0.25, color="purple")

theta = ph.motion.easeReturn("easeInOutQuad", 0, np.pi, len(A))
A += ph.transform.rotate(theta)

z = ph.motion.easeReturn("easeInOutQuad", 0, 10, len(A))
A += ph.transform.distort(seed=42, sigma=0.05, alpha=z)

A.show()
