import random
import numpy as np
import pixelhouse as ph

pal = ph.palette(20)
random.seed(44)

C = ph.Canvas(400, 400, bg=pal[0])
r = 0.20

for k, y in enumerate(np.arange(-6, 6, r * 2)):

    x0 = np.arange(-6, 6, r * 5)
    if k % 2:
        x0 += r

    colors = [random.choice(pal[1:]) for k in range(len(x0))]

    for k in range(len(x0)):
        c = colors[k]
        C += ph.circle(x=x0[k], y=y, r=r, color=c)

C.save("figures/circle_lines.png")
C.show()
