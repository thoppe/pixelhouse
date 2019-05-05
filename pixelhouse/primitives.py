import numpy as np
import cv2
import os
from PIL import Image, ImageDraw, ImageFont
from .artist import Artist, constant

_script_path = os.path.dirname(os.path.realpath(__file__))

_DEFAULT_COLOR = "white"
_DEFAULT_SECONDARY_COLOR = "black"
_DEFAULT_THICKNESS = -1
_DEFAULT_ANTIALIASED = True
_DEFAULT_MODE = "direct"
_DEFAULT_FONT_SIZE = 1.0
_DEFAULT_FONT = os.path.join(
    _script_path, "fonts", "Alien-Encounters-Regular.ttf"
)


class PrimitiveArtist(Artist):

    # Basic attributes common to all artists
    x = constant(0.0)
    y = constant(0.0)
    color = constant(_DEFAULT_COLOR)
    thickness = constant(_DEFAULT_THICKNESS)
    antialiased = constant(_DEFAULT_ANTIALIASED)
    mode = constant(_DEFAULT_MODE)
    gradient = constant(None)

    def basic_transforms(self, cvs, t, use_shift=True):
        x = cvs.transform_x(self.x(t), use_shift=use_shift)
        y = cvs.transform_y(self.y(t), use_shift=use_shift)
        thickness = cvs.transform_thickness(self.thickness(t))
        color = cvs.transform_color(self.color(t))
        lineType = cvs.get_lineType(self.antialiased(t))
        mode = self.mode(t)

        # There is a gradient, adjust the mode
        if self.gradient(t) is not None:
            mode = "gradient"

        return x, y, thickness, color, lineType, mode


class circle(PrimitiveArtist):
    """
    Draws a circle to the canvas. Arguments can be a constant 
    or a function that returns a value from t=[0...1].
        
    Args:
    x (float): x coordinate of the circle center
    y (float): y coordinate of the circle center
    r (float): Circle radius

    color (tuple or string): Color (ignored if gradient used)
    thickness (float): Line thickness (use -1 for filled)
    antialiased (bool): Antialiased edges
    gradient (linear_gradient): pixelhouse.gradient for coloring
    mode (string): Direct, blend, add, or subtract
    """

    r = constant(2.0)
    args = ("x", "y", "r", "color", "thickness", "lineType")

    def draw(self, cvs, t=0.0):

        x, y, thickness, color, lineType, mode = self.basic_transforms(cvs, t)
        r = cvs.transform_length(self.r(t), use_shift=True)

        # Require the radius to be non-negative
        r = max(0, r)

        args = (x, y), r, color, thickness, lineType, cvs.shift
        cvs.cv2_draw(cv2.circle, args, mode=mode, gradient=self.gradient, t=t)


class rectangle(PrimitiveArtist):
    """
    Draws a rectangle to the canvas. Arguments can be a constant 
    or a function that returns a value from t=[0...1].
        
    Args:
    x (float): x coordinate of the upper left rectangle
    y (float): y coordinate of the upper left rectangle
    x1 (float): x coordinate of the lower right rectangle
    y1 (float): y coordinate of the lower right rectangle

    color (tuple or string): Color (ignored if gradient used)
    thickness (float): Line thickness (use -1 for filled)
    antialiased (bool): Antialiased edges
    gradient (linear_gradient): pixelhouse.gradient for coloring
    mode (string): Direct, blend, add, or subtract
    """

    x1 = constant(1.0)
    y1 = constant(1.0)
    args = ("x", "y", "x1", "y1", "color", "thickness", "lineType")

    def draw(self, cvs, t=0.0):
        x, y, thickness, color, lineType, mode = self.basic_transforms(cvs, t)
        x1 = cvs.transform_x(self.x1(t), use_shift=True)
        y1 = cvs.transform_y(self.y1(t), use_shift=True)

        args = (x, y), (x1, y1), color, thickness, lineType, cvs.shift
        cvs.cv2_draw(
            cv2.rectangle, args, mode=mode, gradient=self.gradient, t=t
        )


