from canvas import canvas
from animation import animation, circle
import src.easing as easing
import numpy as np
import os
import itertools

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

    n = 3
    t = np.arange(0, 2*np.pi, 2*np.pi/n) + np.pi/6
    x,y = np.cos(t), np.sin(t)

    c.circle(x[0], y[0], r=1, color=[0,255,0])
    c.circle(x[1], y[1], r=1, color=[255,0,0])
    c.circle(x[2], y[2], r=1, color=[0,0,255])

    # An example of not saturating the images together
    c.circle(0, 0, r=0.25, color=[55,]*3, blend=False)

    return c

def simple_rectangles():
    c = canvas(**canvas_args)

    c.rectangle(-1,-1,1,1,[255,0,0])
    c.rectangle(0,0,2,-2,[0,0,255])
    c.rectangle(-3,-3,0.5,0.5,[0,255,0])

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

#########################################################################

if __name__ == "__main__":
    
    simple_circles().save("examples/simple_circles.png")
    simple_rectangles().save("examples/simple_rectangle.png")
    rotating_circles().to_gif("examples/moving_circles.gif", **gif_args)
    checkerboard().to_gif("examples/checkerboard.gif", **gif_args)
