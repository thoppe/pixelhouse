import pixelhouse as ph
import numpy as np

C = ph.Animation()

x = np.linspace(0.05, 0.1, 100)
C += ph.circle(x=x, r=3.0)

C.resize(4)
C.show()
