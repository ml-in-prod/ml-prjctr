import numpy as np
import pandas as pd

from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from arize.pandas.logger import Client
from arize.utils.types import ModelTypes, Environments, Schema

import uuid
from datetime import datetime, timedelta

SPACE_KEY = "***"
API_KEY = "***"

model_id = "classification_model"
model_version = "1.0"
model_type = ModelTypes.SCORE_CATEGORICAL


def generate_prediction_ids(X):
    return pd.Series((str(uuid.uuid4()) for _ in range(len(X))), index=X.index)


def simulate_production_timestamps(X, days=1):
    t = datetime.now()
    current_ts, earlier_ts = t.timestamp(), (t - timedelta(days=days)).timestamp()
    return pd.Series(np.linspace(earlier_ts, current_ts, num=len(X)), index=X.index)


def init_arize():
    arize_client = Client(space_key=SPACE_KEY, api_key=API_KEY)

    return arize_client


def log_prediction(arize_client, features, X_test, y_test_pred, y_test_pred_score):
    production_dataset = X_test.join(
        pd.DataFrame(
            {
                "prediction_id": generate_prediction_ids(X_test),
                "prediction_ts": simulate_production_timestamps(X_test),
                "prediction_label": y_test_pred,
                "prediction_score": y_test_pred_score,
            }
        )
    )

    production_schema = Schema(
        prediction_id_column_name="prediction_id",
        timestamp_column_name="prediction_ts",
        prediction_label_column_name="prediction_label",
        prediction_score_column_name="prediction_score",
        feature_column_names=features,
    )

    response = arize_client.log(
        dataframe=production_dataset,
        schema=production_schema,
        model_id=model_id,
        model_version=model_version,
        model_type=model_type,
        environment=Environments.PRODUCTION,
    )

    if response.status_code == 200:
        print("Logs saved successfully")


def load_dataset():
    data = datasets.load_breast_cancer()
    X, y = datasets.load_breast_cancer(return_X_y=True)
    X, y = X.astype(np.float32), y.astype(str)
    X, y = pd.DataFrame(X, columns=data["feature_names"]), pd.Series(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, random_state=42)

    return X_train, X_test, y_train, X_val, data["feature_names"]


def train(X_train, y_train):
    clf = LogisticRegression(
        max_iter=3000, verbose=False).fit(X_train, y_train)

    return clf


def predict(model, X):
    proba = model.predict_proba(X)
    pred = pd.Series((str(np.argmax(p)) for p in proba), index=X.index)
    score = pd.Series((p[1] for p in proba), index=X.index)
    return pred, score


def predict_result(clf, train_values):
    y_pred, y_pred_score = predict(clf, train_values)

    return y_pred, y_pred_score


def main():
    X_train, X_test, y_train, X_val, features = load_dataset()

    model = train(X_train, y_train)

    arize = init_arize()

    # y_train_pred, y_train_pred_score = predict(model, X_train)
    y_val_pred, y_val_pred_score = predict(model, X_val)
    y_test_pred, y_test_pred_score = predict(model, X_test)

    log_prediction(arize, features, X_test, y_test_pred, y_test_pred_score)

    log_prediction(arize, features, X_val, y_val_pred, y_val_pred_score)


if __name__ == "__main__":
    main()
