import cv2
import numpy as np
from src.color.colors import NamedColors

matplotlib_colors = NamedColors()
#_default_color = [255, 255, 255]
_default_color = 'white'

class BasicCanvas():
    '''
    Basic canvas object for quad drawings. 
    Extent measures along the x-axis.
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
        
        return (int(x), int(y))

    def transform_length(self, r):
        r *= (self.width/self.extent)
        return int(r)

    def transform_color(self, c):
        if isinstance(c, str):
            return matplotlib_colors(c)
        return c

    def transform_angle(self, rads):
        # From radians into degrees, counterclockwise
        return -rads*(360/(2*np.pi))

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

    def _combine(self, func, args, blend, **kwargs):
        # Saturate or blend the images together

        if blend:
            dst = canvas(self.width, self.height).img
            func(dst, *args)
            cv2.add(self.img, dst, self.img)
        else:
            func(self.img, *args)


class canvas(BasicCanvas):

    @staticmethod
    def get_lineType(antialiased):
        if antialiased:
            return cv2.LINE_AA
        return 8
    
    def circle(self, x=0, y=0, r=1, color=_default_color,
               thickness=-1, antialiased=True, blend=True):

        x, y = self.transform_coordinates(x, y)
        r = self.transform_length(r)
        thickness = self.transform_length(thickness)
        lineType = self.get_lineType(antialiased)
        color=self.transform_color(color)

        args = (x,y), r, color, thickness, lineType
        self._combine(cv2.circle, args, blend=blend)

    def rectangle(self, x0=0, y0=0, x1=1, y1=1, color=_default_color,
                  thickness=-1, antialiased=True, blend=True):
        
        x0, y0 = self.transform_coordinates(x0, y0)
        x1, y1 = self.transform_coordinates(x1, y1)
        thickness = self.transform_length(thickness)
        lineType = self.get_lineType(antialiased)
        color=self.transform_color(color)
        
        args = (x0,y0), (x1, y1), color, thickness, lineType
        self._combine(cv2.rectangle, args, blend=blend)

    def line(self, x0=0, y0=0, x1=1, y1=1, color=_default_color,
             thickness=1, antialiased=True, blend=True):
        
        x0, y0 = self.transform_coordinates(x0, y0)
        x1, y1 = self.transform_coordinates(x1, y1)
        thickness = self.transform_length(thickness)
        lineType = self.get_lineType(antialiased)
        color=self.transform_color(color)
        
        args = (x0,y0), (x1, y1), color, thickness, lineType
        self._combine(cv2.line, args, blend=blend)

    
    def background(self, color=_default_color):
        ### This doesn't work yet!
        raise NotImplementedError
 
    def ellipse(self, x=0, y=0,
                major_length=1, minor_length=1,
                rotation=0,
                line_start=0,
                line_end=2*np.pi,
                color=_default_color,
                thickness=-1,
                antialiased=True,
                blend=True
    ):
        # Angles measured in radians
        
        x, y = self.transform_coordinates(x, y)
        major_length = self.transform_length(major_length)
        minor_length = self.transform_length(minor_length)
        thickness = self.transform_length(thickness)
        lineType = self.get_lineType(antialiased)
        color=self.transform_color(color)
        
        rotation_degree = self.transform_angle(rotation)
        start_degree = self.transform_angle(line_start)
        end_degree = self.transform_angle(line_end)
        
            
        args = ((x,y), (major_length, minor_length),
                rotation_degree, start_degree, end_degree,
                color, thickness, lineType)
        
        self._combine(cv2.ellipse, args, blend=blend)


if __name__ == "__main__":
    c = canvas(200,200,extent=4)

    color = [0, 0, 255]
    c.line(-4, 0, 4, 0, thickness=0.025,color=color)


   
    c.show()
    


