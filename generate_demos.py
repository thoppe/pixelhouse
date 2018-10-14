from canvas import canvas
from animation import animation, circle
import src.easing as easing
import numpy as np
import os

save_dest = "examples"

animation_args = {
    "width" : 100,
    "height" : 100,
    "fps" : 6,
}

gif_args = {
    "palettesize" : 32,
    "gifsicle" : True,
}

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

rotating_circles().to_gif("examples/moving_circles.gif", **gif_args)

