# Experimenting with a new kind of transform (see resist.png for an example)

import pixelhouse as ph
import numpy as np
import cv2
from pixelhouse.artist import constant


def erosion_distance(canvas, kernel_size=5, depth_iterations=3, decay=0.90):
    dist = np.zeros(shape=canvas.shape[:2], dtype=float)
    dist += canvas.alpha / 255
    mask = dist.astype(np.uint8)

    ks = kernel_size
    kernel = np.ones((ks, ks), np.uint8)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ks, ks))

    gamma = 1.0
    for k in range(depth_iterations):
        gamma *= decay
        mask = cv2.erode(mask, kernel, iterations=3)
        dist += gamma * mask

    return dist


class rise(ph.transform.elastic.ElasticTransform):
    dist = constant(None)
    amplitude = constant(0.02)
    theta = constant(0.0)
    mode = constant("constant")

    args = ("dist", "amplitude", "theta", "mode")

    def draw(self, cvs, t=0.0):
        coords = cvs.grid_coordinates()

        cx = coords[0][:, :, 0]
        cy = coords[1][:, :, 0]
        dist = self.dist(t)

        dx = np.zeros_like(coords[0]).astype(np.float)
        dy = np.zeros_like(coords[1]).astype(np.float)

        dist = np.array(dist)

        theta = self.theta(t)
        amplitude = cvs.transform_length(self.amplitude(t), is_discrete=False)

        dy += amplitude * np.cos(theta) * dist[:, :, np.newaxis]
        dx += amplitude * np.sin(theta) * dist[:, :, np.newaxis]

        dy[:, :, 0] *= 0

        self.transform(cvs, dy, dx, coords, self.mode(t), order=0)


pal = ph.palette(13)
# w,h = 3*600, 3*200
scale = 4
w, h = scale * 600, scale * 400

C = ph.Canvas(w, h)
C += ph.text(
    "RESIST",
    x=0,
    y=0.5,
    font="TitilliumWeb-Black.ttf",
    vpos="center",
    font_size=2.50,
)

dist = erosion_distance(
    C, kernel_size=3, decay=0.8, depth_iterations=20
).tolist()

C = ph.Animation(w, h, bg=pal[-1])

n, tc = 40, 0.020
lg = ph.gradient.linear([pal[0], pal[1]])


for y in np.linspace(1.25 * C.ymin, 1.25 * C.ymax, n):
    C += ph.line(C.xmin, y, C.xmax, y, thickness=tc, gradient=lg)
C += ph.filters.gaussian_blur(0.10, 0.10)
for y in np.linspace(1.25 * C.ymin, 1.25 * C.ymax, n):
    C += ph.line(C.xmin, y, C.xmax, y, thickness=tc, gradient=lg)

z = ph.motion.easeInQuad(0, 0.030, flip=True)
C += rise(dist, amplitude=z)

X = C.render(len(C) // 2)
X += ph.transform.scale(1.0 / scale, 1.0 / scale)
X += ph.filters.gaussian_blur(0.50, 0)
X.show()
X.save("../examples/figures/resist.png")
C.show()
