from . import Canvas, Artist
from .motion import easing

from contextlib import contextmanager
import cv2
import os
import numpy as np
import scipy.interpolate

from tqdm import tqdm


class Animation:
    def __init__(
        self, width=200, height=200, duration=5, fps=5, extent=4, bg="black"
    ):

        self.bg = bg
        self.extent = extent

        self.duration = duration
        self.fps = fps

        n_frames = int(fps * duration)

        self.frames = [
            Canvas(width, height, extent, bg=bg) for _ in range(n_frames)
        ]

        self.has_rendered = [False] * len(self)
        self.timepoints = np.linspace(0, 1, len(self) + 1)[:-1]

        # Keeps track of which list of artists to grab
        self.artist_stack = [[]]
        self.keyframes = np.array([0] * len(self))

    def blank(self, **kwargs):
        """
        Return a new animation object similar to this one. Any arguments passed
        in the keywords are also passed to the new object.
        """
        kws = {
            "width": self.width,
            "height": self.height,
            "bg": self.bg,
            "extent": self.extent,
            "duration": self.duration,
            "fps": self.fps,
        }
        kws.update(kwargs)

        return Animation(**kws)

    @property
    def height(self):
        return self.frames[0].height

    @property
    def width(self):
        return self.frames[0].width

    def resize(self, fx=0, fy=0, output_size=None):
        """
        Resizes the all canvas' either by a set scale or direct pixel amount
        """
        for canvas in self.frames:
            canvas.resize(fx, fy, output_size)

    @property
    def aspect_ratio(self):
        return self.frames[0].aspect_ratio

    @property
    def xmin(self):
        return self.frames[0].xmin

    @property
    def xmax(self):
        return self.frames[0].xmax

    @property
    def ymin(self):
        return self.frames[0].ymin

    @property
    def ymax(self):
        return self.frames[0].ymax

    def __len__(self):
        return len(self.frames)

    def __call__(self, art):
        self.artist_stack[-1].append(art)
        return self

    def __iadd__(self, rhs):
        """
        Add an Artist to the canvas, or if another animation, extend the
        animation from the rhs.
        """
        if isinstance(rhs, Artist):
            self(rhs)
        elif isinstance(rhs, Animation):
            self.frames.extend(rhs.frames)
            self.has_rendered.extend(rhs.has_rendered)
            self.timepoints = np.hstack([self.timepoints, rhs.timepoints])
            self.duration += rhs.duration
            self.artist_stack.extend(rhs.artist_stack)

            new_keyframes = rhs.keyframes.copy()
            new_keyframes += self.keyframes.max() + 1
            self.keyframes = np.hstack([self.keyframes, new_keyframes])

        else:
            raise TypeError(f"Can't combine a Animation with a {type(rhs)}")

        return self

    def render_all(self):
        for n in range(len(self)):
            self.render(n)

    def render(self, n):
        assert 0 <= n < len(self)

        if not self.has_rendered[n]:

            t = self.timepoints[n]

            artists = self.artist_stack[self.keyframes[n]]
            for art in artists:
                art.draw(self.frames[n], t)

            self.has_rendered[n] = True

            # Copy any shared attributes to the next frame
            if n < len(self) - 1:
                self.frames[n + 1].shared_attributes.update(
                    self.frames[n].shared_attributes
                )

        return self.frames[n]

    def show(self, delay=50, repeat=True):  # pragma: no cover

        is_status_bar = True
        while True:
            if is_status_bar:
                ITR = tqdm(range(len(self)))
                is_status_bar = False
            else:
                ITR = range(len(self))

            for n in ITR:
                img = self.render(n)
                img.show(1)
                key = cv2.waitKey(50)
                if key != -1:
                    return False

            if not repeat:
                break

    @contextmanager
    def layer(self):
        canvas = _CanvasLayer()
        yield canvas
        self(canvas)


class _CanvasLayer:
    """
    Keep track of the artists when used in a layer.
    """

    def __init__(self):
        self.artists = []

    def __iadd__(self, art):
        self.artists.append(art)
        return self

    def draw(self, cvs, t=0.0):
        with cvs.layer() as C:
            for art in self.artists:
                art.draw(C, t)

    @contextmanager
    def layer(self):  # pragma: no cover
        msg = "Nested layers in Animation are not possible yet."
        raise NotImplementedError(msg)
