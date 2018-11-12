import numpy as np
from pixelhouse import Canvas, Animation, motion
from pixelhouse import circle, text
from pixelhouse.transform.simple import translate, rotate
from pixelhouse.filter import gaussian_blur

import pixelhouse as ph

pal = ph.ColorLoversPalette()(6)

C = Canvas(400, 400, bg=pal[2])

lg = ph.linear_gradient(pal[0], pal[1])

C += circle(color=pal[3])
C += gaussian_blur()
C += circle(color=pal[3])
for i in np.arange(-6,6,1.0):
    C += text(y=i,gradient=lg)

C.save("../examples/logo.png")
C.show()
