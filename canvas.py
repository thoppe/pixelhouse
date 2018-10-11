import cv2
import numpy as np

def transform_points(fn):
    def wrapped(self, x=0, y=0, *args, **kwargs):
        
        x *= self.width / 2.0
        x /= self.extent
        x += self.width / 2

        y *= -self.height / 2.0
        y /= self.extent
        y += self.height / 2

        return fn(self, x=int(x), y=int(y), *args, **kwargs)
    return wrapped


class canvas():
    '''
    Canvas object for quad drawings. 
    Extent measures the scale in across the width.
    '''

    def __init__(
            self,
            width=400,
            height=200,
            extent=4.0,
            name='quadImage',
    ):
        self.img = np.zeros((height, width, 3), np.uint8)
        self.name = name

        self.extent = extent
        

    def __repr__(self):
        return f"Quad Image {self.height}x{self.width}, extent {self.extent}"

    @property
    def height(self):
        return self.img.shape[0]

    @property
    def width(self):
        return self.img.shape[1]

    def show(self):
        cv2.imshow(self.name, self.img)
        cv2.waitKey(0)

    @transform_points
    def circle(self, x=0, y=0, r=20, color=[255,255,255]):
        r = int(r/self.extent)
        cv2.circle(self.img, (x,y), r, color, -1)


c = canvas()
img = c.circle()
c.show()


