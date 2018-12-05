import os
import json
import numpy

_script_path = os.path.dirname(os.path.abspath(__file__))


class ColorLoversPalette:
    """
    Nice palettes from ...
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
