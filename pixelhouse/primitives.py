import numpy as np
import cv2
from .artists import artist, constant


class circle(artist):
    r = constant(1.0)

    def __call__(self, cvs, t=0.0):
        x, y, thickness, color, lineType = self.basic_transforms(cvs, t)
        r = cvs.transform_length(self.r(t))
        
        args = (x,y), r, color, thickness, lineType
        cvs.cv2_draw(cv2.circle, args, blend=self.blend(t))

class rectangle(artist):
    x1 = constant(1.0)
    y1 = constant(1.0)

    def __call__(self, cvs, t=0.0):
        x, y, thickness, color, lineType = self.basic_transforms(cvs, t)
        x1 = cvs.transform_x(self.x1(t))
        y1 = cvs.transform_y(self.y1(t))

        args = (x,y), (x1, y1), color, thickness, lineType
        cvs.cv2_draw(cv2.rectangle, args, blend=self.blend(t))


class line(artist):
    x1 = constant(1.0)
    y1 = constant(1.0)
    thickness = constant(0.1)

    def __call__(self, cvs, t=0.0):
        x, y, thickness, color, lineType = self.basic_transforms(cvs, t)
        x1 = cvs.transform_x(self.x1(t))
        y1 = cvs.transform_y(self.y1(t))

        args = (x,y), (x1, y1), color, thickness, lineType
        cvs.cv2_draw(cv2.line, args, blend=self.blend(t))

class ellipse(artist):
    a = constant(2.0)
    b = constant(1.0)
    
    rotation = constant(0.0)
    angle_start = constant(0.0)
    angle_end = constant(2*np.pi)

    def __call__(self, cvs, t=0.0):
        x, y, thickness, color, lineType = self.basic_transforms(cvs, t)

        a = cvs.transform_length(self.a(t))
        b = cvs.transform_length(self.b(t))
        
        rotation = cvs.transform_angle(self.rotation(t))
        angle_start = cvs.transform_angle(self.angle_start(t))
        angle_end = cvs.transform_angle(self.angle_end(t))

        args = ((x,y), (a, b),
                rotation, angle_start, angle_end, color, thickness, lineType)

        cvs.cv2_draw(cv2.ellipse, args, blend=self.blend(t))


if __name__== "__main__":
    c = canvas.Canvas()

    circle(x=1,color='r')(c,t=0.5)
    circle(x=-1,color='b')(c)
    rectangle(x=-3,y=-3,color='g')(c)
    line(x=-3,y=-3,color='g')(c)
    ellipse(color='purple')(c)

    c.show()
