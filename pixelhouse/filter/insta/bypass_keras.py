"""
Proof of concept to show how to bypass a MLP keras model with numpy only.
"""

import os
import numpy as np
import h5py


os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
n_samples = 3

x = np.random.uniform(0, 1, size=(n_samples, 5))
print("Input array")
print(x)

obj = np.load("models/Sutro.npz")
weights = obj["W"]
bias = obj["b"]

y = x.copy()
for w, b in zip(weights[:-1], bias[:-1]):
    y = np.tanh(y.dot(w) + b)

# The last layer has no activation
y_numpy = y.dot(weights[-1]) + bias[-1]

f_model = "models/Sutro.h5"
import keras

clf = keras.models.load_model(f_model)
y_keras = clf.predict(x)
print("Keras output")
print(y_keras)

print("Numpy output")
print(y_numpy)

print("Check passes?", np.isclose(y_keras, y_numpy).all())
