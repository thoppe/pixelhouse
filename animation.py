import canvas
import pixelhouse.motion.easing as easing

import cv2
import os
import numpy as np
import tempfile
import scipy.interpolate

import imageio
from tqdm import tqdm

class animation():

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
            canvas.canvas(width, height, extent) for _ in
            range(n_frames)
        ]
        self.has_rendered = [False,]*len(self)
        self.timepoints = np.linspace(0, 1, len(self)+1)[:-1]

    def __len__(self):
        return len(self.frames)

    def add(self, art):
        self.artists.append(art)

    def render(self, n):
        assert(0 <= n < len(self))

        if not self.has_rendered[n]:

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

        # Convert from BGR to RGB
        #images = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in images]
        
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
            
#############################################################################

#############################################################################

if __name__ == "__main__":
    from artists import line
    
    A = animation(width=400, height=400, fps=10)

    # Use an ease function to go in an out
    tc = 0.315

    r = 3.0
    lag = 0.1
    c = [65, 0, 20]

    for k in range(20):

        theta = easing.OffsetEase(lag, stop=2*np.pi, duration=len(A))()

        L = line(
            x1=r*np.cos(theta),
            y1=r*np.sin(theta),
            thickness=tc, color=c
        )
        A.add(L)
        
        r *= 0.98
        lag *= 1.17
        
    A.show(repeat=True)
