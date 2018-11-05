# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Canvas, circle
from pixelhouse.gradient import linear_gradient 

sx = 400


c = Canvas(width=sx, height=sx, bg='purple')

lg0 = linear_gradient(theta=0,color0='red', color1='green')
lg1 = linear_gradient(color0='white', color1=[255,255,155,20])

circle(gradient=lg1)(c)
circle(x=2.5,y=-2.5,r=0.5,gradient=lg0)(c)

c.show()
