# A working file to test various aspects of the module
import numpy as np
import pixelhouse as ph
from pixelhouse import Canvas, Animation, polyline, circle, Artist
from pixelhouse.transform import rotate, translate
from pixelhouse.filter import gaussian_blur

pal = ph.ColorLoversPalette()(4)

C = Canvas(width=400, height=400, bg=pal[0])

C += circle(x=1, y=-.5, color=pal[1])

with C.layer() as CX:
    CX += polyline(color='k')
    CX += gaussian_blur(.5,.5)
C += circle(r=0.5)
C.show()
