# Testing gradients of all kinds
import pixelhouse as ph
import numpy as np

C = ph.Canvas(height=200, width=800, bg="w")
# C = ph.Animation(height=200,width=800, bg='w')

pal = ph.palette(2)

lg = ph.gradient.linear(pal, interpolation="discrete")
C += ph.rectangle(C.xmin, -1, C.xmax, 0, gradient=lg)

lg = ph.gradient.linear(pal)
C += ph.rectangle(C.xmin, 1, C.xmax, 0, gradient=lg)

C.show()
