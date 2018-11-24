# Testing chained animation

import numpy as np
import random
import pixelhouse as ph
from pixelhouse.filters import gaussian_blur


pal = ph.palette(0)
random.seed(44)

x = np.linspace(0, 2, 100)

C = ph.Animation(400, 400, bg=pal[0])
C += ph.rectangle(x=x, x1=x + 1, color=pal[3])

C2 = C.blank(duration=1)
C2 += ph.circle(x=x, color=pal[2])
C2 += gaussian_blur()
C += C2


C.show()
