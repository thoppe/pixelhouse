import cv2
import numpy as np

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

    def transform_angle(self, rads):
        # From radians into degrees, counterclockwise
        return -rads*(360/(2*np.pi))

    def show(self, delay=0):
        cv2.imshow(self.name, self.img)
        cv2.waitKey(delay)

    def save(self, f_save):
        cv2.imwrite(f_save, self.img)

    def _combine(self, func, args, blend, **kwargs):
        # Saturate or blend the images together

        if blend:
            dst = canvas(self.width, self.height).img
            func(dst, *args)
            cv2.add(self.img, dst, self.img)
        else:
            func(self.img, *args)


_default_color = [255, 255, 255]

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

        args = (x,y), r, color, thickness, lineType
        self._combine(cv2.circle, args, blend=blend)

    def rectangle(self, x0=0, y0=0, x1=1, y1=1, color=_default_color,
                  thickness=-1, antialiased=True, blend=True):
        
        x0, y0 = self.transform_coordinates(x0, y0)
        x1, y1 = self.transform_coordinates(x1, y1)
        thickness = self.transform_length(thickness)
        lineType = self.get_lineType(antialiased)
            
        args = (x0,y0), (x1, y1), color, thickness, lineType
        self._combine(cv2.rectangle, args, blend=blend)

    def line(self, x0=0, y0=0, x1=1, y1=1, color=_default_color,
             thickness=1, antialiased=True, blend=True):
        
        x0, y0 = self.transform_coordinates(x0, y0)
        x1, y1 = self.transform_coordinates(x1, y1)
        thickness = self.transform_length(thickness)
        lineType = self.get_lineType(antialiased)
            
        args = (x0,y0), (x1, y1), color, thickness, lineType
        self._combine(cv2.line, args, blend=blend)

    
    def background(self, color=_default_color):
        ### This doesn't work yet!
        raise NotImplementedError
        
        x = self.extent
        cx = canvas(self.width, self.height, self.extent)
        cx.rectangle(-x,-x, x, x, color=color, blend=True)
        cx = cx.img

        img2gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        # Now black-out the area of logo in ROI
        img1_bg = cv2.bitwise_and(self.img, self.img, mask = mask_inv)

        # Take only region of logo from logo image.
        #img2_fg = cv2.bitwise_and(self.img,self.img, mask = mask)
        
        #self.img = cv2.addWeighted(self.img, 1.0, cx.img, 1.0, 0.0)
        #self.img = img1_bg

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

        rotation_degree = self.transform_angle(rotation)
        start_degree = self.transform_angle(line_start)
        end_degree = self.transform_angle(line_end)
        
            
        args = ((x,y), (major_length, minor_length),
                rotation_degree, start_degree, end_degree,
                color, thickness, lineType)
        
        self._combine(cv2.ellipse, args, blend=blend)


if __name__ == "__main__":
    c = canvas(200,200,extent=4)

    c.line(-4, 0, 4, 0, thickness=0.025)
    c.background([45,]*3)

   
    c.show()
    


