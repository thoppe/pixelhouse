from .canvas import Canvas
from .motion import easing

import cv2
import os
import numpy as np
import scipy.interpolate

from tqdm import tqdm

class Animation():

    def __init__(
            self,
            duration=5, fps=5,
            width=200, height=200, extent=4,
            bg='black',
    ):
        
        self.duration = duration
        self.fps = fps
        self.artists = []

        n_frames = int(fps*duration)

        self.frames = [
            Canvas(width, height, extent, bg=bg) for _ in
            range(n_frames)
        ]
        self.has_rendered = [False,]*len(self)
        self.timepoints = np.linspace(0, 1, len(self)+1)[:-1]

    def __len__(self):
        return len(self.frames)

    def __call__(self, art):
        self.artists.append(art)
        return self

    def render(self, n):
        assert(0 <= n < len(self))

        if not self.has_rendered[n]:

            t = self.timepoints[n]

            for art in self.artists:
                art(self.frames[n], t)

            self.has_rendered[n] = True

            # Copy any shared attributes to the next frame
            if n < len(self)-1:
                self.frames[n+1].shared_attributes.update(
                    self.frames[n].shared_attributes)

        return self.frames[n]

    def show(self, delay=50, repeat=True):

        is_status_bar = True
        while True:
            if is_status_bar:
                ITR = tqdm(range(len(self)))
                is_status_bar = False
            else:
                ITR = range(len(self))
                
            for n in ITR:
                img = self.render(n)
                img.show(delay=delay)
            if not repeat:
                break
