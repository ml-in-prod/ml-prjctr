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


def train_model(x_train: np.ndarray, y_train: np.ndarray) -> ak.TextRegressor:
    reg = ak.TextRegressor(overwrite=True, max_trials=1)
    # Feed the text regressor with training data.
    reg.fit(x_train, y_train, epochs=2)
    # Predict with the best model.

    model = reg.export_model()

    try:
        model.save("model_autokeras", save_format="tf")
    except Exception:
        model.save("model_autokeras.h5")

    return reg


def get_data(path: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    train_dataset = pd.read_csv(path,
                                na_values="?", comment='\t',
                                sep=",", skipinitialspace=True)

    X = train_dataset.excerpt
    y = train_dataset.target

    train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

    return np.array(train_X), np.array(train_y), np.array(val_X)


def predict(model: ak.TextRegressor, x: np.ndarray) -> np.ndarray:
    # replace with real model
    # time.sleep(0.001)
    return model.predict(x)


def run_inference(x_test: np.ndarray, batch_size: int = 64) -> np.ndarray:
    model = load_model("model_autokeras", custom_objects=ak.CUSTOM_OBJECTS)

    y_pred = []
    for k in range(0, 100):
        for i in range(0, x_test.shape[0], batch_size):
            x_batch = x_test[i: i + batch_size]
            y_batch = predict(model, x_batch)
            y_pred.append(y_batch)
    return np.concatenate(y_pred)


def run_inference_process_pool(x_test: np.ndarray, max_workers: int = 16) -> np.ndarray:
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        chunk_size = len(x_test) // max_workers

        chunks = []
        # split in to chunks
        for i in range(0, len(x_test), chunk_size):
            chunks.append(x_test[i: i + chunk_size])

        futures = []
        # submit chunks for inference
        for chunk in chunks:
            future = executor.submit(run_inference, x_test=chunk)
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
    max_workers = 16
    _ = run_inference_process_pool(x_test=x_test, max_workers=max_workers)
    print(f"Inference {max_workers} workers {time.monotonic() - s}")


if __name__ == "__main__":
    main()
