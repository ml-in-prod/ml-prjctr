import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression

import numpy 

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, ReLU

# Parameters of the data-set
n_samples = 10000
n_features = 1000
n_informative = 500
noise = 3
# Create dataset and preprocess it
x, y = make_regression(n_samples=n_samples, n_features=n_features, n_informative=n_informative, noise=noise)
x = x / abs(x).max(axis=0)
y = y / abs(y).max()
x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=42)

model = tf.keras.Sequential()
model.add(Dense(1024, kernel_initializer="he_normal", input_dim=n_features))
model.add(ReLU())
model.add(Dense(1024))
model.add(ReLU())
model.add(Dense(1))

model.compile(
    loss="mse",
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001)
)

model.fit(
    x_train, 
    y_train, 
    epochs=200, 
    batch_size=1024, 
    verbose=1
)

def predict():
    return model.predict(x_val)

def test_my_stuff(benchmark):
    #for i in range(0,1000):
    res = benchmark(predict)

    assert type(res) == numpy.ndarray

