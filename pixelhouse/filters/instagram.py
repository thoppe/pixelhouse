"""
Pseudo-instagram filters (weights derived from samples).
"""

from ..artist import Artist, constant
import numpy as np
import cv2
import glob
import os

_script_path = os.path.dirname(os.path.abspath(__file__))
_model_path = os.path.join(_script_path, "insta", "models")

known_models = set(
    [
        os.path.basename(name).split(".")[0]
        for name in glob.glob(os.path.join(_model_path, "*.npz"))
    ]
)


class instafilter(Artist):

    weight = constant(1.0)
    args = ("weight",)

    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)

        if name not in known_models:
            msg = f"Model {name} not in {known_models}"
            raise KeyError(msg)

        f_model = os.path.join(_model_path, f"{name}.npz")
        assert os.path.exists(f_model)

        obj = np.load(f_model)
        self.weights = obj["W"]
        self.bias = obj["b"]

    @staticmethod
    def _saturation_and_lightness(xBGR):
        # Returns the max BGR color and the largest delta in BGR space.
        mx, mn = xBGR.max(axis=1), xBGR.min(axis=1)
        avg = xBGR.mean(axis=1)
        return np.array([avg, mx - mn]).T

    @staticmethod
    def _scale(img):
        # Scales the colors to a flat (h*w, channel) array \in [0, 1]
        h, w, channels = img.shape
        return img.reshape(h * w, channels).astype(np.float32) / 255

    def draw(self, cvs, t=0.0):

        weight = self.weight(t)
        if weight <= 0:
            # With zero weight, skip the filter
            return None

        height, width, channels = cvs.shape

        img = cvs.img[:, :, :3]
        alpha = None

        if channels != 3:
            alpha = cvs.img[:, :, 3:]

        # Model expect BGR, canvas uses RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        xBGR = self._scale(img)
        xLS = self._saturation_and_lightness(xBGR)

        y = np.hstack([xBGR, xLS])

        # Apply MLP layers
        for w, b in zip(self.weights[:-1], self.bias[:-1]):
            y = np.tanh(y.dot(w) + b)

        # The last layer has no activation
        y = y.dot(self.weights[-1]) + self.bias[-1]

        yp = np.clip(y * 255, 0, 255).astype(np.uint8)
        imgBGR = yp[:, :3].reshape(height, width, 3)

        # Convert back to RGB colorspace
        img2 = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2RGB)

        if alpha is not None:
            img2 = np.dstack([img2, alpha])

        # With weight > 1 apply the whole filter
        if weight >= 1:
            cvs.img = img2
        # Otherwise blend
        cvs.img = cv2.addWeighted(cvs.img, 1 - weight, img2, weight, gamma=0.0)
