from pixelhouse import Canvas, circle
import pixelhouse as ph
import numpy as np


def draw_circles(C):
    """
    This function draws the shaded circles to the screen. We are drawing
    them in a function so we can reuse them quickly for blending.
    """

    # Palette #19 is a good predefined palette with whites and blues
    pal = ph.palette(19)

    # The base radius of our circles. Everything will scale from this
    radius = 1.60
    offset = 0.50
    tc = 0.2  # Base thickness

    # All the circles will have a linear gradient from top to bottom,
    # or bottom to top (we use theta for that). The second parameter [1, 0]
    # controls the alpha (the transparency). The sizing and thickness was
    # choosen by hand to get a nice effect.

    lg = ph.gradient.linear([pal[0], pal[1]], [1, 0], theta=-np.pi / 2)
    C += circle(0, 0, radius + offset, thickness=tc, gradient=lg)

    lg = ph.gradient.linear([pal[0], pal[1]], [1, 0], theta=np.pi / 2)
    C += circle(0, 0, radius - 2 * offset, thickness=tc / 2, gradient=lg)

    lg = ph.gradient.linear([pal[2], pal[1]], [1, 0], theta=-np.pi / 2)
    C += circle(0, 0, radius - offset, thickness=tc / 2, gradient=lg)

    lg = ph.gradient.linear([pal[2], pal[1]], [1, 0], theta=np.pi / 2)
    C += circle(0, 0, radius + 1.5 * offset, thickness=tc / 2, gradient=lg)


# Start a new canvas and load in an image. It will resize automatically.
C = Canvas().load("asphalt-dark-dawn-531321.jpg")

# Apply the instagram-like filter named 1977.
# Use ph.filters.instafilter("") to get a list of all known.
C += ph.filters.instafilter("1977")

# Start a new layer. This uses the current image as a background, and then
# applies it after the context is over.
with C.layer() as layer:

    # Draw the circles, blend, then draw them again.
    # This makes them have a glowy effect.
    draw_circles(layer)
    layer += ph.filters.gaussian_blur()
    draw_circles(layer)

C.save("figures/blue_woods.png")
C.show()
