import pandas as pd
import feast
from joblib import load
import json

import tensorflow as tf

import wandb
import numpy as np
from pydantic import BaseModel

from fastapi import FastAPI

class DriverData(BaseModel):
    driver_id: str
    trip_completed: int


class DriverModel:
    def __init__(self):
        wandb.init(project="feature-store")

        artifact = wandb.use_artifact(
             "securims/feature-store/tf_model:latest", type="model")

        artifact.download(root='tf_model')

        self.model = tf.keras.models.load_model('tf_model')

        self.fs = feast.FeatureStore(repo_path="feature_repo/")

    def predict(self, driver_id, trip_completed):
        driver_features = self.fs.get_online_features(
            entity_rows=[{"driver_id": driver_id}],
            features=[
                "driver_hourly_stats:conv_rate",
                "driver_hourly_stats:acc_rate",
            ],
        )
        driver_features_dict = driver_features.to_dict()
        driver_features_dict["trip_completed"] = trip_completed

        df = pd.DataFrame.from_dict(driver_features_dict)

        df["score"] = self.model.predict(df.to_numpy())
        
        return df["score"][0]

model = DriverModel()
app = FastAPI()

@app.get("/")
def health_check() -> str:
    return "server is running"


@app.post("/predict-driver-score")
def predict_score(payload: DriverData) -> json:
    prediction = model.predict(driver_id=payload.driver_id, trip_completed=payload.trip_completed)
    
    print(prediction)
    return json.dumps({"score": float(prediction)})
