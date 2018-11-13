import numpy as np
import random
from pixelhouse import Canvas, Animation, motion
from pixelhouse import circle, text
from pixelhouse.transform.simple import translate, rotate
from pixelhouse.filter import gaussian_blur

import pixelhouse as ph

pal = ph.ColorLoversPalette()(20)
random.seed(44)

C = Canvas(400, 400, bg=pal[0])
r = 0.20

for k, y in enumerate(np.arange(-6, 6, r * 2)):

    x0 = np.arange(-6, 6, r * 5)
    if k % 2:
        x0 += r

    colors = [random.choice(pal[1:]) for k in range(len(x0))]

    for k in range(len(x0)):
        c = colors[k]
        C += circle(x=x0[k], y=y, r=r, color=c)

C.save("circle_lines.png")
C.show()
