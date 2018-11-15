from contextlib import contextmanager
import cv2
import numpy as np
import collections
from . import Artist
from .color import matplotlib_colors


class Canvas:
    """
    Basic canvas object for pixelhouse drawings. 
    Extent measures along the x-axis.
    """

    def __init__(
        self,
        width=200,
        height=200,
        extent=4.0,
        bg="black",
        name="pixelhouseImage",
        shift=8,
    ):
        channels = 4
        self._img = np.zeros((height, width, channels), np.uint8)
        self.shift = shift

        # Assign the background color, but make sure it is fully transparent
        # needed for antialiased edges
        self.bg = bg
        bg = np.array(self.transform_color(bg)).astype(np.uint8)
        bg[3] = 0
        self._img[:, :] = bg

        self.name = name
        self.extent = extent

        # When animating, we may want to pass attributes from one canvas
        # to another. Do so in the shared_attributes
        self.shared_attributes = {}

    def __repr__(self):
        return (
            f"pixelhouse (w/h) {self.height}x{self.width}, "
            f"extent {self.extent}"
        )

    @property
    def height(self):
        return self._img.shape[0]

    @property
    def width(self):
        return self._img.shape[1]

    @property
    def channels(self):
        return self._img.shape[2]

    @property
    def img(self):
        return self._img

    @property
    def shape(self):
        return self.height, self.width, self.channels

    @property
    def alpha(self):
        """
        Return the alpha channel from the image
        """
        return self.img[:, :, 3]

    def blank(self, bg=None):
        # Return an empty canvas of the same size
        if bg is None:
            bg = self.bg

        return Canvas(self.width, self.height, bg=bg)

    def copy(self, bg=None, transparent=False):
        # Returns a deep copy of this canvas
        cvs = Canvas(self.width, self.height, bg=self.bg)
        cvs._img = self.img.copy()

        if transparent:
            cvs._img[:, :, 3] = 0

        return cvs

    def __call__(self, art=None):
        """
        Calls an artist on the canvas.
        """
        if art is not None:
            art(self)
        return self

    def __len__(self):
        """
        Return 2 so calling functions work seamlessly between 
        Canvas and Animation (allows for interpolation to not complain).
        """
        return 2

    def combine(self, rhs, mode="blend"):
        if rhs.width != self.width:
            raise ValueError("Can't combine images with different widths")

        if rhs.height != self.height:
            raise ValueError("Can't combine images with different heights")

        if mode == "blend":
            self.blend(rhs)
        elif mode == "add":
            cv2.add(self._img, rhs.img, self._img)
        elif mode == "subtract":
            cv2.subtract(self._img, rhs.img, self._img)
        else:
            raise ValueError(f"Unknown mode {mode}")

        return self

    def __iadd__(self, rhs):
        """
        Add an Artist to the canvas, or combine two canvas depending
        on what the rhs is.
        """
        if isinstance(rhs, Artist):
            self(rhs)
        elif isinstance(rhs, Canvas):
            self.combine(rhs)
        else:
            raise TypeError(f"Can't combine a Canvas with a {type(rhs)}")

        return self

    def cv2_draw(self, func, args, mode, **kwargs):

        if mode == "direct":
            func(self._img, *args)
        elif mode == "gradient":
            rhs = self.blank()
            func(rhs.img, *args)
            kwargs["gradient"](self, t=kwargs["t"], mask=rhs)
        else:
            rhs = self.blank()
            func(rhs.img, *args)
            self.combine(rhs, mode)

    def blend(self, rhs):
        # Smooth the image based off the alpha from the mask image

        a = rhs.alpha.reshape(self.height, self.width, -1).astype(np.float32)
        a /= 255

        MX = (1 - a) * self._img + a * rhs._img
        MX = np.clip(MX, 0, 255).astype(np.uint8)
        self._img = MX

    def transform_x(self, x, is_discrete=True, use_shift=False):
        x *= self.width / 2.0
        x /= self.extent
        x += self.width / 2.0

        if is_discrete:
            if use_shift and self.shift:
                x *= 2 ** self.shift
            return int(x)

        return x

    def inverse_transform_x(self, x):
        x -= self.width / 2
        x *= self.extent
        x /= self.width / 2.0
        return x

    def transform_y(self, y, is_discrete=True, use_shift=False):
        y *= -self.height / 2.0
        y /= self.extent
        y += self.height / 2.0
        if is_discrete:
            if use_shift and self.shift:
                y *= 2 ** self.shift
            return int(y)
        return y

    def inverse_transform_y(self, y):
        y -= self.height / 2
        y *= self.extent
        y /= self.height / 2.0
        return y

    def transform_length(self, r, is_discrete=True, use_shift=False):
        r *= float(self.width) / self.extent

        if use_shift and self.shift:
            r *= 2 ** self.shift

        if is_discrete:
            return int(r)
        return r

    def transform_kernel_length(self, r):
        # Kernels must be positive and odd integers
        r = self.transform_length(r, is_discrete=False)

        remainder = r % 2
        r = int(r - r % 2)
        r += -1 if remainder < 1 else 1

        r = max(1, r)
        return r

    def transform_thickness(self, r):
        # If thickness is negative, leave it alone
        if r > 0:
            return self.transform_length(r)

        return r

    def transform_color(self, c):
        if isinstance(c, str):
            c = matplotlib_colors(c)

        # Force add in the alpha channel
        if len(c) == 3:
            c = list(c) + [255]

        return c

    def grid_coordinates(self):

        attrs = self.shared_attributes

        if (
            "grid_coordinates" in attrs.keys()
            and attrs["prior_shape"] == self.shape
        ):
            return attrs["grid_coordinates"]

        shape = tuple(self.shape)

        xg, yg, zg = np.meshgrid(
            np.arange(shape[1]), np.arange(shape[0]), np.arange(shape[2])
        )

        attrs["grid_coordinates"] = (xg, yg, zg)
        attrs["prior_shape"] = self.shape

        return attrs["grid_coordinates"]

    def grid_points(self):

        attrs = self.shared_attributes

        if "grid_points" in attrs.keys() and attrs["prior_shape"] == self.shape:
            return attrs["grid_points"]

        xg, yg, _ = self.grid_coordinates()
        xg = xg[:, :, 0]
        yg = yg[:, :, 0]

        xp = self.inverse_transform_x(xg.astype(np.float32))
        yp = self.inverse_transform_y(yg.astype(np.float32))

        attrs["grid_points"] = (xp, yp)
        attrs["prior_shape"] = self.shape

        return attrs["grid_points"]

    @staticmethod
    def transform_angle(rads):
        # From radians into degrees, counterclockwise
        return -rads * (360 / (2 * np.pi))

    @staticmethod
    def get_lineType(antialiased):
        if antialiased:
            return cv2.LINE_AA
        return 8

    def show(self, delay=0):
        # Before we show we have to convert back to BGR
        dst = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)

        cv2.imshow(self.name, dst)
        cv2.waitKey(delay)

    def save(self, f_save):
        # Before we save we have to convert back to BGR
        dst = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(f_save, dst)

    def load(self, f_img):
        # Read the image in and convert to RGB space
        self._img = cv2.cvtColor(cv2.imread(f_img), cv2.COLOR_BGR2RGB)

        alpha = np.zeros_like(self._img[:, :, 0])
        self._img = np.dstack((self._img, alpha))

        return self

    @contextmanager
    def layer(self):
        canvas = self.copy(transparent=True)
        yield canvas
        self += canvas
