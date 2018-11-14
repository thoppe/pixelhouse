import numpy as np
import pixelhouse as ph
from pixelhouse.filter import gaussian_blur
import pixelhouse.transform.elastic as el

pal = ph.ColorLoversPalette()(6)
f_font = "../pixelhouse/fonts/Montserrat-Medium.otf"

C = ph.Canvas(500, 200, bg=pal[2])
C = ph.Animation(500, 200, bg=pal[2], fps=10)
lg = ph.linear_gradient(pal[0], pal[1])

C += ph.text("pixelhouse", font_size=0.75, font=f_font)

z = np.linspace(0, 0.5)
C += el.wave(amplitude=z, theta=np.pi/2)
#C += el.wave(theta=np.pi/2)

'''
# C += el.pull(alpha=0.05)
# C += el.distort(alpha=20)
z = np.logspace(-0.8, -1.5, 100)
print(z)
C += el.distort(sigma=z, seed=20)
'''

# C.save("logo_pixelhouse.png")
C.show()
