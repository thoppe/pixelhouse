import numpy as np
import pixelhouse as ph

# A = ph.Canvas(width=300, height=300)
# A = ph.Animation(width=300, height=300, fps=25)
A = ph.Animation(width=300, height=300)

# Draw grid lines
dx = 4
for i in np.arange(-dx, dx, 0.5):
    A += ph.line(i, -dx, i, dx, thickness=0)
    A += ph.line(-dx, i, dx, i, thickness=0)

z = ph.motion.easeInOutQuad(2, -2)
x = ph.motion.easeInOutQuad(2, -2)
A += ph.transform.pull(x, 0.25, alpha=z, mode="constant")

A.show()
