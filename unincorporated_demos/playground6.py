# Example of rotating off axis
import numpy as np
import pixelhouse as ph
from pixelhouse.filter import gaussian_blur
from pixelhouse.transform import rotate

pal = ph.ColorLoversPalette()(6)

# C = ph.Canvas(400, 400, bg=pal[2])
C = ph.Animation(400, 400, bg=pal[2])

lg = ph.linear_gradient(pal[0], pal[1])

theta = np.linspace(0, 2 * np.pi)
C += ph.text("pixelhouse", gradient=lg)
C += rotate(theta, x=-3)


C.show()
