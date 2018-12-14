import numpy as np
import pixelhouse as ph

# Palette #6 looks like the beach
pal = ph.palette(6)

canvas = ph.Canvas(400, 400, bg=pal[2])

# Draw a circle, fuzz it, then draw it again
canvas += ph.circle(color=pal[3])
canvas += ph.filters.gaussian_blur()
canvas += ph.circle(color=pal[3])

# Build a nice but subtle linear gradient for the text
# Angle it at -45 degress (-pi/4)
lg = ph.gradient.linear([pal[0], pal[1]], theta=-np.pi / 4)

# Draw the text and repeat it vertically
for i in np.arange(-6, 6, 1.0):
    canvas += ph.text("pixelhouse", y=i, gradient=lg)

canvas.save("figures/logo_pixelhouse.png")
canvas.show()