class line(PrimitiveArtist):
    """
    Draws a line to the canvas. Arguments can be a constant 
    or a function that returns a value from t=[0...1].
        
    Args:
    x (float): x coordinate of the upper left point
    y (float): y coordinate of the upper left point
    x1 (float): x coordinate of the lower right point
    y1 (float): y coordinate of the lower right point

    color (tuple or string): Color (ignored if gradient used)
    thickness (float): Line thickness 
    antialiased (bool): Antialiased edges
    gradient (linear_gradient): pixelhouse.gradient for coloring
    mode (string): Direct, blend, add, or subtract
    """

    x1 = constant(1.0)
    y1 = constant(1.0)
    thickness = constant(0.2)
    args = ("x", "y", "x1", "y1", "color", "thickness", "lineType")

    def draw(self, cvs, t=0.0):
        x, y, thickness, color, lineType, mode = self.basic_transforms(cvs, t)
        x1 = cvs.transform_x(self.x1(t), use_shift=True)
        y1 = cvs.transform_y(self.y1(t), use_shift=True)

        # Thickness must be at least one pixel
        thickness = max(thickness, 1)

        args = (x, y), (x1, y1), color, thickness, lineType, cvs.shift
        cvs.cv2_draw(cv2.line, args, mode=mode, gradient=self.gradient, t=t)


class ellipse(PrimitiveArtist):
    """
    Draws an ellipse to the canvas. Arguments can be a constant 
    or a function that returns a value from t=[0...1].
        
    Args:
    x (float): x coordinate of the upper left point
    y (float): y coordinate of the upper left point
    a (float): major axis length 
    b (float): minor axis length
    rotation (float): rotation about the center in radians
    angle_start (float): sector angle to start drawing in radians
    angle_end (float): sector angle to stop drawing in radians

    color (tuple or string): Color (ignored if gradient used)
    thickness (float): Line thickness (use -1 for filled)
    antialiased (bool): Antialiased edges
    gradient (linear_gradient): pixelhouse.gradient for coloring
    mode (string): Direct, blend, add, or subtract
    """

    a = constant(2.0)
    b = constant(1.0)

    rotation = constant(0.0)
    angle_start = constant(0.0)
    angle_end = constant(2 * np.pi)
    args = (
        "x",
        "y",
        "a",
        "b",
        "rotation",
        "angle_start",
        "angle_end",
        "color",
        "thickness",
        "lineType",
    )

    def draw(self, cvs, t=0.0):
        x, y, thickness, color, lineType, mode = self.basic_transforms(cvs, t)

        a = cvs.transform_length(self.a(t), use_shift=True)
        b = cvs.transform_length(self.b(t), use_shift=True)

        rotation = cvs.transform_angle(self.rotation(t))
        angle_start = cvs.transform_angle(self.angle_start(t))
        angle_end = cvs.transform_angle(self.angle_end(t))

        args = (
            (x, y),
            (a, b),
            rotation,
            angle_start,
            angle_end,
            color,
            thickness,
            lineType,
            cvs.shift,
        )

        cvs.cv2_draw(cv2.ellipse, args, mode=mode, gradient=self.gradient, t=t)


