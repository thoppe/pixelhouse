'''
Converts MLP keras models from compute_from_image.py to something that
is pure numpy.
'''

import os, glob
import numpy as np
import h5py

F_MODELS = glob.glob("models/*.h5")

for f in F_MODELS:
    name = os.path.basename(f).split('.h5')[0]
    f_new = os.path.join('models', name + '.npz')
    
    W, b = [], []
    
    with h5py.File(f, 'r') as h5:
        for key in h5["model_weights"]:
            g = h5['model_weights'][key][key]
            W.append(g['kernel:0'][...])
            b.append(g['bias:0'][...])

    np.savez_compressed(f_new, W=W, b=b)
    print(f_new)

