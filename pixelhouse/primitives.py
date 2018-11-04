import numpy as np
import cv2
from .artist import Artist, constant

_DEFAULT_COLOR = 'white'
_DEFAULT_THICKNESS = -1
_DEFAULT_ANTIALIASED = True
_DEFAULT_MODE = 'direct'

class PrimitiveArtist(Artist):

    # Basic attributes common to all artists
    x = constant(0.0)
    y = constant(0.0)
    color = constant(_DEFAULT_COLOR)
    thickness = constant(_DEFAULT_THICKNESS)
    antialiased = constant(_DEFAULT_ANTIALIASED)
    mode = constant(_DEFAULT_MODE)
   
    def basic_transforms(self, cvs, t):
        x = cvs.transform_x(self.x(t))
        y = cvs.transform_y(self.y(t))
        thickness = cvs.transform_thickness(self.thickness(t))
        color = cvs.transform_color(self.color(t))
        lineType = cvs.get_lineType(self.antialiased(t))

        return x, y, thickness, color, lineType



class circle(PrimitiveArtist):
    r = constant(1.0)
    args = ('x', 'y', 'r', 'color', 'thickness', 'linetype')

    def __call__(self, cvs, t=0.0):
        x, y, thickness, color, lineType = self.basic_transforms(cvs, t)
        r = cvs.transform_length(self.r(t))
        
        args = (x,y), r, color, thickness, lineType
        cvs.cv2_draw(cv2.circle, args, mode=self.mode(t))

class rectangle(PrimitiveArtist):
    x1 = constant(1.0)
    y1 = constant(1.0)
    args = ('x', 'y', 'x1', 'y1', 'color', 'thickness', 'lineType')

    def __call__(self, cvs, t=0.0):
        x, y, thickness, color, lineType = self.basic_transforms(cvs, t)
        x1 = cvs.transform_x(self.x1(t))
        y1 = cvs.transform_y(self.y1(t))

        args = (x,y), (x1, y1), color, thickness, lineType
        cvs.cv2_draw(cv2.rectangle, args, mode=self.mode(t))


class line(PrimitiveArtist):
    x1 = constant(1.0)
    y1 = constant(1.0)
    thickness = constant(0.1)
    args = ('x', 'y', 'x1', 'y1', 'color', 'thickness', 'lineType')

    def __call__(self, cvs, t=0.0):
        x, y, thickness, color, lineType = self.basic_transforms(cvs, t)
        x1 = cvs.transform_x(self.x1(t))
        y1 = cvs.transform_y(self.y1(t))

        # Thickness must be at least one pixel
        thickness = max(thickness, 1)

        args = (x,y), (x1, y1), color, thickness, lineType
        cvs.cv2_draw(cv2.line, args, mode=self.mode(t))

class ellipse(PrimitiveArtist):
    a = constant(2.0)
    b = constant(1.0)
    
    rotation = constant(0.0)
    angle_start = constant(0.0)
    angle_end = constant(2*np.pi)
    args = ('x', 'y', 'a', 'b', 'rotation',
            'angle_start', 'angle_end', 'color',
            'thickness', 'lineType')

    def __call__(self, cvs, t=0.0):
        x, y, thickness, color, lineType = self.basic_transforms(cvs, t)

        a = cvs.transform_length(self.a(t))
        b = cvs.transform_length(self.b(t))
        
        rotation = cvs.transform_angle(self.rotation(t))
        angle_start = cvs.transform_angle(self.angle_start(t))
        angle_end = cvs.transform_angle(self.angle_end(t))

        args = ((x,y), (a, b),
                rotation, angle_start, angle_end, color, thickness, lineType)

        cvs.cv2_draw(cv2.ellipse, args, mode=self.mode(t))



class polyline(PrimitiveArtist):
    xpts = constant([0.0, 1.0, 2.0])
    ypts = constant([0.0, 2.0, 0.0])
    thickness = constant(0.1)
    is_closed = constant(1)
    
    args = ('xpts', 'ypts', 'is_closed', 'color', 'thickness', 'lineType')

    def __call__(self, cvs, t=0.0):
        print (np.array(self.xpts(t)).dtype)

        xpts = cvs.transform_x(np.array(self.xpts(t)), False)
        ypts = cvs.transform_y(np.array(self.ypts(t)), False)

        thickness = cvs.transform_thickness(self.thickness(t))
        color = cvs.transform_color(self.color(t))
        lineType = cvs.get_lineType(self.antialiased(t))
        is_closed = self.is_closed(t)
        
        pts = np.vstack([xpts, ypts]).T.astype(np.int32)
        print(pts.shape, pts.dtype)
                
        args = [pts], is_closed, color, thickness, lineType
        cvs.cv2_draw(cv2.polylines, args, mode=self.mode(t))
