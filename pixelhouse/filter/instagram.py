'''
Pseudo-instagram filters (weights derived from samples).
'''

#from ..artist import Artist, constant
import numpy as np
import cv2
import glob
import os
import keras

_script_path = os.path.dirname(os.path.abspath(__file__))
_model_path = os.path.join(_script_path, 'pseudoinsta', 'models')

known_models = set([
    os.path.basename(name).split('.')[0] for name in 
    glob.glob(os.path.join(_model_path, '*.h5'))
])

class PseudoFilter(object):    

    def __init__(self, name):
        super().__init__()
        
        if name not in known_models:
            msg = f'Model {name} not in {known_models}'
            raise KeyError(msg)

        f_model = os.path.join(_model_path, f'{name}.h5')
        assert(os.path.exists(f_model))

        self.clf = keras.models.load_model(f_model)

    @staticmethod
    def _scale(img):
        h, w, channels = img.shape
        return img.reshape(h*w, channels).astype(np.float32)/255

    def __call__(self, img, t=0.0):

        xBGR = self._scale(img)
        xHSV = self._scale(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))
        xLAB = self._scale(cv2.cvtColor(img, cv2.COLOR_BGR2LAB))
        x = np.hstack([xBGR, xHSV, xLAB])
        yp = self.clf.predict(x, batch_size=2*12)

        h, w, channels = img.shape
        img_ALL = (255*np.clip(yp, 0,1)).astype(np.uint8)
        imgRGB = img_ALL[:, :3].reshape(h, w, 3)
        
        return imgRGB

if __name__ == "__main__":
    img = cv2.imread('test_img.jpg')
    
    F = PseudoFilter('Ludwig')

    print("Loaded image and model")
    img2 = F(img)
    
    cv2.imshow('image',img)
    cv2.waitKey(0)
    
    cv2.imshow('image',img2)
    cv2.waitKey(0)
