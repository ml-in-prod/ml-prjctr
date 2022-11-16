import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression

import neptune.new as neptune
from neptune.new.integrations.tensorflow_keras import NeptuneCallback


import numpy 

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, ReLU

import tensorflow_model_optimization as tfmot

run = neptune.init(project="securims/tf-keras-integration",
                   api_token="")


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

initial_sparsity = 0.0
final_sparsity = 0.75
begin_step = 1000
end_step = 5000
pruning_params = {
        'pruning_schedule': tfmot.sparsity.keras.PolynomialDecay(
            initial_sparsity=initial_sparsity,
            final_sparsity=final_sparsity,
            begin_step=begin_step,
            end_step=end_step)
    }
model = tfmot.sparsity.keras.prune_low_magnitude(model, **pruning_params)
pruning_callback = tfmot.sparsity.keras.UpdatePruningStep()

model.compile(
    loss="mse",
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001)
)


neptune_cbk = NeptuneCallback(run=run, base_namespace="metrics")
# model.fit(x_train, y_train, epochs=5, batch_size=64, callbacks=[neptune_cbk])


model.fit(
    x_train, 
    y_train, 
    epochs=200, 
    batch_size=1024, 
    callbacks= [pruning_callback, neptune_cbk], 
    verbose=1
)

def predict():
    return model.predict(x_val)