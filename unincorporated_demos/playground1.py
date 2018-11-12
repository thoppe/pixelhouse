# A working file to test various aspects of the module
import numpy as np
from pixelhouse import Canvas, Animation, circle, rectangle
from pixelhouse.filter import gaussian_blur

C1 = Canvas(width=400, height=400, bg='purple')
C1 += circle(x=0, color='w')

C2 = C1.blank()
C2 += circle(x=0, y=2, r=0.7, color='r')

C3 = C1.blank('w')
C3 += circle(x=0, y=-2, r=0.7,color='k')

C1 += gaussian_blur(blur_x=2)
C1 += circle(x=0, color='w')
C2 += circle(x=0, y=2, r=0.7, color='r')

C1 += C3
C1 += C2
C1.show()
