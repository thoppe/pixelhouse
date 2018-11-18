import numpy as np
import pixelhouse as ph
from pixelhouse.filters import gaussian_blur
import pixelhouse.transform.elastic as el

pal = ph.palette(8)
f_font = "../pixelhouse/fonts/Montserrat-Medium.otf"

C = ph.Canvas(500, 200, bg=pal[2])
C = ph.Animation(500, 200, bg=pal[2])#, fps=10)
lg = ph.linear_gradient(pal[0], pal[1])

C += ph.text("pixelhouse", font_size=0.78, font=f_font, color='w')
C += ph.text("pixelhouse", font_size=0.75, font=f_font, gradient=lg)


#a = 0.01
#a = ph.motion.easeReturn("easeInOutQuad", 0, 0.06, len(C))
a = ph.motion.easeReturn("easeInOutQuad", 0.06, 0.0, len(C))

z = np.linspace(2*np.pi, 0)
C += el.wave(amplitude=3*a, wavelength=1.5, offset=z)

z = np.linspace(0, 2*np.pi)
C += el.wave(amplitude=a, wavelength=0.3, offset=z)

z = np.linspace(0, 2*np.pi)
C += el.wave(amplitude=a/2, wavelength=0.3/7, offset=z+.2)

C.show()
