import pixelhouse as ph

# Show (and save the top 20 palettes from pixelhouse)
canvas = ph.palette_blocks(range(20))
canvas.save("figures/palettes_top_20.jpg")

canvas.show()




