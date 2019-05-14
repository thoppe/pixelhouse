from contextlib import contextmanager
import cv2
import os
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
        self.img = np.zeros((height, width, channels), np.uint8)
        self.shift = shift

        # Assign the background color, but make sure it is fully transparent
        # needed for antialiased edges
        self.bg = bg
        bg = np.array(self.transform_color(bg)).astype(np.uint8)
        bg[3] = 0
        self.img[:, :] = bg

        self.name = name
        self.extent = extent

        self.pixels_per_unit = width / (2 * self.extent)

        # When animating, we may want to pass attributes from one canvas
        # to another. Do so in the shared_attributes
        self.shared_attributes = {}

    def __repr__(self):
        return (
            f"Canvas (w/h) {self.height}x{self.width}, " f"extent {self.extent}"
        )

    @property
    def height(self):
        return self.img.shape[0]

    @property
    def width(self):
        return self.img.shape[1]

    @property
    def channels(self):
        return self.img.shape[2]

    @property
    def aspect_ratio(self):
        return self.width / float(self.height)

    @property
    def xmin(self):
        return self.inverse_transform_x(0)

    @property
    def xmax(self):
        return self.inverse_transform_x(self.width)

    @property
    def ymin(self):
        return self.inverse_transform_y(0)

    @property
    def ymax(self):
        return self.inverse_transform_y(self.height)

    @property
    def shape(self):
        return self.height, self.width, self.channels

    @property
    def alpha(self):
        """
        Return the alpha channel from the image
        """
        return self.img[:, :, 3]

    @alpha.setter
    def alpha(self, value):
        """
        Set the alpha channel for the image, 
        either as a fixed value or an array.
        """
        self.img[:, :, 3] = value

    def blank(self, bg=None):
        """
            Return an empty canvas of the same size.
            Does not modify in place.
        """
        if bg is None:
            bg = self.bg

        cvs = Canvas(self.width, self.height, bg=bg)
        cvs.pixels_per_unit = self.pixels_per_unit

        return cvs

    def copy(self, bg=None, transparent=False):
        """
            Returns a deep copy of this canvas
        """
        cvs = self.blank()
        cvs.img = self.img.copy()

        if transparent:
            cvs.img[:, :, 3] = 0

        return cvs

    def __call__(self, art=None):
        """
            Calls an Artist on the canvas.
            Example: canvas(translate(x=2, y=1))
        """
        if art is not None:
            art.draw(self)
        return self

    def __getitem__(self, key):
        return self.img[key]

    def __setitem__(self, key, val):
        self.img[key] = val

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
            cv2.add(self.img, rhs.img, self.img)
        elif mode == "subtract":
            cv2.subtract(self.img, rhs.img, self.img)
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
            func(self.img, *args)
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

        MX = (1 - a) * self.img + a * rhs.img
        MX = np.clip(MX, 0, 255).astype(np.uint8)
        self.img = MX

    def transform_x(self, x, is_discrete=True, use_shift=False):
        x += self.extent
        x *= self.pixels_per_unit

        if is_discrete:
            if use_shift and self.shift:
                x *= 2 ** self.shift
            return int(x)

        return x

    def inverse_transform_x(self, x):
        x /= self.pixels_per_unit
        x -= self.extent
        return x

    def transform_length(self, r, is_discrete=True, use_shift=False):
        r *= float(self.width) / self.extent / 2

        if use_shift and self.shift:
            r *= 2 ** self.shift

        if is_discrete:
            return int(r)
        return r

    def transform_y(self, y, is_discrete=True, use_shift=False):
        y *= -1
        y += self.extent / self.aspect_ratio
        y *= self.pixels_per_unit

        if is_discrete:
            if use_shift and self.shift:
                y *= 2 ** self.shift
            return int(y)

        return y

    def inverse_transform_y(self, y):
        y /= self.pixels_per_unit
        y -= self.extent / self.aspect_ratio
        y *= -1
        return y

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

    def show(self, delay=0):  # pragma: no cover

        """ 
        Opens a preview window displaying the image. 
        Returns the keycode of the button pressed.
        """

        # Before we show we have to convert back to BGR
        dst = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)

        cv2.imshow(self.name, dst)
        cv2.moveWindow(self.name, 40, 40)

        return cv2.waitKey(delay)

    def save(self, filename):

        """ Writes the canvas out to the specified filename
        """

        # Before we save we have to convert back to BGR
        dst = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(filename, dst)

    def load(self, filename):

        """ Reads an image in from a specified filename
            and converts it to RGB space
        """

        if not os.path.exists(filename):
            raise FileNotFoundError(f'"{filename}" not found')

        # Read the image in and convert to RGB space
        img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

        # If needed, add in an alpha channel
        if img.shape[2] == 3:
            alpha = np.zeros_like(img[:, :, 0])
            img = np.dstack((img, alpha))

        self.img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)

        # Set the pixels_per_unit
        self.pixels_per_unit = self.width / (2 * self.extent)

        return self

    @contextmanager
    def layer(self):
        canvas = self.copy(transparent=True)
        yield canvas
        self += canvas

    def resize(self, fx=0, fy=0, output_size=None):
        """
        Resizes the canvas either by a set scale or direct pixel amount
        """

        if output_size and (fx or fy):
            raise ValueError("Can't set both fx,fy and output_size")

        if output_size:
            self.img = cv2.resize(self.img, output_size)
        else:
            if not fy:
                fy = fx
            self.img = cv2.resize(self.img, (0, 0), fx=float(fx), fy=float(fy))

        return self


def hstack(canvas_list):
    """
    Stacks the images from two or more canvas horizontally,
    uses the extent and background color from the first canvas on the list.
    """
    cvs = canvas_list[0].blank()
    cvs.img = np.hstack([x.img for x in canvas_list])
    return cvs


def vstack(canvas_list):
    """
    Stacks the images from two or more canvas vertically,
    uses the extent and background color from the first canvas on the list.
    """
    cvs = canvas_list[0].blank()
    cvs.img = np.vstack([x.img for x in canvas_list])
    return cvs


def gridstack(canvas_grid):
    """
    Stacks the an array of arrays of canvas into a grid.
    Uses the extent and background color from the first canvas on the list.
    """
    cvs = canvas_grid[0][0].blank()
    rows = [hstack([x for x in row]) for row in canvas_grid]
    return vstack(rows)


def load(filename):
    """
    Helper function to load an image directly. 
    pixelhouse.load(filename) returns a preloaded canvas.
    """
    return Canvas().load(filename)
