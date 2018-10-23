import cv2
import numpy as np
import collections
from .color import matplotlib_colors

class Canvas():
    '''
    Basic canvas object for quad drawings. 
    Extent measures along the x-axis.
    '''

    def __init__(
            self,
            width=200,
            height=200,
            extent=4.0,
            name='pixelhouseImage',
    ):
        self._img = np.zeros((height, width, 3), np.uint8)
        self.name = name
        self.extent = extent
        

    def __repr__(self):
        return (
            f"pixelhouse (w/h) {self.height}x{self.width}, " \
            f"extent {self.extent}"
        )

    @property
    def height(self):
        return self._img.shape[0]

    @property
    def width(self):
        return self._img.shape[1]

    @property
    def img(self):
        return self._img

    
    def cv2_draw(self, func, args, blend, **kwargs):
        # Saturate or blend the images together
        if blend:
            dst = Canvas(self.width, self.height).img
            func(dst, *args)
            cv2.add(self._img, dst, self._img)
        else:
            func(self._img, *args)


    def transform_x(self, x):
        x *= self.width / 2.0
        x /= self.extent
        x += self.width / 2
        return int(x)

    def transform_y(self, y):
        y *= -self.height / 2.0
        y /= self.extent
        y += self.height / 2        
        return int(y)

    def transform_length(self, r, is_discrete=True):
        r *= (self.width/self.extent)
        if is_discrete:
            return int(r)
        return r

    def transform_kernel_length(self, r):
        # Kernels must be positive and odd integers
        r = self.transform_length(r, is_discrete=False)

        remainder = r%2
        r = int(r - r%2)
        r += -1 if remainder < 1 else 1

        r = max(1, r)
        return r
    
    def transform_thickness(self, r):
        # If thickness is negative, leave it alone
        if r>0:
            return self.transform_length(r)
        return r
    

    def transform_color(self, c):
        if isinstance(c, str):
            return matplotlib_colors(c)
        return c

    @staticmethod
    def transform_angle(rads):
        # From radians into degrees, counterclockwise
        return -rads*(360/(2*np.pi))
    
    @staticmethod
    def get_lineType(antialiased):
        if antialiased:
            return cv2.LINE_AA
        return 8

    def load(self, f_image):
        raise NotImplementedError

    def show(self, delay=0):
        # Before we show we have to convert back to BGR
        dst = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
        
        cv2.imshow(self.name, dst)
        cv2.waitKey(delay)

    def save(self, f_save):
        # Before we save we have to convert back to BGR
        dst = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(f_save, dst)


######################################################################


if __name__ == "__main__":
    from artists import circle
    
    cvs = Canvas(200,200,extent=4)

    color = 'olive'
    circle(thickness=0.5,color='olive')(cvs)
    
    cvs.show()
    
