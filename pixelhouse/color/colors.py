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

        # Load a hex color
        if name and name[0]=="#":
            name = name.lstrip("#")

            if len(name) != 6:
                raise ValueError("Can only use full hex colors")
            
            color = list(int(name[i:i+2], 16) for i in (0, 2 ,4))

        elif name in self.colors:
            color = self.colors[name]

        else:
            color_list = self.colors.keys()
            msg = (f"{color_list} are known colors, {name} is unknown "
                   f"and not hex.")
            raise KeyError(msg)

        return color

    def __len__(self):
        return len(self.colors)
