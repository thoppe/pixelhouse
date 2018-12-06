# A working file to test various aspects of the module
import numpy as np
import pixelhouse as ph

# A = ph.Canvas(width=300, height=300)
A = ph.Animation(width=400, height=400, fps=2)

A += ph.circle(r=1.0, color="darkorange")
A += ph.circle(r=0.8, color="w", mode="direct")

z = ph.motion.easeInOutQuad(0, 2 * np.pi)
A += ph.transform.motion_lines(0.4, theta=z)
A += ph.transform.motion_lines(0.4)
A += ph.transform.rotate(z)

A.show()
