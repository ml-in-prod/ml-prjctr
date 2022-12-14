import numpy as np
import concurrent.futures
from typing import Tuple
import time
from tqdm import tqdm
from concurrent.futures import wait
import time

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import load_model

import autokeras as ak

import wandb
from wandb.keras import WandbCallback

def train_model(x_train: np.ndarray, y_train: np.ndarray) -> ak.TextRegressor:

    wandb.init(project="ml-in-prod")

    wandb.config = {
       "learning_rate": 0.001,
       "epochs": 5,
       "batch_size": 128
    }

    reg = ak.TextRegressor(overwrite=True, max_trials=1)
    # Feed the text regressor with training data.

    reg.fit(x_train, y_train, epochs=5, callbacks=[WandbCallback()])

    # Predict with the best model.

    model = reg.export_model()

    try:
        model.save("model_autokeras", save_format="tf")
    except:
        model.save("model_autokeras.h5") 
    
    art = wandb.Artifact("model_autokeras", type="model")
    art.add_dir("model_autokeras")
    wandb.log_artifact(art)

    return reg


def get_data(path: str = './test.csv') -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    train_dataset = pd.read_csv(path,
                                na_values="?", comment='\t',
                                sep=",", skipinitialspace=True)

    X = train_dataset.excerpt
    y = train_dataset.target

    train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

    train = pd.DataFrame(train_X)
    val = pd.DataFrame(train_y)
    test = pd.DataFrame(val_X)

    train.to_csv("train.csv")
    val.to_csv("val.csv")
    test.to_csv("test_val.csv")

    return np.array(train_X), np.array(train_y), np.array(val_X)


def predict(model: ak.TextRegressor, x: np.ndarray) -> np.ndarray:
    # replace with real model
    # time.sleep(0.001)
    return model.predict(x)


def run_inference(x_test: np.ndarray, path:str = "model_autokeras", batch_size: int = 64) -> np.ndarray:
    wandb.init(project="ml-in-prod")

    wandb.config = {
       "learning_rate": 0.001,
       "epochs": 5,
       "batch_size": 128
    }

    artifact = wandb.use_artifact("securims/ml-in-prod/model_autokeras:latest", type="model")
    artifact_dir = artifact.download(root=path)

    model = load_model(path, custom_objects=ak.CUSTOM_OBJECTS)

    y_pred = []
    for k in range(0, 100):
        for i in range(0, x_test.shape[0], batch_size):
            x_batch = x_test[i: i + batch_size]
            y_batch = predict(model, x_batch)
            y_pred.append(y_batch)
    return np.concatenate(y_pred)


def run_inference_process_pool(x_test: np.ndarray, path:str = "model_autokeras", max_workers: int = 16) -> np.ndarray:
    print(path)
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        chunk_size = len(x_test) // max_workers

        chunks = []
        # split in to chunks
        for i in range(0, len(x_test), chunk_size):
            chunks.append(x_test[i: i + chunk_size])

        futures = []
        # submit chunks for inference
        for chunk in chunks:
            future = executor.submit(run_inference, x_test=chunk, path=path)
            futures.append(future)

        # # wait for all futures
        wait(futures)

        y_pred = []
        for future in futures:
            y_batch = future.result()
            y_pred.append(y_batch)

    return np.concatenate(y_pred)


def main():
    x_train, y_train, x_test = get_data('./test.csv')

    train_model(x_train, y_train)

    # s = time.monotonic()
    # _ = run_inference_process_pool(x_test=x_test, max_workers=1)
    # print(f"Inference one worker {time.monotonic() - s}")

    s = time.monotonic()
    max_workers = 8
    _ = run_inference_process_pool(x_test=x_test, max_workers=max_workers)
    print(f"Inference {max_workers} workers {time.monotonic() - s}")


if __name__ == "__main__":
    main()
