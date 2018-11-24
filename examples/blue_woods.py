from pixelhouse import Canvas, ellipse
import pixelhouse as ph
import numpy as np


def draw_circles(C, dx=0.25, tc=0.1):
    pal = ph.palette(19)
    
    base_r = 0.80

    r = base_r + dx
    lg = ph.gradient.linear([pal[0], pal[1]], [1, 0], theta=-np.pi / 2)
    C += ellipse(0, 0, r, r, thickness=tc, gradient=lg)

    r = base_r - 2 * dx
    lg = ph.gradient.linear([pal[0], pal[1]], [1, 0], theta=np.pi / 2)
    C += ellipse(0, 0, r, r, thickness=tc / 2, gradient=lg)

    r = base_r - dx
    lg = ph.gradient.linear([pal[2], pal[1]], [1, 0], theta=-np.pi / 2)
    C += ellipse(0, 0, r, r, thickness=tc / 2, gradient=lg)

    r = base_r + 1.5 * dx
    lg = ph.gradient.linear([pal[2], pal[1]], [1, 0], theta=np.pi / 2)
    C += ellipse(0, 0, r, r, thickness=tc / 2, gradient=lg)


C = Canvas().load("asphalt-dark-dawn-531321.jpg")
C += ph.filters.instafilter("1977")

with C.layer() as C2:
    draw_circles(C2)
    C2 += ph.filters.gaussian_blur()
    draw_circles(C2)

C.save("figures/blue_woods.png")
C.show()
