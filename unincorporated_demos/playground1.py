# Testing layers
import numpy as np
import pixelhouse as ph

C = ph.Canvas(width=400, height=400, bg="purple")

with C.layer() as CX:
    CX += ph.circle(r=2, x=0, color="w")
    for i in range(10):
        CX += ph.filters.gaussian_blur(blur_x=0.50)

    CX += ph.circle(x=0, color="w")

C += ph.circle(x=0, y=2, r=1.4, color="r")
C += ph.circle(x=0, y=-2, r=1.4, color="k")
C += ph.circle(x=0, y=2, r=1.4, color="r")

C.show()
