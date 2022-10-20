import streamlit as st

from tensorflow.keras.models import load_model

import autokeras as ak

import wandb
from wandb.keras import WandbCallback

PROJECT = "ml-in-prod"
model = None


if (model is None):
    wandb.init(PROJECT)

    artifact = wandb.use_artifact("securims/ml-in-prod/model_autokeras:latest", type="model")
    artifact_dir = artifact.download(root="model_autokeras")

model = load_model("model_autokeras", custom_objects=ak.CUSTOM_OBJECTS)

text = st.text_input('Predict text score')

st.write('Text ', text)

if len(text) > 0:
    st.write('Prediction ', model.predict([text])[0][0])
