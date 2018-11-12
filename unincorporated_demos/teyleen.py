# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Canvas, ellipse, linear_gradient
from pixelhouse.color import ColorLoversPalette
from pixelhouse.filter import gaussian_blur, instafilter
import numpy as np


def draw_circles(C, dx=0.25, tc=0.1):
    pal = ColorLoversPalette()(19)

    # Change the transparcy on one of the colors
    pal[1][3] = 0

    base_r = 0.80
    
    r = base_r+dx
    lg = linear_gradient(pal[0], pal[1], theta=np.pi/2)
    C += ellipse(0,0,r,r,thickness=tc,gradient=lg)
    
    r = base_r - 2*dx
    lg = linear_gradient(pal[0], pal[1], theta=-np.pi/2)
    C += ellipse(0,0,r,r,thickness=tc/2,gradient=lg)
    
    r = base_r-dx
    lg = linear_gradient(pal[2], pal[1], theta=np.pi/2)
    C += ellipse(0,0,r,r,thickness=tc/2,gradient=lg)
    
    r = base_r+1.5*dx
    lg = linear_gradient(pal[2], pal[1], theta=-np.pi/2)
    C += ellipse(0,0,r,r,thickness=tc/2,gradient=lg)
   

C = Canvas().load("asphalt-dark-dawn-531321.jpg")
C += instafilter('1977')
    
C2 = C.copy()
    
draw_circles(C2)
C2 += gaussian_blur()
draw_circles(C2)

C += C2
C.save("../examples/teyleen_unknown.jpg")
C.show()


