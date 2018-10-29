# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Canvas, Animation, circle
from pixelhouse.transform.simple import translate, rotate

c1 = Canvas(width=400, height=400)
circle(x=0, color='w')(c1)

translate()(c1)
circle(x=-1, r=0.25, color='purple')(c1)
rotate()(c1)

c1.show()
