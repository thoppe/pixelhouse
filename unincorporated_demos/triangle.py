# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Canvas, polyline

c1 = Canvas(width=400, height=400, bg='white')
polyline(color='k')(c1)

c1.show()
