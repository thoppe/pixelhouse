# Experimenting with hstack, vstack, and dstack

import numpy as np
import pixelhouse as ph
import cv2

pal = ph.palette(2)

C = ph.Canvas(height=50, width=400, bg="w")
lg = ph.gradient.linear(pal, interpolation="discrete")
C += ph.rectangle(C.xmin, C.ymin, C.xmax, C.ymax, gradient=lg)

C2 = ph.Canvas(height=50, width=400, bg="w")
lg = ph.gradient.linear(pal[::-1], interpolation="discrete")
C2 += ph.rectangle(C.xmin, C.ymin, C.xmax, C.ymax, gradient=lg)

CX = ph.vstack([C,C2])
CX.show()



grid = []
for i in range(3):
    row = []
    for j in range(5):
        C = ph.Canvas(height=200, width=200)
        C += ph.circle(r=2, color=pal[(i + j) % 5])
        row.append(C)
    grid.append(row)


ph.canvas.gridstack(grid).show()
# C.show()

# lg = ph.gradient.linear(pal)
# C += ph.rectangle(C.xmin, 1, C.xmax, 0, gradient=lg)
