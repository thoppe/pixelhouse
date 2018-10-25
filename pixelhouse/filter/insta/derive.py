import cv2
import os
import glob
import numpy as np
import json
import pandas as pd
from tqdm import tqdm 

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
    colorspace = 9
    inner_layers = 2

    layers = [Dense(9**2, input_shape=(colorspace,), activation='tanh')]
    for n in range(inner_layers):
        layers.append(Dense(9**2, activation='tanh'))

    layers.append(Dense(colorspace, activation=None))
    model = Sequential(layers)

    model.compile(optimizer='ADAM',  loss='mae')
    
    history = model.fit(
        x, y,
        epochs=n_epochs, batch_size=2**9,verbose=10,
        callbacks=[Histories()]
    )

    loss = history.history['loss']
    
    yp = model.predict(x, batch_size=2*12)
    
    img_ALL = (255*np.clip(yp, 0,1)).astype(np.uint8)
    imgRGB = img_ALL[:, :3].reshape(h, w, 3)
    imgHSV = img_ALL[:, 3:6].reshape(h, w, 3)
    imgLAB = img_ALL[:, 6:9].reshape(h, w, 3)

    # Convert these colorspaces back to BGR for saving
    imgHSV = cv2.cvtColor(imgHSV, cv2.COLOR_HSV2BGR)
    imgLAB = cv2.cvtColor(imgLAB, cv2.COLOR_LAB2BGR)
    
        
    return model, imgRGB, imgHSV, imgLAB

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def train_from_target(f_target, n_epochs):

    name = os.path.basename(f_target).replace('.jpg', '')
    f_save = os.path.join(save_dest_models, name + '.h5')
    f_source = 'samples/Normal.jpg'

    img0 = cv2.imread(f_source)
    img1 = cv2.imread(f_target)

    model, imgRGB, imgHSV, imgLAB = train(img0, img1, n_epochs)

    '''
    W, b = weights

    js = {
        "W": json.loads(json.dumps(W, cls=NumpyEncoder)),
        "b": json.loads(json.dumps(b, cls=NumpyEncoder)),
        "name" : name,
        "color_order" : "BGR HSV LAB",
        "loss" : loss,
        "n_epochs" : n_epochs,
    }

    with open(f_json, 'w') as FOUT:
        FOUT.write(json.dumps(js, indent=2))
    '''
    model.save(f_save)

    f0 = os.path.join(save_dest_images, name + '_0.jpg')
    cv2.imwrite(f0,img1)

    f1 = os.path.join(save_dest_images, name + '_1_RGB.jpg')
    cv2.imwrite(f1,imgRGB)

    f1 = os.path.join(save_dest_images, name + '_1_HSV.jpg')
    cv2.imwrite(f1,imgHSV)

    f1 = os.path.join(save_dest_images, name + '_1_LAB.jpg')
    cv2.imwrite(f1,imgLAB)
    

if __name__ == "__main__":
    
    TARGETS = glob.glob('samples/*')
    for f_target in tqdm(TARGETS):
        if "Normal" in f_target:
            continue

        name = os.path.basename(f_target).replace('.jpg', '')
        f_save = os.path.join(save_dest_models, name + '.h5')
        
        if os.path.exists(f_save):
            continue

        print(f"Starting {name}")
        train_from_target(f_target, 40)
