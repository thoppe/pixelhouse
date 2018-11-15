from pixelhouse import Canvas, Animation
from pixelhouse import circle, line, ellipse, rectangle
from pixelhouse.color import matplotlib_colors, ColorLoversPalette
from pixelhouse.filters import instafilter
from pixelhouse.transform import scale
import pixelhouse.motion as motion

from pixelhouse import canvas2mp4, canvas2gif

import numpy as np
import itertools

save_dest = "examples"

canvas_args = {"width": 100, "height": 100, "extent": 4}

animation_args = {"fps": 20, "duration": 1.5}
animation_args.update(canvas_args)

gif_args = {"palettesize": 32, "gifsicle": True}

palettes = ColorLoversPalette()

#########################################################################


def simple_circles():
    C = Canvas(**canvas_args)

    n = 3
    t = np.arange(0, 2 * np.pi, 2 * np.pi / n) + np.pi / 6
    x, y = np.cos(t), np.sin(t)

    C += circle(x[0], y[0], 1, color=[0, 255, 0], mode="add")
    C += circle(x[1], y[1], 1, color=[255, 0, 0], mode="add")
    C += circle(x[2], y[2], 1, color=[0, 0, 255], mode="add")

    # An example of not saturating the images together
    C += circle(0, 0, 0.25, color=[155, 155, 155])

    return C


def simple_rectangles():
    C = Canvas(**canvas_args)

    C += rectangle(-1, -1, 1, 1, color="lightcoral")
    C += rectangle(0, 0, 2, -2, color="lime")
    C += rectangle(-3, -3, 0.5, 0.5, color="royalblue")

    return C


def simple_lines():
    C = Canvas(**canvas_args)

    tc = 0.04

    # An example of the functional interface Artist(Canvas)
    for i in np.arange(-4, 5, 0.5):
        line(x=-4, y=i, x1=4, y1=i, thickness=tc, color=[20] * 3)(C)
        line(x=i, y=4, x1=i, y1=-4, thickness=tc, color=[20] * 3)(C)

    for i in np.arange(-4, 5, 1):
        line(x=-4, y=i, x1=4, y1=i, thickness=tc, color=[100, int(100 + i * 10), 100])(
            C
        )
        line(x=i, y=4, x1=i, y1=-4, thickness=tc, color=[100, 100, int(100 + i * 10)])(
            C
        )

    line(-4, 0, 4, 0, thickness=0.05)(C)
    line(0, 4, 0, -4, thickness=0.05)(C)

    return C


def instagram_filters():

    f_sample = "pixelhouse/filter/insta/samples/Normal.jpg"
    C = Canvas(bg="w", **canvas_args).load(f_sample)
    C += scale(fx=0.25)
    C += circle(r=0.50, color="r")
    C += instafilter("Ludwig", weight=0.80)

    return C


def teyleen_982():
    C = Canvas(**canvas_args)
    pi = np.pi

    pal = [matplotlib_colors("lavender")] + palettes(96)
    tc = 0.025

    dx = pi / 8
    t0 = dx
    t1 = 2 * pi - dx
    r = 1.8

    for n in range(6):
        ellipse(
            a=r,
            b=r,
            rotation=pi / 2,
            angle_start=t0,
            angle_end=t1,
            color=pal[n],
            thickness=tc,
        )(C)

        dx *= 1.4
        t0 = dx
        t1 = 2 * pi - dx
        r -= 0.2

    return C


def teyleen_116():
    C = Canvas(**canvas_args)
    pal = palettes(152)

    x = 0.25
    C += circle(x, x, r=x / 2, color=pal[0])
    C += circle(-x, x, r=x / 2, color=pal[1])
    C += circle(x, -x, r=x / 2, color=pal[2])
    C += circle(-x, -x, r=x / 2, color=pal[3])

    C += circle(y=x / 2, r=2 - x, color=pal[4], thickness=x / 20)
    C += circle(y=-x / 2, r=2 - x, color=pal[4], thickness=x / 20)

    return C


#########################################################################


def rotating_circles():
    A = Animation(**animation_args)
    x = motion.easeReturn("easeInOutQuad", -1, 1, len(A))

    A(circle(x, 1, r=1.25, color=[0, 250, 150], mode="add"))
    A(circle(-x, -1, r=1.25, color=[255, 5, 100], mode="add"))

    return A


def checkerboard():
    A = Animation(**animation_args)
    z = motion.easeReturn("easeInOutQuad", 0, 1, len(A))

    r = 0.20
    c = [150, 250, 0]
    coord = [-2, 0, 2]
    args = {"r": r, "color": c, "mode": "add"}

    for dx, dy in itertools.product(coord, repeat=2):
        A += circle(z + dx, z + dy, **args)
        A += circle(z + dx, -z + dy, **args)
        A += circle(-z + dx, -z + dy, **args)
        A += circle(-z + dx, z + dy, **args)

        A += circle(dx, z + dy, **args)
        A += circle(z + dx, dy, **args)

        A += circle(dx, -z + dy, **args)
        A += circle(-z + dx, dy, **args)

    return A


def timer():
    A = Animation(**animation_args)

    tc = 0.315
    r = 3.0
    lag = 0.1

    for k in range(20):

        theta = motion.offsetEase(lag, stop=2 * np.pi, duration=len(A))()

        A += line(
            x1=r * np.cos(theta),
            y1=r * np.sin(theta),
            thickness=tc,
            color="indigo",
            mode="add",
        )

        r *= 0.98
        lag *= 1.17

    return A


def pacman():
    args = animation_args.copy()
    args["duration"] = 0.5
    A = Animation(**args)

    pac_color = (253, 255, 0)

    # Chomping easing function
    dp = np.pi / 4
    x0 = motion.easeOutQuad(0, dp, len(A) // 2)()
    x1 = motion.easeInQuad(dp, 0, len(A) // 2)()
    z = np.hstack([x0, x1])

    A += ellipse(a=1, b=1, angle_start=z, angle_end=2 * np.pi - z, color=pac_color)

    return A


#########################################################################

if __name__ == "__main__":

    simple_lines().save("figures/simple_lines.png")
    simple_circles().save("figures/simple_circles.png")
    simple_rectangles().save("figures/simple_rectangle.png")

    canvas2gif(rotating_circles(), "figures/moving_circles.gif", **gif_args)
    canvas2gif(pacman(), "figures/pacman.gif", **gif_args)
    canvas2gif(checkerboard(), "figures/checkerboard.gif", **gif_args)
    canvas2gif(timer(), "figures/timer.gif", **gif_args)

    teyleen_982().save("figures/teyleen_982.png")
    teyleen_116().save("figures/teyleen_116.png")
