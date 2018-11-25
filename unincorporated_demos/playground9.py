# Experimenting with new filter, splatter!

import numpy as np
import pixelhouse as ph
import cv2

class splatter(ph.Artist):
    
    color = ph.artist.constant('w')
    gamma = ph.artist.constant(0.10)
    iterations = ph.artist.constant(20)
    kernel_size = ph.artist.constant(5)
    seed = ph.artist.constant(None)
    
    args = ("color", "gamma", "iterations", "kernel_size", "seed")
    
    def draw(self, cvs, t=0):
        random_state = np.random.RandomState(self.seed(t))

        color = cvs.transform_color(self.color(t))
        n = self.kernel_size(t)
        gamma = self.gamma(t)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(n,n))
        org = cvs._img.copy()

        for i in range(self.iterations(t)):
            
            mask = cvs.alpha
            idx = (cv2.dilate(mask, kernel) & (~mask)).astype(bool)
            xi, xj = np.where(idx)
            p = np.random.uniform(size=len(xi))
    
            idx[xi[p>gamma], xj[p>gamma]] = False
            cvs._img[idx] = color

        mask = cvs.alpha
        idx = ~cv2.erode(mask, kernel).astype(bool)
        cvs._img[idx] = org[idx]


pal = ph.palette(32)
np.random.shuffle(pal)

C = ph.Canvas(400,400,bg=pal[0])
#C = ph.Animation(400,400,bg=pal[0])

for i in range(30):
    with C.layer() as CX:
        x = np.random.uniform(-4, 4)
        y = np.random.uniform(-4, 4)
        c = pal[np.random.randint(1,5)]
        r = np.random.uniform(0.2, 0.5)
        gamma = np.random.uniform(0.05, 0.10)
        
        CX += ph.circle(x=x,y=y,r=r,color=c)
        CX += splatter(gamma=gamma,color=c,seed=20)

C.show()
