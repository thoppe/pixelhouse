import pixelhouse as ph
import numpy as np
from scipy import interpolate

pal = ph.palette(3)
g = ph.gradient.linear([pal[2], pal[3]])


class squish(ph.transform.elastic.ElasticTransform):
    def __init__(self, art):
        self.art = art
        self.dt = 0.001

    def draw(self, cvs, t=0.0):

        gravity = 5.0
        npts = 5

        # Measure the CM along a few fixed points back in time
        u = np.linspace(t-(npts-1)*self.dt, t, npts)
        CM = np.array([self.art.center_of_mass(_t) for _t in u]).T

        tck, _ = interpolate.splprep(CM, u=u, s=0)

        r = np.array(interpolate.splev(t, tck, der=0,ext=2))
        v = np.array(interpolate.splev(t, tck, der=1,ext=2))
        a = np.array(interpolate.splev(t, tck, der=2,ext=2))

        font = "TitilliumWeb-Black.ttf"

        cvs += ph.text(f"x={r[0]:0.2f}",y=1.5,font_size=0.3, font=font)
        cvs += ph.text(f"v={v[0]:0.2f}",y=-1.0,x=-2,font_size=0.3,font=font)
        cvs += ph.text(f"a={a[0]:0.2f}",y=-1.0,x=2,font_size=0.3,font=font)

        aT = (r[0]*a[0] + r[1]*a[1]) * self.dt / np.linalg.norm(v)
        aN = (v[1]*a[0] - v[0]*a[1]) * self.dt**2 / np.linalg.norm(v)
        print(aT, aN)

        return False

        '''
        coords = cvs.grid_coordinates()
        y = cvs.inverse_transform_y(coords[1].astype(float))
        x = cvs.inverse_transform_x(coords[0].astype(float))

        dist = np.sqrt((c1[0] - x[:,:,0])**2 + (c1[1]-y[:,:,0])**2)
        dist = np.dstack([dist,]*4)

        dx = dist * (-acc[0])
        dy = 0*(dist * acc[1])

        self.transform(cvs, dy, dx, coords, 'nearest', order=0)
                
        import pylab as plt
        plt.imshow(dx[:,:,0])
        plt.colorbar()
        plt.show()


        exit()
        
        print(acc)
        '''

C = ph.Animation(400, 200, fps=20)
b = ph.motion.easeInOutQuad(-2, 2, flip=True)
q = ph.circle(x=b, y=0, r=0.5, gradient=g)

C += q
C += squish(q)

C.show()
