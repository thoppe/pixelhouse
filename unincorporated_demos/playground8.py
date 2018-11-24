import pixelhouse as ph

C = ph.Canvas(height=200,width=800, bg='k')

pal = ph.palette(1)
lg = ph.linear_gradient(colors=[pal[0], pal[3], pal[0]])
C += ph.rectangle(C.xmin, C.ymin, C.xmax,C.ymax, gradient=lg)
C.show()

#lg = ph.linear_gradient(color0=pal[0], color1=pal[3], interpolation="RGB")
#C += ph.rectangle(C.xmin, C.ymin, C.xmax,C.ymax, gradient=lg)
#C.show()
