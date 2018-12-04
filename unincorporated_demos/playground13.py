# Testing the new easing

import pixelhouse as ph
from pixelhouse import *
from pixelhouse.motion import *
import numpy as np

pal = palette(15)
g = ph.gradient.linear([pal[2], pal[3]])

C = Animation(400, 200, bg=pal[0])

b = motion.easeInOutQuad(-3, 3, flip=True)
C += circle(x=b, y=-1, r=0.2, gradient=g)

b = motion.easeInOutQuad(-2, 2, flip=True, phase=0.1)
C += circle(x=b, y=0, r=0.2, gradient=g)

C += circle(x=b + 1, y=1, r=0.2, gradient=g)
C += circle(x=b - 1, y=1.2, r=0.2, gradient=g)
C += circle(x=b * 2, y=1.2, r=0.2, gradient=g)
C += circle(x=b / 2, y=1.2, r=0.2, gradient=g)

C.show()
