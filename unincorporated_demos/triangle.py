# A working file to test various aspects of the module
import numpy as np
import pixelhouse as ph

pal = ph.palette(4)

C = ph.Canvas(width=400, height=400, bg=pal[0])
C = ph.Animation(width=400, height=400, bg=pal[0])

C += ph.circle(x=1, y=-0.5, r=2, color=pal[1])
theta = np.linspace(0, 2 * np.pi)

with C.layer() as CX:
    CX += ph.polyline(color="k")
    CX += ph.transform.rotate(theta)
    CX += ph.filters.gaussian_blur(0.25, theta / 6)

C += ph.circle(x=-1, r=1.0)

C.show()
