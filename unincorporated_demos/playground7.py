# Testing chained animation

import numpy as np
import random
from pixelhouse import Canvas, Animation, motion
from pixelhouse import circle, text, rectangle
from pixelhouse.transform.simple import translate, rotate
from pixelhouse.filter import gaussian_blur
import pixelhouse as ph

pal = ph.ColorLoversPalette()(0)
random.seed(44)

x = np.linspace(0, 2, 100)

C = Animation(400, 400, bg=pal[0])
C += rectangle(x=x, x1=x + 1, color=pal[3])

C2 = C.blank(duration=1)
C2 += circle(x=x, color=pal[2])
C2 += gaussian_blur()
C += C2


C.show()
