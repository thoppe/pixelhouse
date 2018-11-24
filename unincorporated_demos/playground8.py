# Testing gradients of all kinds

import pixelhouse as ph

C = ph.Canvas(height=200,width=800, bg='k')

pal = ph.palette(1)
lg = ph.gradient.linear([pal[0], pal[3], pal[0]])
C += ph.rectangle(C.xmin, C.ymin, C.xmax,C.ymax, gradient=lg)
C.show()
