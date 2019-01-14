from .artist import Artist
from .canvas import Canvas, load
from .animation import Animation

from . import transform
from . import motion
from . import filters
from . import color
from . import gradient

from .primitives import circle, line, ellipse, rectangle, polyline, text
from .color import palette, palette_rectangles, palette_blocks
from .io import canvas2gif, canvas2mp4
from .canvas import hstack, vstack, gridstack

from ._version import __version__
