import cv2
from tqdm import tqdm
import os
import numpy as np
import json
import pandas as pd

import keras
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Input, Lambda

save_dest_models = 'models'
os.system(f'mkdir -p {save_dest_models}')

save_dest_images = 'examples'
os.system(f'mkdir -p {save_dest_images}')


def scale_values(img):
    h, w, channels = img.shape
    return img.reshape(h*w, channels).astype(np.float32)/255


def train(img0, img1, n_epochs=40):
        
    # Printing log

    class Histories(keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs={}):
            print(logs)

    h, w, channels = img0.shape
    xBGR = scale_values(img0)
    xHSV = scale_values(cv2.cvtColor(img0, cv2.COLOR_BGR2HSV))
    xLAB = scale_values(cv2.cvtColor(img0, cv2.COLOR_BGR2LAB))
    #xYCrCb = scale_values(cv2.cvtColor(img0, cv2.COLOR_BGR2YCrCb))
    
    yBGR = scale_values(img1)
    yHSV = scale_values(cv2.cvtColor(img1, cv2.COLOR_BGR2HSV))
    yLAB = scale_values(cv2.cvtColor(img1, cv2.COLOR_BGR2LAB))
    
    x = np.hstack([xBGR, xHSV, xLAB])
    y = np.hstack([yBGR, yHSV, yLAB])

    W = Dense(9, input_shape=(9,))
    model = Sequential([W,])

    model.compile(optimizer='ADAM',  loss='mae')
    
    history = model.fit(
        x, y,
        epochs=n_epochs, batch_size=2**9,verbose=10,
        callbacks=[Histories()]
    )

    loss = history.history['loss']
    
    yp = model.predict(x)
    
    img2 = (255*np.clip(yp, 0,1)).astype(np.uint8)
    img2 = img2[:, :3].reshape(h, w, 3)
    
    return img2, W.get_weights(), loss

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def train_from_target(f_target, n_epochs):
    
    f_json = os.path.join(save_dest_models, name + '.json')
    f_source = 'samples/Normal.jpg'

    img0 = cv2.imread(f_source)
    img1 = cv2.imread(f_target)

    img2, weights, loss = train(img0, img1, n_epochs)

    W, b = weights
    name = os.path.basename(f_target).replace('.jpg', '')
    print(1)
    js = {
        "W": json.loads(json.dumps(W, cls=NumpyEncoder)),
        "b": json.loads(json.dumps(b, cls=NumpyEncoder)),
        "name" : name,
        "color_order" : "BGR HSV LAB",
        "loss" : loss,
    }
    print(js)

    with open(f_json, 'w') as FOUT:
        FOUT.write(json.dumps(js, indent=2))

    f0 = os.path.join(save_dest_images, name + '_0.jpg')
    cv2.imwrite(f0,img0)

    f1 = os.path.join(save_dest_images, name + '_1.jpg')
    cv2.imwrite(f1,img1)

    #display_img = np.concatenate((img0, img1, img2), axis=1)
    #cv2.imshow(f_source, display_img)
    #cv2.waitKey(0)

if __name__ == "__main__":
    
    f_target = 'samples/Charmes.jpg'
    train_from_target(f_target, 1)
