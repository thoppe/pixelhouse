"""
Functions to save and load gifs and mp4. Ignore coverage on this file since
it relies on outside programs.
"""

from . import Animation
from tqdm import tqdm

import imageio
import tempfile
import os


def canvas2gif(
    A, f_gif, palettesize=256, gifsicle=False, duration=None
):  # pragma: no cover
    images = [A.render(n).img for n in tqdm(range(len(A)))]

    if duration == None:
        duration = A.duration / A.fps

    imageio.mimsave(
        f_gif,
        images,
        duration=duration,
        palettesize=palettesize,
        subrectangles=True,
    )

    fs = os.stat(f_gif).st_size
    print(f"Rendered {f_gif}, filesize {fs}")

    if gifsicle:
        cmd = f"gifsicle -i {f_gif} --colors {palettesize} -O3 -o {f_gif}"
        os.system(cmd)
        fs = os.stat(f_gif).st_size
        print(f"gifsicle reduced filesize to {fs}")


def canvas2mp4(A, f_mp4, loop=1):  # pragma: no cover

    with tempfile.TemporaryDirectory() as tmp_dir:

        for n, img in tqdm(enumerate(A.frames)):
            A.render(n)
            img.save(f"{tmp_dir}/{n:04d}.png")

        cmd = (
            f"ffmpeg -loop 1 -t {A.duration*loop} "
            f"-y -framerate {A.fps} -i {tmp_dir}/%04d.png "
            f"-c:v libx264 -profile:v high -crf 10 -pix_fmt yuv420p "
            f"{f_mp4}"
        )

        os.system(cmd)

        fs = os.stat(f_mp4).st_size
        print(f"Rendered {f_mp4}, filesize {fs}")
