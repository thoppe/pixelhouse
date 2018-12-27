import os
import json
import numpy as np
import collections

_script_path = os.path.dirname(os.path.abspath(__file__))


class ColorLoversPalette:
    """
    Nice palettes inspired by https://www.colourlovers.com/
    """

    def __init__(self, colorset=1000):
        # Load the top 1000 by default

        f_palette = os.path.join(_script_path, f"palettes/{colorset}.json")
        self.f_palette = f_palette
        self.colors = None

    def _load_colors(self):
        # Lazy load the colors
        with open(self.f_palette) as FIN:
            raw = FIN.read()

        self.colors = json.loads(raw)

    def __call__(self, n):
        if self.colors is None:
            self._load_colors()

        if n > len(self.colors):
            msg = f"Only {len(self)} palettes known, requested number {n}"
            raise KeyError(msg)

        pal = [x + [255] for x in self.colors[n]]

        return pal

    def __len__(self):
        return len(self.colors)


def palette_rectangles(n, show_number=True, width=400, ratio=7):
    """
    Returns a canvas that shows the what palette "n" looks like.

    Example: 
         palette_rectangle(42).show()
    """

    from .. import Canvas, rectangle, text, palette

    extent = 4
    C = Canvas(width, width // ratio, extent=extent, bg="w")

    pal = palette(n)
    segments = np.linspace(-extent, extent, len(pal) + 2)

    for x0, x1, c in zip(segments, segments[1:], pal):
        C += rectangle(x0, -extent / ratio, x1, extent / ratio, color=c)

    if show_number:
        C += text(x=0.83 * extent, text=str(n), color="k", font_size=0.75)

    return C


def palette_blocks(palette_numbers, columns=2, show_number=True, width=400):
    """
    Returns a canvas that shows what a list (palette_numbers) of palettes 
    look like.
    
    Example: 
         palette_blocks(range(20)).show()
    """

    from .. import gridstack

    if not palette_numbers:
        raise ValueError("Need to pass in a list of palette numbers to show")

    if len(palette_numbers) < columns:
        raise ValueError("Need to pass in at least as many palettes as columns")

    blocks = collections.defaultdict(list)
    row = 0

    for n in palette_numbers:
        canvas = palette_rectangles(n, show_number=show_number, width=width)
        blocks[row].append(canvas)
        row = (row + 1) % ((len(palette_numbers) + 1) // columns)

    blocks = [blocks[k] for k in blocks]

    # Pad out irregular number of items
    m = len(blocks[0])

    while len(blocks[-1]) != m:
        blocks[-1].append(canvas.blank())

    C = gridstack(blocks)
    return C
