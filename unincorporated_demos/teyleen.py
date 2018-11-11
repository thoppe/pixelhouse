# A working file to test various aspects of the module
import numpy as np
import pixelhouse as ph
from pixelhouse import Canvas, ellipse
from pixelhouse.color import ColorLoversPalette
from pixelhouse.filter import gaussian_blur, instafilter
import numpy as np


def draw_circles(C, dx=0.25, tc=0.1):

    c0 = pal[0]
    c1 = pal[1]
    c1[3] = 0
    c2 = pal[2]

    base_r = 0.80
    
    r = base_r+dx
    lg = ph.linear_gradient(theta=np.pi/2, color0=c0, color1=c1)
    C(ellipse(0,0,r,r,thickness=tc,gradient=lg))

    
    r = base_r - 2*dx
    lg = ph.linear_gradient(theta=-np.pi/2, color0=c0, color1=c1)
    C(ellipse(0,0,r,r,thickness=tc/2,gradient=lg))
    
    r = base_r-dx
    lg = ph.linear_gradient(theta=np.pi/2, color0=c2, color1=c1)
    C(ellipse(0,0,r,r,thickness=tc/2,gradient=lg))
    
    r = base_r+1.5*dx
    lg = ph.linear_gradient(theta=-np.pi/2, color0=c2, color1=c1)
    C(ellipse(0,0,r,r,thickness=tc/2,gradient=lg))
   

pal = ColorLoversPalette()(19)
    
C = Canvas().load("asphalt-dark-dawn-531321.jpg")
C(instafilter('1977'))
    
C2 = C.copy()
    
draw_circles(C2)
gaussian_blur()(C2)
draw_circles(C2)

C += C2
C.save("../examples/teyleen_unknown.jpg")
C.show()


