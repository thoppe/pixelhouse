# A working file to test various aspects of the module
import numpy as np
import pixelhouse as ph
from pixelhouse import Canvas, Animation
from pixelhouse import circle, motion, rectangle, line, ellipse

# A = Canvas(width=300, height=300)
A = Animation(width=400, height=400, fps=2)

A += circle(r=0.5, color="darkorange")
A += circle(r=0.4, color="w", mode="direct")

z = ph.motion.easeInOutQuad(0, 2 * np.pi, len(A))()
A += ph.transform.motion_lines(0.2, theta=z)
A += ph.transform.motion_lines(0.2)
A += ph.transform.rotate(z)

A.show()
