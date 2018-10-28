'''
Pseudo-instagram filters (weights derived from samples).
'''

#from ..artist import Artist, constant
import numpy as np
import cv2
import glob
import os

_script_path = os.path.dirname(os.path.abspath(__file__))
_model_path = os.path.join(_script_path, 'insta', 'models')

known_models = set([
    os.path.basename(name).split('.')[0] for name in 
    glob.glob(os.path.join(_model_path, '*.npz'))
])

class PseudoFilter(object):    

    def __init__(self, name):
        super().__init__()
        
        if name not in known_models:
            msg = f'Model {name} not in {known_models}'
            raise KeyError(msg)

        f_model = os.path.join(_model_path, f'{name}.npz')
        assert(os.path.exists(f_model))

        obj = np.load(f_model)
        self.weights = obj['W']
        self.bias = obj['b']

    @staticmethod
    def _saturation_and_lightness(xBGR):
        # Returns the max BGR color and the largest delta in BGR space.
        mx, mn = xBGR.max(axis=1), xBGR.min(axis=1)
        avg = xBGR.mean(axis=1)
        return np.array([avg, mx-mn]).T

    @staticmethod
    def _scale(img):
        # Scales the colors to a flat (h*w, channel) array \in [0, 1]
        h, w, channels = img.shape
        return img.reshape(h*w, channels).astype(np.float32)/255

    def __call__(self, img, t=0.0):
        height, width, channels = img.shape
        assert(channels==3)
        
        xBGR = self._scale(img)
        xLS = self._saturation_and_lightness(xBGR)
        
        y = np.hstack([xBGR, xLS])

        # Apply MLP layers
        for w, b in zip(self.weights[:-1], self.bias[:-1]):
            y = np.tanh(y.dot(w) + b)

        # The last layer has no activation
        y = y.dot(self.weights[-1]) + self.bias[-1]

        yp = np.clip(y*255, 0, 255).astype(np.uint8)
        imgBGR = yp[:, :3].reshape(height, width, 3)

        return imgBGR

if __name__ == "__main__":
    img = cv2.imread('insta/samples/Normal.jpg')
    
    print("Loading image and model")
    F = PseudoFilter('Ludwig')

    print("Applying sampling")
    img2 = F(img)
    
    cv2.imshow('image',img)
    cv2.waitKey(0)
    
    cv2.imshow('image',img2)
    cv2.waitKey(0)
