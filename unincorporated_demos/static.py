# An example of a live animation
import numpy as np
import pixelhouse as ph
import time

class random_static(ph.Artist):

    def __init__(self):
        self.k = 0
        self.t0 = time.time()
        
    def draw(self, cvs, t=0):
        p = np.random.uniform(size=(cvs.height, cvs.width))
        cvs._img[p >= 0.5] = [125,]*4
        cvs._img[p <  0.5] = [0,]*4

        self.k += 1
        total_time = time.time() - self.t0
        fps = self.k / total_time

        cvs += ph.text(f"{fps:0.2f}")

#A = ph.LiveAnimation(1600, 800)
A = ph.LiveAnimation(800, 400)

A += random_static()
A.show()