class polyline(PrimitiveArtist):
    """
    Draws multiple line segments to the canvas. Arguments can be a constant 
    or a function that returns a value from t=[0...1].
        
    Args:
    xpts (array): x coordinates of the line
    ypts (array): y coordinates of the line
    is_closed(bool): draw the final line segment
    is_filled(bool): fill the polygon with (cv2.fillpoly)

    color (tuple or string): Color (ignored if gradient used)
    thickness (float): Line thickness 
    antialiased (bool): Antialiased edges
    gradient (linear_gradient): pixelhouse.gradient for coloring
    mode (string): Direct, blend, add, or subtract
    """

    xpts = constant([0.0, 1.0, 2.0])
    ypts = constant([0.0, 2.0, 0.0])
    thickness = constant(0.2)
    is_closed = constant(1)
    is_filled = constant(0)

    args = (
        "xpts",
        "ypts",
        "is_closed",
        "color",
        "thickness",
        "lineType",
        "is_filled",
    )

    def draw(self, cvs, t=0.0):

        xpts = cvs.transform_x(np.array(self.xpts(t)), False)
        ypts = cvs.transform_y(np.array(self.ypts(t)), False)

        thickness = cvs.transform_thickness(self.thickness(t))
        color = cvs.transform_color(self.color(t))
        lineType = cvs.get_lineType(self.antialiased(t))
        is_closed = self.is_closed(t)
        mode = self.mode(t)

        pts = np.vstack([xpts, ypts]).T.astype(np.int32)

        if self.gradient(t) is not None:
            raise NotImplementedError("Can't use gradients on polylines yet")

        if not self.is_filled(t):
            args = [pts], is_closed, color, thickness, lineType, 0
            cvs.cv2_draw(cv2.polylines, args, mode=mode)

        args = [pts], color, lineType, 0
        cvs.cv2_draw(cv2.fillPoly, args, mode=mode)


class text(PrimitiveArtist):
    """
    Writes text the canvas. Arguments can be a constant 
    or a function that returns a value from t=[0...1].
        
    Args:
    text (string): Words to draw
    font_size (float): Size of the font (BUG: unknown how this scales)
    font (string): path to font file
    vpos (string): (upper/center/lower) vertical orientation
    hpos (string): (left/center/right) horizontal orientation

    color (tuple or string): Color (ignored if gradient used)
    thickness (float): Line thickness 
    antialiased (bool): Antialiased edges
    gradient (linear_gradient): pixelhouse.gradient for coloring
    mode (string): Direct, blend, add, or subtract
    """

    text = constant("pixelhouse")
    font = constant(_DEFAULT_FONT)
    font_size = constant(_DEFAULT_FONT_SIZE)

    vpos = constant("center")
    hpos = constant("center")

    args = ("text", "font_size", "vpos", "hpos", "font", "color")

    def draw(self, cvs, t=0.0):
        """
        Use PIL to measure and draw the font.
        """
        x, y, thickness, color, lineType, mode = self.basic_transforms(
            cvs, t, use_shift=False
        )

        text = self.text(t)
        fs = cvs.transform_length(self.font_size(t))
        f_font = self.font(t)

        if not os.path.exists(f_font):
            raise FileNotFoundError(f"Missing font {f_font}")

        font = ImageFont.truetype(self.font(t), fs)

        # Measure the font
        tw, th = font.getsize(text)

        vpos = self.vpos(t)
        if vpos == "upper":
            y -= th
        elif vpos == "center":
            y -= th // 2
        elif vpos == "lower":
            pass
        else:
            possible = ["upper", "center", "lower"]
            raise ValueError(
                f"Unknown font vertical position {vpos}, "
                f"must be one of {possible}."
            )

        hpos = self.hpos(t)
        if hpos == "left":
            pass
        elif hpos == "center":
            x -= tw // 2
        elif hpos == "right":
            x -= tw
        else:
            possible = ["left", "center", "right"]
            raise ValueError(
                f"Unknown font vertical position {hpos}, "
                f"must be one of {possible}."
            )

        # If there is no gradient, just draw it
        if not self.gradient(t):
            pil = Image.fromarray(cvs.copy().img)

            # Draw the text onto the text canvas
            draw = ImageDraw.Draw(pil)

            draw.text((x, y), text, tuple(color), font)
            cvs.img = np.array(pil)
            return True

        cvs2 = cvs.blank()
        pil = Image.fromarray(cvs2.img)
        draw = ImageDraw.Draw(pil)

        draw.text((x, y), text, (255, 255, 255, 255), font)
        cvs2.img = np.array(pil)

        self.gradient(cvs, t, mask=cvs2)
