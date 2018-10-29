# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Canvas, Animation, circle
from pixelhouse.transform.affine import translate

c1 = Canvas(width=400, height=400)#, bg='purple')
circle(x=0, color='w')(c1)


translate()(c1)
circle(x=-1, r=0.25, color='purple')(c1)
translate(dy=-.7)(c1)

c1.show()
