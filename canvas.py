import cv2
import numpy as np
import collections
from pixelhouse.color.colors import NamedColors

matplotlib_colors = NamedColors()
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
        self._img = np.zeros((height, width, 3), np.uint8)
        self.name = name
        self.extent = extent
        self.layers = collections.defaultdict(list)
        

    def __repr__(self):
        return (
            f"pixelhouse (w/h) {self.height}x{self.width}, " \
            f"extent {self.extent}"
        )

    def get_max_layer_number(self):
        if not self.layers:
            return 0
        else:
            return max(self.layers.keys())

    @property
    def height(self):
        return self._img.shape[0]

    @property
    def width(self):
        return self._img.shape[1]

    @property
    def img(self):
        self._img = np.zeros_like(self._img)

        for ln in sorted(self.layers.keys()):
            for layer in self.layers[ln]:
                func, args, blend = layer

                # Saturate or blend the images together
                if blend:
                    dst = canvas(self.width, self.height).img
                    func(dst, *args)
                    cv2.add(self._img, dst, self._img)
                else:
                    func(self._img, *args)

        return self._img

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

    def append(self, func, args, blend, layer=None, **kwargs):
        if layer is None:
            layer = self.get_max_layer_number()
            
        self.layers[layer].append( [func, args, blend] )



class canvas(BasicCanvas):
    
    def circle(self, x=0, y=0, r=1, color=_default_color,
               thickness=-1, antialiased=True, blend=True, layer=None):

        x, y = self.transform_coordinates(x, y)
        r = self.transform_length(r)
        thickness = self.transform_length(thickness)
        lineType = self.get_lineType(antialiased)
        color=self.transform_color(color)

        args = (x,y), r, color, thickness, lineType
        self.append(cv2.circle, args, blend=blend, layer=None)

    def rectangle(self, x0=0, y0=0, x1=1, y1=1, color=_default_color,
                  thickness=-1, antialiased=True, blend=True, layer=None):
        
        x0, y0 = self.transform_coordinates(x0, y0)
        x1, y1 = self.transform_coordinates(x1, y1)
        thickness = self.transform_length(thickness)
        lineType = self.get_lineType(antialiased)
        color=self.transform_color(color)
        
        args = (x0,y0), (x1, y1), color, thickness, lineType
        self.append(cv2.rectangle, args, blend=blend, layer=layer)

    def line(self, x0=0, y0=0, x1=1, y1=1, color=_default_color,
             thickness=1, antialiased=True, blend=True, layer=None):
        
        x0, y0 = self.transform_coordinates(x0, y0)
        x1, y1 = self.transform_coordinates(x1, y1)
        thickness = self.transform_length(thickness)
        lineType = self.get_lineType(antialiased)
        color=self.transform_color(color)
        
        args = (x0,y0), (x1, y1), color, thickness, lineType
        self.append(cv2.line, args, blend=blend, layer=None)
 
    def ellipse(self, x=0, y=0,
                major_length=1, minor_length=1,
                rotation=0,
                angle_start=0,
                angle_end=2*np.pi,
                color=_default_color,
                thickness=-1,
                antialiased=True,
                blend=True,
                layer=None,
    ):
        # Angles measured in radians
        
        x, y = self.transform_coordinates(x, y)
        major_length = self.transform_length(major_length)
        minor_length = self.transform_length(minor_length)
        thickness = self.transform_length(thickness)
        lineType = self.get_lineType(antialiased)
        color=self.transform_color(color)
        
        rotation_degree = self.transform_angle(rotation)
        start_degree = self.transform_angle(angle_start)
        end_degree = self.transform_angle(angle_end)
        
            
        args = ((x,y), (major_length, minor_length),
                rotation_degree, start_degree, end_degree,
                color, thickness, lineType)
        
        self.append(cv2.ellipse, args, blend=blend, layer=layer)
    
    
    def background(self, color=_default_color):
        ### This doesn't work yet!
        raise NotImplementedError


if __name__ == "__main__":
    c = canvas(200,200,extent=4)

    color = [0, 0, 255]
    c.circle(thickness=0.5,color=color)
    c.circle(thickness=0,color=color)
   
    c.show()
    
