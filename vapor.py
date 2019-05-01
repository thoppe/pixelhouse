import pixelhouse as ph
import numpy as np
#from pixelhouse.filters.simple import glow


pal = ['#FF6AD5','#C774E8','#AD8CFF','#8795E8','#94D0FF',]

# Use the canvas for a static image
C = ph.Canvas(512, 512)
#C = ph.Animation(512, 512, duration=2, fps=20)


#lw = 0.75/3
#Y = np.linspace(-4.5, 4.5, len(pal))

lw = 1.0
Y = np.linspace(-3, 3, len(pal))
dk = 1.0/len(pal)
move = ph.motion.easeInOutQuad

    
for k, y in enumerate(Y):
    x = move(3, 0.25, flip=True, phase=k*dk)
    gx = move(1, 4, flip=True, phase=k*dk)
    line = ph.line(x=-x, x1=x, y=y, y1=y, thickness=lw, color=pal[k])
    C += ph.filters.glow(line, glow_x=gx, glow_y=1, n=10)
    print(k,y)

#ph.canvas2mp4(C, 'vwa.mp4')
C.show()
