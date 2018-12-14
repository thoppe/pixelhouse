import random
import numpy as np
import pixelhouse as ph


# Inspired by
# https://dev.to/agathacco/how-to-create-pure-css-illustrations-and-animate-them---part-1-1j1k

# Setup our canvas! Make it 400 by 400 pixels,
canvas = ph.Canvas(400, 400, bg='navy') #FEEE9D

# Face shadow
canvas += ph.circle(0.1, -0.1, color='w') #EFBB42

# Face 150/170
canvas += ph.circle(0, 0, color='yellow') #FBD671

# Eyes #20184E
x = 0.75
canvas += ph.ellipse(x,  x, a=x*(3/10), b=x*(5/10),color='k')
canvas += ph.ellipse(-x,  x, a=x*(3/10), b=x*(5/10),color='k')

# Pupils #FBD671; 
canvas += ph.ellipse(x-x/15, x+x/10, a=x/6, b=x/4,color='w')
canvas += ph.ellipse(-x-x/15, x+x/10, a=x/6, b=x/4,color='w')


# Mouth #20184E
canvas += ph.ellipse(0,  -1, a=0.75, b=0.50,
                     angle_start=np.pi, angle_end=2*np.pi,color='k')

# Tounge color #F15962; 100/80
# Display the image. It'll stay open until you press a key.
canvas.show()
