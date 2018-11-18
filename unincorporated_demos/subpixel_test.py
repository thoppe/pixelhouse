import pixelhouse as ph
import numpy as np

C = ph.Canvas()
C = ph.Animation()

x = np.linspace(0.05, 0.1, 100)
C += ph.circle(x=x, r=1.5)

C += ph.transform.scale(4)
C.show()
