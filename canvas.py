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
    
    def circle(self, x=0, y=0, r=1, color=_default_color,
               thickness=-1, antialiased=True, blend=True):

        x, y = self.transform_coordinates(x, y)
        r = self.transform_length(r)
        thickness = self.transform_length(thickness)

        if antialiased:
            lineType = cv2.LINE_AA
        else:
            lineType = 8

        args = (x,y), r, color, thickness, lineType
        self._combine(cv2.circle, args, blend=blend)


    def rectangle(self, x0=0, y0=0, x1=1, y1=1, color=_default_color,
                  thickness=-1, antialiased=True, blend=True):

        x0, y0 = self.transform_coordinates(x0, y0)
        x1, y1 = self.transform_coordinates(x1, y1)
        thickness = self.transform_length(thickness)
        
        if antialiased:
            lineType = cv2.LINE_AA
        else:
            lineType = 8
            
        args = (x0,y0), (x1, y1), color, thickness, lineType
        self._combine(cv2.rectangle, args, blend=blend)



if __name__ == "__main__":
    c = canvas(400,400,extent=4)

    c.rectangle(-1,-1,1,1,[255,0,0])
    c.rectangle(0,0,2,-2,[0,0,255])
    c.rectangle(-3,-3,0.5,0.5,[0,255,0])
    
    
    c.show()
    


