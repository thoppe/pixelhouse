import numpy as np
import pixelhouse as ph
from pixelhouse.filter import gaussian_blur
import pixelhouse.transform.elastic as el

pal = ph.ColorLoversPalette()(6)
f_font = "../pixelhouse/fonts/Montserrat-Medium.otf"

C = ph.Canvas(500, 200, bg=pal[2])
C = ph.Animation(500, 200, bg=pal[2], fps=30)
lg = ph.linear_gradient(pal[0], pal[1])

# C += ph.circle(color=pal[3])
# C += gaussian_blur()
# C += ph.circle(color=pal[3])

# for i in np.arange(-6, 6, 1.0):
#    C += ph.text("pixelhouse", font=f_font, y=i, gradient=lg)
C += ph.text("pixelhouse", font=f_font,color='w')

# C += el.pull(alpha=0.05)
# C += el.distort(alpha=20)
#z = np.logspace(-0.8, -1.5, 100)
#print(z)
#C += el.distort(sigma=z, seed=20)
#z2 = 0.15 - z
# C += gaussian_blur(z2,z2)
# C.save("logo_pixelhouse.png")
C.show()
