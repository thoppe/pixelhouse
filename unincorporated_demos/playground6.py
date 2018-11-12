import numpy as np
import random
from pixelhouse import Canvas, Animation, motion
from pixelhouse import circle, text
from pixelhouse.transform.simple import translate, rotate
from pixelhouse.filter import gaussian_blur

import pixelhouse as ph

pal = ph.ColorLoversPalette()(15)
q = lambda x: np.random.uniform(-4,4)
#q = lambda x: np.random.normal(0,x)

C = Canvas(400, 400, bg=pal[0])
#C = Animation(400, 400, fps=30, bg=pal[0], duration=7)
r = 0.20

for k,y in enumerate(np.arange(-6,6,r*2)):
    
    x0 = np.arange(-6,6,r*5)
    if k%2: x0+= r

    p = np.random.permutation(range(len(x0)))
    colors = [random.choice(pal[1:]) for k in range(len(x0))]

    for k in range(len(x0)):
        x = motion.easeReturn('easeInOutQuad', x0[k], x0[p[k]], len(C))
        c = colors[k]
        
        C += circle(x=x,y=y,r=r,color=c)
C.save("../examples/circle_lines.png")

        
#C += translate(0, 1.0)

'''
for i in np.arange(-5,5,r*5):
    for j in np.arange(-5,5,r*5):
        x0.append(i)
        y0.append(j)

p = np.random.permutation(range(len(x0)))
colors = [random.choice(pal[1:]) for k in range(len(x0))]

for k in range(len(x0)):
    
    c = colors[k]

    x = motion.easeReturn('easeInOutQuad', x0[k], x0[p[k]], len(C))
    y = motion.easeReturn('easeInOutQuad', y0[k], y0[p[k]], len(C))
    y = y0[k]
    
    C += circle(x=x,y=y,r=r,color=c)
'''

'''
for k,y in enumerate(np.arange(-6,6,r*2)):
    
    x0 = np.arange(-6,6,r*5)
    if k%2: x0+= r

    p = np.random.permutation(range(len(x0)))
    colors = [random.choice(pal[1:]) for k in range(len(x0))]

    for k in range(len(x0)):
        x = motion.easeReturn('easeInOutQuad', x0[k], x0[p[k]], len(C))
        c = colors[k]
        
        C += circle(x=x,y=y,r=r,color=c)
'''    

'''
for i in range(100):
    for c in pal[1:]:
        x = motion.easeReturn('easeInOutQuad', q(1), q(1.5), len(C))
        y = motion.easeReturn('easeInOutQuad', q(1), q(1.5), len(C))
        C += circle(x=x,y=y,r=r,color=c)
    
    C += gaussian_blur(.05,0.05)
'''

    
#C += gaussian_blur()
#C += circle(color=pal[3])
#for i in np.arange(-6,6,1.0):
#    C += text(y=i,gradient=lg)
from pixelhouse import canvas2mp4, canvas2gif

#canvas2mp4(C, "dots.mp4")
#canvas2gif(C, "dots.gif", gifsicle=True, palettesize=32)
C.show()
