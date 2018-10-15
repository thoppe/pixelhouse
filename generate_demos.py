from canvas import canvas
from animation import animation, circle, line
import src.easing as easing
import numpy as np
import os
import itertools
from src.nice_colors import get_palette

save_dest = "examples"

canvas_args = {
    "width" : 100,
    "height" : 100,
    "extent": 4,
}

animation_args = {
    "fps" : 6,
}
animation_args.update(canvas_args)

gif_args = {
    "palettesize" : 32,
    "gifsicle" : True,
}

#########################################################################


def simple_circles():
    c = canvas(**canvas_args)
    q = 155
    
    n = 3
    t = np.arange(0, 2*np.pi, 2*np.pi/n) + np.pi/6
    x,y = np.cos(t), np.sin(t)

    c.circle(x[0], y[0], r=1, color=[0,255,0])
    c.circle(x[1], y[1], r=1, color=[255,0,0])
    c.circle(x[2], y[2], r=1, color=[0,0,255])

    # An example of not saturating the images together
    c.circle(0, 0, r=0.25, color=[q,q,q], blend=False)
    
    return c

def simple_rectangles():
    c = canvas(**canvas_args)

    c.rectangle(-1,-1,1,1,[255,0,0])
    c.rectangle(0,0,2,-2,[0,0,255])
    c.rectangle(-3,-3,0.5,0.5,[0,255,0])

    return c


def simple_ellipses():
    c = canvas(**canvas_args)

    a0 = np.pi/8
    a1 = 2*np.pi - np.pi/8

    c.ellipse(0,0, 1, 0.75, 0, a0, a1,
              color=[155,230,235])

    c.ellipse(-4,0, 1, 0.75, 0, a0, a1,
              color=[155,230,235])

    c.ellipse(4,0, 1, 0.75, 0, a0, a1,
              color=[155,230,235])
    
    return c

def simple_lines():
    c = canvas(**canvas_args)
    
    c.line(-4, 0, 4, 0, thickness=0.05)
    c.line(0, 4, 0, -4, thickness=0.05)

    tc = 0.04

    for i in np.arange(-4,5,1):
        c.line(-4, i, 4, i, thickness=tc, color=[100,int(100+i*10),100])
        c.line(i, 4, i, -4, thickness=tc, color=[100,100,int(100+i*10)])

    for i in np.arange(-4,5,.5):
        c.line(-4, i, 4, i, thickness=tc, color=[20,]*3)
        c.line(i, 4, i, -4, thickness=tc, color=[20,]*3)

    return c

def teyleen_982():
    c = canvas(**canvas_args)
    pi = np.pi
    
    pal = [[230]*3,] + get_palette(96) + [[230]*3,]
    
    c = canvas(**canvas_args)
    tc = 0.025

    dx = pi/8
    t0 = dx
    t1 = 2*pi-dx
    r = 1.8

    for n in range(6):
        c.ellipse(0,0,r,r,pi/2,t0,t1,
                  color=pal[n],
                  thickness=tc)

        dx *= 1.4
        t0 = dx
        t1 = 2*pi-dx
        r -= 0.2

    return c

#########################################################################


def rotating_circles():
    A = animation(**animation_args)

    # Use an ease function to go in an out
    E1 = easing.QuadEaseInOut(-1, 1, len(A)//2)
    E2 = easing.QuadEaseInOut(1, -1, len(A)//2)
    x = np.hstack([E1(),E2()])

    A.add(circle(x=x, y=1, r=1.25,color=[150,250,0]))
    A.add(circle(x=-x, y=-1, r=1.25,color=[100,5,255]))
        
    return A


def checkerboard():
    A = animation(**animation_args)

    # Use an ease function to go in an out
    E1 = easing.QuadEaseInOut(0, 1, len(A)//2)
    E2 = easing.QuadEaseInOut(1, 0, len(A)//2)
    z = np.hstack([E1(),E2()])
    
    r = 0.20
    c = [150, 250, 0]
    coord = [-2, 0, 2]

    for dx, dy in itertools.product(coord, repeat=2):
        A.add(circle(x=z+dx, y=z+dy, r=r,color=c))
        A.add(circle(x=z+dx, y=-z+dy, r=r,color=c))
        A.add(circle(x=-z+dx, y=-z+dy, r=r,color=c))
        A.add(circle(x=-z+dx, y=z+dy, r=r,color=c))

        A.add(circle(x=dx, y=z+dy, r=r,color=c))
        A.add(circle(x=z+dx, y=dy, r=r,color=c))

        A.add(circle(x=dx, y=-z+dy, r=r,color=c))
        A.add(circle(x=-z+dx, y=dy, r=r,color=c))
    
    return A


def timer():
    A = animation(**animation_args)

    r, polyn, tc = 3, 0.1, 0.315
    c = [65, 0, 20]

    for k in range(20):

        theta = easing.SmoothEaseIn(polyn, 0, 2*np.pi, len(A))()
        L = line(
            x0=0,y0=0,x1=r*np.cos(theta),
            y1=r*np.sin(theta),
            thickness=tc, color=c
        )
        A.add(L)
        
        r *= 0.98
        polyn *= 1.2

    return A

#########################################################################

if __name__ == "__main__":

    '''
    simple_lines().save("examples/simple_lines.png")
    simple_circles().save("examples/simple_circles.png")
    simple_rectangles().save("examples/simple_rectangle.png")
    simple_ellipses().save("examples/simple_ellipses.png")
    
    rotating_circles().to_gif("examples/moving_circles.gif", **gif_args)
    checkerboard().to_gif("examples/checkerboard.gif", **gif_args)
    timer().to_gif("examples/timer.gif", **gif_args)
    '''

    teyleen_982().save("examples/teyleen_982.png")
    
