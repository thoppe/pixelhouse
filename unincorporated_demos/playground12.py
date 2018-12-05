import pixelhouse as ph
import numpy as np
from scipy.ndimage.measurements import center_of_mass

pal = ph.palette(3)
g = ph.gradient.linear([pal[2], pal[3]])


class squish(ph.transform.elastic.ElasticTransform):
    def __init__(self, art):
        self.art = art
        self.dt = 0.01

    def measure_CoM(self, cvs, t):
        bg = cvs.copy()
        self.art.draw(bg, t)
        mask = bg.alpha / 255

        y, x = center_of_mass(mask)
        cx = cvs.inverse_transform_x(x)
        cy = cvs.inverse_transform_y(y)

        return np.array([cx, cy])

    def draw(self, cvs, t=0.0):

        gravity = 5.0

        # c0 = self.measure_CoM(cvs, t-self.dt)
        # c1 = self.measure_CoM(cvs, t)
        # c2 = self.measure_CoM(cvs, t+self.dt)

        ca = self.measure_CoM(cvs, t - self.dt * 3)
        c0 = self.measure_CoM(cvs, t - self.dt * 2)
        c1 = self.measure_CoM(cvs, t - self.dt)
        c2 = self.measure_CoM(cvs, t)

        cm = np.array([ca, c0, c1, c2]).T
        print(cm[1].dtype, cm.dtype, type(cm[1][2]))

        # Fit with spline?
        from scipy.interpolate import splrep

        S = splrep(cm[0], cm[1], k=1)
        print(S)
        exit()

        # Finite second-order difference scheme
        acc = (c0 - 2 * c1 + c2) / self.dt ** 2
        acc /= gravity

        print(acc)
        cvs += ph.text(f"x={acc[0]:0.2f}", y=1.5, font="TitilliumWeb-Black.ttf")
        cvs += ph.text(
            f"y={acc[1]:0.2f}", y=-1.5, font="TitilliumWeb-Black.ttf"
        )
        return

        coords = cvs.grid_coordinates()
        y = cvs.inverse_transform_y(coords[1].astype(float))
        x = cvs.inverse_transform_x(coords[0].astype(float))

        dist = np.sqrt((c1[0] - x[:, :, 0]) ** 2 + (c1[1] - y[:, :, 0]) ** 2)
        dist = np.dstack([dist] * 4)

        dx = dist * (-acc[0])
        dy = 0 * (dist * acc[1])

        # print(c0,c1,c2)
        print(t, acc[1])
        # print(dx.max())

        self.transform(cvs, dy, dx, coords, "nearest", order=0)
        """
        
        import pylab as plt
        plt.imshow(dx[:,:,0])
        plt.colorbar()
        plt.show()


        exit()
        
        print(acc)
        """


C = ph.Animation(400, 200, fps=20)
b = ph.motion.easeInOutQuad(-2, 2, flip=True)
q = ph.circle(x=b, y=0, r=0.5, gradient=g)

C += q
C += squish(q)

C.show()
