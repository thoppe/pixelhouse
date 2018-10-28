import os
import numpy as np
import h5py

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

x = np.random.uniform(0,1,size=(3,5))
print(x)

obj = np.load('models/Sutro.npz')
weights = obj['W']
bias = obj['b']
for w, b in zip(weights[:-1], bias[:-1]):
    print(w.shape)
exit()

print(len(weights))
exit()
y = x.copy()
for w, b in zip(weights[:-1], bias[:-1]):
    print(y.shape)
    y = np.tanh(y.dot(w) + b)
print(y)


#f_model = 'models/Sutro.h5'
#import keras
#clf = keras.models.load_model(f_model)
#yp = clf.predict(x)
#print(yp)

