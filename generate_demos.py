from pixelhouse.canvas import Canvas, matplotlib_colors
from pixelhouse.animation import Animation
from pixelhouse.artists import circle, line, ellipse, rectangle
import numpy as np
import os
import itertools

import pixelhouse.motion.easing as easing
from pixelhouse.color.palettes import ColorLoversPalette

save_dest = "examples"

canvas_args = {
    "width" : 100,
    "height" : 100,
    "extent": 4,
}

animation_args = {
    "fps" : 20,
    "duration" : 1.5,
}
animation_args.update(canvas_args)

gif_args = {
    "palettesize" : 32,
    "gifsicle" : True,
}

palettes = ColorLoversPalette()

#########################################################################


def simple_circles():
    c = Canvas(**canvas_args)

    n = 3
    t = np.arange(0, 2*np.pi, 2*np.pi/n) + np.pi/6
    x,y = np.cos(t), np.sin(t)

    circle(x=x[0], y=y[0], r=1, color=[0,255,0])(c)
    circle(x=x[1], y=y[1], r=1, color=[255,0,0])(c)
    circle(x=x[2], y=y[2], r=1, color=[0,0,255])(c)

    # An example of not saturating the images together
    circle(x=0, y=0, r=0.25, color=[155,155,155], blend=False)(c)
    
    return c

def simple_rectangles():
    c = Canvas(**canvas_args)

    rectangle(x=-1,y=-1,x1=1,y1=1,color='lightcoral')(c)
    rectangle(x=0,y=0,x1=2,y1=-2,color='lime')(c)
    rectangle(x=-3,y=-3,x1=0.5,y1=0.5,color='royalblue')(c)

    return c


def simple_lines():
    c = Canvas(**canvas_args)
    
    line(x=-4, y=0, x1=4, y1=0, thickness=0.05)(c)
    line(x=0, y=4, x1=0, y1=-4, thickness=0.05)(c)

    tc = 0.04

    for i in np.arange(-4,5,1):
        line(x=-4, y=i, x1=4, y1=i, thickness=tc,
             color=[100,int(100+i*10),100])(c)
        line(x=i, y=4, x1=i, y1=-4, thickness=tc,
             color=[100,100,int(100+i*10)])(c)

    for i in np.arange(-4,5,.5):
        line(x=-4, y=i, x1=4, y1=i,
             thickness=tc, color=[20,]*3)(c)
        line(x=i, y=4, x1=i, y1=-4,
             thickness=tc, color=[20,]*3)(c)

    return c


def teyleen_982():
    c = Canvas(**canvas_args)
    pi = np.pi
    
    pal = [matplotlib_colors("lavender"),] + palettes(96)
    tc = 0.025

    dx = pi/8
    t0 = dx
    t1 = 2*pi-dx
    r = 1.8

    for n in range(6):
        ellipse(a=r,b=r,rotation=pi/2,
                angle_start=t0,angle_end=t1,
                color=pal[n],
                thickness=tc)(c)

        dx *= 1.4
        t0 = dx
        t1 = 2*pi-dx
        r -= 0.2

    return c

def teyleen_116():
    c = Canvas(**canvas_args)
    pal = palettes(152)

    x = 0.25
    circle(x=x,y=x, r=x/2, color=pal[0])
    circle(x=-x,y=x, r=x/2, color=pal[1])
    circle(x=x,y=-x, r=x/2, color=pal[2])
    circle(x=-x,y=-x, r=x/2, color=pal[3])

    circle(y=x/2, r=2-x, color=pal[4],thickness=x/20)(c)
    circle(y=-x/2, r=2-x, color=pal[4],thickness=x/20)(c)

    return c


#########################################################################


def rotating_circles():
    A = Animation(**animation_args)
    x = easing.easeReturn('easeInOutQuad', -1, 1, len(A))

    A.add(circle(x=x, y=1, r=1.25,color=[0,250,150]))
    A.add(circle(x=-x, y=-1, r=1.25,color=[255,5,100]))
        
    return A


def checkerboard():
    A = Animation(**animation_args)
    z = easing.easeReturn('easeInOutQuad', 0, 1, len(A))
        
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
    A = Animation(**animation_args)
    
    tc = 0.315
    r = 3.0
    lag = 0.1

    for k in range(20):

        theta = easing.OffsetEase(lag, stop=2*np.pi, duration=len(A))()

        L = line(
            x1=r*np.cos(theta),
            y1=r*np.sin(theta),
            thickness=tc, color='indigo',
        )
        A.add(L)
        
        r *= 0.98
        lag *= 1.17

    return A


def pacman():
    args = animation_args.copy()
    args["duration"] = 0.5
    A = Animation(**args)

    pac_color = (253,255,0)

    # Chomping easing function
    dp = np.pi/4
    x0 = easing.easeOutQuad(0, dp, len(A)//2)()
    x1 = easing.easeInQuad(dp, 0, len(A)//2)()
    z = np.hstack([x0,x1])

    pacman = ellipse(
        a=1, b=1,
        angle_start=z, angle_end=2*np.pi-z, color=pac_color)

    A.add(pacman)
    return A

#########################################################################

if __name__ == "__main__":

    simple_lines().save("examples/simple_lines.png")
    simple_circles().save("examples/simple_circles.png")
    simple_rectangles().save("examples/simple_rectangle.png")

    rotating_circles().to_gif("examples/moving_circles.gif", **gif_args)
    pacman().to_gif("examples/pacman.gif", **gif_args)
    checkerboard().to_gif("examples/checkerboard.gif", **gif_args)
    timer().to_gif("examples/timer.gif", **gif_args)

    teyleen_982().save("examples/teyleen_982.png")
    teyleen_116().save("examples/teyleen_116.png")
    
    
