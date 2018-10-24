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
            bg='black',
            name='pixelhouseImage',
    ):
        channels = 4
        self._img = np.ones((height, width, channels), np.uint8)

        self.bg = bg
        #bg = np.array(self.transform_color(bg)).astype(np.uint8)
        #bg[3] = 0
        #self._img *= bg
        
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

    def blank(self):
        # Return an empty canvas of the same size
        return Canvas(self.width, self.height, bg=self.bg)

    def combine(self, rhs, mode="overlay"):
        if(rhs.width != self.width):
            raise ValueError("Can't combine images with different widths")

        if(rhs.height != self.height):
            raise ValueError("Can't combine images with different heights")

        if mode == "overlay":
            self.overlay(rhs)
        elif mode == "add":
            cv2.add(self._img, rhs.img, self._img)
        elif mode == "subtract":
            cv2.subtract(self._img, rhs.img, self._img)
        else:
            raise ValueError(f"Unknown mode {mode}")

    
    def cv2_draw(self, func, args, mode, **kwargs):
        if mode=='direct':
            func(self._img, *args)
        else:
            rhs = self.blank()
            func(rhs.img, *args)
            self.combine(rhs, mode=mode)

    def overlay(self, rhs):
        # https://stackoverflow.com/a/37198079/249341
        overlay_t_img = rhs.img
        face_img = self.img[:, :, :3]

        # Split out the transparency mask from the colour info
        overlay_img = overlay_t_img[:,:,:3] # Grab the BRG planes
        overlay_mask = overlay_t_img[:,:,3:]  # And the alpha plane

        # Again calculate the inverse mask
        background_mask = 255 - overlay_mask

        # Turn the masks into three channel, so we can use them as weights
        overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
        background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

        # Create a masked out face image, and masked out overlay
        # We convert the images to floating point in range 0.0 - 1.0
        dx = 1 / 255.0

        overlay_part = (overlay_img*dx) * (overlay_mask*dx)
        face_part = (face_img*dx) * (background_mask*dx)

        # And finally just add them together,
        # and rescale it back to an 8bit integer image    
        self._img = np.uint8(cv2.addWeighted(
            face_part, 255.0, overlay_part, 255.0, 0.0))

        # Add back in a fully opaque channel
        alpha = 255*np.ones_like(self._img[:,:,0])
        self._img = np.dstack((self._img, alpha))

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
            c = matplotlib_colors(c)

        # Force add in the alpha channel
        if len(c) == 3:
            c += [255,]

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
    
