from .canvas import Canvas
from .motion import easing

import cv2
import os
import numpy as np
import tempfile
import scipy.interpolate

import imageio
from tqdm import tqdm

class Animation():

    def __init__(
            self,
            duration=5, fps=5,
            width=200, height=200, extent=4
    ):
        
        self.duration = duration
        self.fps = fps
        self.artists = []

        n_frames = int(fps*duration)

        self.frames = [
            Canvas(width, height, extent) for _ in
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
            print(f"Rendering {n}/{len(self)}")

            t = self.timepoints[n]

            for art in self.artists:
                art(self.frames[n], t)

            self.has_rendered[n] = True

        return self.frames[n]

    def show(self, delay=50, repeat=True):
        while True:
            for n in range(len(self)):
                img = self.render(n)
                img.show(delay=delay)
            if not repeat:
                break

    def to_gif(self, f_gif, palettesize=256, gifsicle=False):
        images = [self.render(n).img for n in range(len(self))]
        
        imageio.mimsave(f_gif, images,
                        #fps=self.fps*2,
                        #duration=self.duration,
                        duration=self.duration/self.fps,
                        palettesize=palettesize, subrectangles=True)
        fs = os.stat(f_gif).st_size
        print(f"Rendered {f_gif}, filesize {fs}")

        if gifsicle:
            cmd = f"gifsicle -i {f_gif} --colors {palettesize} -O3 -o {f_gif}"
            os.system(cmd)
            fs = os.stat(f_gif).st_size
            print(f"gifsicle reduced filesize to {fs}")
            
    def to_mp4(self, f_mp4, loop=1):

        with tempfile.TemporaryDirectory() as tmp_dir:

            for n,img in tqdm(enumerate(self.frames)):
                self.render(n)
                img.save(f"{tmp_dir}/{n:04d}.png")
            
            cmd = f'ffmpeg -loop 1 -t {self.duration*loop} ' \
                  f'-y -framerate {self.fps} -i {tmp_dir}/%04d.png ' \
                  f'-c:v libx264 -profile:v high -crf 10 -pix_fmt yuv420p '\
                  f'{f_mp4}'

            os.system(cmd)

            fs = os.stat(f_mp4).st_size
            print(f"Rendered {f_mp4}, filesize {fs}")
