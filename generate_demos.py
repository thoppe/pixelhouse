from canvas import canvas
from animation import animation, circle
import src.easing as easing
import numpy as np
import os

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

def rotating_circles(show=False):
    # Rotating circles
    A = animation(**animation_args)

    # Use an ease function to go in an out
    E1 = easing.QuadEaseInOut(-1, 1, len(A)//2)
    E2 = easing.QuadEaseInOut(1, -1, len(A)//2)
    
    x = np.hstack([E1(),E2()])

    A.add(circle(x=x, y=1, r=1.25,color=[150,250,0]))
    A.add(circle(x=-x, y=-1, r=1.25,color=[100,5,255]))

    if show:
        A.show(repeat=True)
        
    return A

simple_circles().save("examples/simple_circles.png")
rotating_circles().to_gif("examples/moving_circles.gif", **gif_args)

