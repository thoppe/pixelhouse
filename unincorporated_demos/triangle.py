# A working file to test various aspects of the module
import numpy as np
import pixelhouse as ph
from pixelhouse import Canvas, polyline, circle
from pixelhouse.transform import rotate, translate

pal = ph.ColorLoversPalette()(2)


c1 = Canvas(width=400, height=400, bg=pal[0])
c1(polyline(color='k'))

c2 = Canvas(width=400, height=400, bg=pal[0])
c2(circle(color=pal[2]))

C = c1.blank()
C += c2
C += c1

C += rotate(np.pi/4)
C += translate(1.0)
C.show()
