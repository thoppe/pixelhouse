import pixelhouse as ph
from tqdm import tqdm 
from pixelhouse import circle
import os
import numpy as np
from playground9 import splatter
import random

random.seed(42)
np.random.seed(42)


f_pts = "hs_pts.npy"

if not os.path.exists(f_pts):
    pts = []
    buffer_radius = 0.10

    def is_overlap(x,y,r):
        for x2, y2, r2, _ in pts:
            dist = np.sqrt((x-x2)**2+(y-y2)**2)

            if dist <= r+r2+buffer_radius:
                return True
        return False

    for n in tqdm(range(8000)):
        p = np.random.uniform(0, 5)
        r = np.random.uniform(0.03, 0.40)

        p += 12*r

        theta = np.random.uniform(0, 2*np.pi)

        x = p*np.cos(theta)
        y = p*np.sin(theta)

        if is_overlap(x,y,r):
            continue

        color = np.random.randint(1,5)
        pts.append((x,y,r, color))

    print(np.array(pts))
    np.save(f_pts, np.array(pts),)


pts = np.load(f_pts)


pal = ph.palette(114)
#C = ph.Canvas(600, 600, bg=pal[0])
C = ph.Animation(600, 600, bg=pal[0], fps=30)

idx = np.argsort(pts[:, -2])
pts = pts[idx]

for x,y,r,color in tqdm(pts):
    u = int(color)

    if u == 1:
        t = np.linspace(0, 100)
        theta = ph.motion.easeInSine(0, 2*np.pi,flip=True)(t)
        tx = np.arctan2(y, x)
        rx = np.sqrt(x**2+y**2)

        x = rx*np.cos(theta+tx)
        y = rx*np.sin(theta+tx)

    elif u == 2:
        t = np.linspace(0, 100)
        theta = ph.motion.easeInBack(0, 2*np.pi,flip=True)(t)
        tx = np.arctan2(y, x)
        rx = np.sqrt(x**2+y**2)

        x = rx*np.cos(theta+tx)
        y = rx*np.sin(theta+tx)

    elif u == 3:
        t = np.linspace(0, 100)
        theta = ph.motion.easeInBack(0, 2*np.pi)(t)
        tx = np.arctan2(y, x)
        rx = np.sqrt(x**2+y**2)

        x = rx*np.cos(theta+tx)
        y = rx*np.sin(theta+tx)

    elif u == 4:
        t = np.linspace(0, 100)
        theta = ph.motion.easeInOutBack(0, 2*np.pi)(t)
        tx = np.arctan2(y, x)
        rx = np.sqrt(x**2+y**2)

        x = rx*np.cos(theta+tx)
        y = rx*np.sin(theta+tx)
    
    C += circle(x=x, y=y, r=r, color=pal[u])
    C += circle(x=x, y=y, r=r, color='k',thickness=.0001)  

    
C.show()
