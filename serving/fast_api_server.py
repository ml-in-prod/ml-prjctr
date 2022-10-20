import json
from typing import Union
import autokeras as ak
from fastapi import FastAPI
from pydantic import BaseModel

import wandb
from tensorflow.keras.models import load_model

class Item(BaseModel):
    text: str

PROJECT = "ml-in-prod"


def download_model(PROJECT):
    wandb.init(PROJECT)

    artifact = wandb.use_artifact("securims/ml-in-prod/model_autokeras:latest", type="model")
    artifact_dir = artifact.download(root="model_autokeras")

    model = load_model("model_autokeras", custom_objects=ak.CUSTOM_OBJECTS)

    return model


app = FastAPI()
loaded_model = download_model(PROJECT)

@app.get("/")
async def server():
    return "Server started"

@app.post("/predict")
async def predict(item: Item):
    prediction = loaded_model.predict([item.text])

    return json.dumps(prediction.tolist())