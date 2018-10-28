import os
import numpy as np
import h5py

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

x = np.random.uniform(0,1,size=(3,5))
print(x)

f_model = 'models/Crema.h5'
#import keras
#clf = keras.models.load_model(f_model)
# yp = clf.predict(x)

weights = []
bias = []

with h5py.File(f_model, 'r') as h5:
    for key in h5["model_weights"]:
        print(key)
    #print(h5.keys())
exit()


print(yp)

