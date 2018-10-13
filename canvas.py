import cv2
import numpy as np

class canvas():
    '''
    Canvas object for quad drawings. Extent measures along the x-axis.
    '''

    def __init__(
            self,
            width=200,
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

    def transform_coordinates(self, x, y):
        x *= self.width / 2.0
        x /= self.extent
        x += self.width / 2

        y *= -self.height / 2.0
        y /= self.extent
        y += self.height / 2
        print(x,y)
        return (int(x), int(y))

    def transform_length(self, r):
        r *= (self.width/self.extent)
        return int(r)

    def show(self):
        cv2.imshow(self.name, self.img)
        cv2.waitKey(0)

    def circle(self, x=0, y=0, r=1, color=[255,255,255],
               thickness=-1, antialiased=True):
        x, y = self.transform_coordinates(x, y)
        r = self.transform_length(r)
        thickness = self.transform_length(thickness)

        if antialiased:
            lineType = cv2.LINE_AA
        else:
            lineType = 8

        cv2.circle(self.img, (x, y), r, color, thickness, lineType)

c = canvas(200,200,extent=4)
c.circle(x=1, y=0.5, r=1)
c.circle(x=-1, y=0.5, r=1, color=[255,0,0])

c.show()


