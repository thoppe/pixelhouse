import json
import os
import random

script_path = os.path.dirname(os.path.abspath(__file__))

# For now only use the top 200
f_palette = os.path.join(script_path, 'nice_color_palettes/200.json')

def hex_to_rgb(h):
    # https://stackoverflow.com/a/29643643/249341
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    
with open(f_palette) as FIN:
    raw = FIN.read()
    colors = json.loads(raw)

def get_palette(n):
    return list(map(hex_to_rgb, colors[n]))
