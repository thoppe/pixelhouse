import os
import json
import numpy

_script_path = os.path.dirname(os.path.abspath(__file__))


class NamedColors:
    """
    Named colors from matplotlib
    """

    def __init__(self, f_colors=None):

        if f_colors is None:
            f_colors = os.path.join(
                _script_path, "named_colors", "matplotlib.json"
            )

        self.f_colors = f_colors
        self.colors = None

    def _load_colors(self):
        # Lazy load the colors

        with open(self.f_colors) as FIN:
            raw = FIN.read()

        self.colors = json.loads(raw)

    def __call__(self, name):
        if self.colors is None:
            self._load_colors()

        if name not in self.colors:
            color_list = self.colors.keys()
            msg = f"{color_list} are known colors, {name} is unknown."
            raise KeyError(msg)

        color = self.colors[name]

        # Add in the alpha channel
        return color

    def __len__(self):
        return len(self.colors)
