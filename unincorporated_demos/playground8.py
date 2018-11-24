# Testing gradients of all kinds
import pixelhouse as ph
import numpy as np

C = ph.Canvas(height=200,width=800, bg='w')
#C = ph.Animation(height=200,width=800, bg='w')

pal = ph.palette(1)
lg = ph.gradient.linear([pal[0], pal[3], pal[0]], [0,1,1])
lg = ph.gradient.linear([pal[0], pal[0],pal[3]], [0,1,1])
C += ph.rectangle(C.xmin, C.ymin, C.xmax,C.ymax, gradient=lg)

C.show()
