import pixelhouse as ph
import numpy as np

pal = ["#FF6AD5", "#C774E8", "#AD8CFF", "#8795E8", "#94D0FF"] * 3
C = ph.Canvas(400, 400)
#C = ph.Animation(512, 512, fps=30, duration=4)

lw = 0.25
Y = np.linspace(-4.0, 4.0, len(pal))
dk = 1.0 / len(pal)
move = ph.motion.easeInOutQuad

for k, y in enumerate(Y):
    x = move(3, 0.25, flip=True, phase=k * dk)
    gx = move(1, 4, flip=True, phase=k * dk)
    line = ph.line(x=-x, x1=x, y=y, y1=y, thickness=lw, color=pal[k])
    C += ph.filters.glow(line, glow_x=gx, glow_y=gx, n=5)


#ph.canvas2mp4(C, "vwa.mp4")
C.save("../examples/figures/vapor.png")
C.show()
