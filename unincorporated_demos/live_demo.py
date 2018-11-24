import pixelhouse as ph
from pixelhouse import *
from pixelhouse.filters import *
from pixelhouse.motion import *
from pixelhouse.transform import *
import numpy as np

pal = palette(15)

C = Canvas(400, 400, bg=pal[0])
C = Animation(400, 400, bg=pal[0])

y = motion.easeReturn("easeInOutQuad", 2, -2, len(C))


def draw_circles(C):
    C += circle(-2, y, r=0.20, color=pal[1])
    C += circle(-1, -y, r=0.20, color=pal[2])
    C += circle(1, y, r=0.20, color=pal[1])
    C += circle(2, -y, r=0.20, color=pal[2])


draw_circles(C)
C += gaussian_blur(0.5, 0.5)
draw_circles(C)

with C.layer() as L:
    theta = easeInOutQuad(0, 2 * np.pi, len(C))()
    L += rectangle(-0.5, -0.5, 0.5, 0.5, color=pal[3])
    L += rotate(theta)

f_font = "../pixelhouse/fonts/Montserrat-Medium.otf"
g = ph.gradient.linear([pal[2], pal[3]])
C += text("H&&T presents", y=3, font_size=0.5, font=f_font, gradient=g)
C += text("pixelhouse", y=-3, font_size=0.5, font=f_font, gradient=g)

C.show()
