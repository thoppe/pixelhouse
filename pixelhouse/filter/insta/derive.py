import cv2
import os
import numpy as np

import keras
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Activation, Input, Lambda

# Source images from
# https://www.makeuseof.com/tag/instagram-filters-work-can-tell-difference/

def read_source(f_source):
    img = cv2.imread(f_source,)
    h, w, channels = img.shape

    b = (img.mean(axis=2).sum(axis=0)/h)
    pixel_n = (b>=254).sum()
    print(w, pixel_n)
    assert((w-pixel_n) % 2 == 0)

    # Split the image in half
    img0 = img[:, :w//2]
    img1 = img[:, w//2:]

    # Remove the whitespace between the images
    img0 = img0[:, :-pixel_n//2]
    img1 = img1[:,  pixel_n//2:]

    # Clip a border to help artifacts
    img0 = img0[2:-2, 2:-2]
    img1 = img1[2:-2, 2:-2]

    assert(img0.shape == img1.shape)

    return img0, img1

def scale_values(img):
    h, w, channels = img0.shape
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

    '''
    # Very simple one-layer model that take BGR+HSV and converts to new filter
    A0 = Input(shape=(9,))
    W = Dense(3)(A0)

    from keras import backend as K
    alpha = K.variable(value=0.5, dtype='float32', name='alpha')
    beta = K.variable(value=0.5, dtype='float32', name='alpha')
    
    A1 = Lambda(lambda x: x*alpha + beta)(W)
    model = Model(inputs=A0, outputs=A1)
    '''

    model.compile(optimizer='ADAM',  loss='mae')
    
    model.fit(
        x, y,
        epochs=n_epochs, batch_size=2**9,verbose=10,
        callbacks=[Histories()]
    )
    
    yp = model.predict(x)
    
    img2 = (255*np.clip(yp, 0,1)).astype(np.uint8)
    img2 = img2[:, :3].reshape(h, w, 3)
    
    return img2, W.get_weights()


#f_source = 'data/crema-e1448847288573.jpg'
f_source = 'data/nashville-e1448853218475.jpg'
#f_source = 'data/Moon-Filter.jpg'

img0, img1 = read_source(f_source)
img2, weights = train(img0, img1, 100)

save_dest_models = 'models'
os.system(f'mkdir -p {save_dest_models}')

save_dest_images = 'examples'
os.system(f'mkdir -p {save_dest_images}')

cv2.imwrite(os.path.join(save_dest_images,'0_'+os.path.basename(f_source)),img0)
cv2.imwrite(os.path.join(save_dest_images,'1_'+os.path.basename(f_source)),img1)
cv2.imwrite(os.path.join(save_dest_images,'2_'+os.path.basename(f_source)),img2)



display_img = np.concatenate((img0, img1, img2), axis=1)
cv2.imshow(f_source, display_img)
cv2.waitKey(0)



