import random
import numpy as np
import pixelhouse as ph

# Start with a good predefined color palette.
# Palette 20 has a bunch of muted reds and blues.
pal = ph.palette(20)

# Split the colors into our primary and background colors.
background_color, primary_colors = pal[0], pal[1:]

# Since we are choosing the colors randomly, if we set a seed we get
# the same result each time.
random.seed(44)

# Setup our canvas! Let's make it 400 by 400 pixels, and use the first palette
# color as the background.
canvas = ph.Canvas(400, 400, bg=background_color)

# Draw circles in lines down the screen. To give it a wavy fell,
# we want every other circle to be offset a bit.
radius = 0.40

for k, y in enumerate(np.arange(-6, 6, radius)):

    for x in np.arange(-6, 6, radius * 2.5):

        # If k is odd (eg. every other one), offset it!
        if k % 2:
            x += radius/2

        # Pick a random color
        color = random.choice(primary_colors)

        # Draw a circle to the canvas by "adding" to it
        canvas += ph.circle(x=x, y=y, r=radius, color=color)

# Save the image.
canvas.save("figures/circle_lines.png")

# Display the image. It'll stay open until you press a key.
canvas.show()
