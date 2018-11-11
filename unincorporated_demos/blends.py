# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Canvas, Animation, circle, motion
from pixelhouse.gradient import linear_gradient 

sx = 400

C = Animation(width=400, height=400, bg='purple')
C = Canvas(width=sx, height=sx, bg='purple')

z = motion.easeInOutQuad(0, 2*np.pi, len(C))()
lg0 = linear_gradient(color0='red', color1='green')
lg1 = linear_gradient(theta=z,color0='w', color1=[255,255,155,0])
C(circle(r=z/4,gradient=lg1))
C(circle(x=2.5,y=-2.5,r=0.5,gradient=lg0))
C.show()



