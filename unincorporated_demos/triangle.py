# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Canvas, polyline, circle

c1 = Canvas(width=400, height=400, bg="white")
c1(polyline(color="k"))

c2 = Canvas(width=400, height=400, bg="white")
c2(circle(color="teal"))

C = c1.blank()
C += c2
C += c1
C.show()
