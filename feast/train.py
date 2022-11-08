from datetime import datetime
from pathlib import Path

import feast
import pandas as pd
from joblib import dump

import tensorflow as tf

import wandb

fs = feast.FeatureStore(repo_path="feature_repo/")


def get_dataset() -> pd.DataFrame:
    dataset = pd.read_csv('driver.csv')
    return dataset


def add_features_to_dataset(training_df: pd.DataFrame) -> pd.DataFrame:
    training_df_with_features = fs.get_historical_features(
        entity_df=training_df,
        features=[
            "driver_hourly_stats:conv_rate",
            "driver_hourly_stats:acc_rate"
        ],
    ).to_df()

    return training_df_with_features


def train_and_save_model():
    wandb.init(project="feature-store")

    training_df = get_dataset()

    training_df['event_timestamp'] = pd.to_datetime(
        training_df['event_timestamp'])

    training_df_with_features = add_features_to_dataset(
        training_df=training_df)

    target = "score"

    train_X = training_df_with_features[training_df_with_features.columns.drop(
        target).drop("event_timestamp")]
    train_Y = training_df_with_features.loc[:, target]

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(1, activation='linear')
    ])

    model.compile(loss=tf.keras.losses.mean_absolute_error,
                  optimizer=tf.keras.optimizers.Adam(lr=0.01),
                  metrics=['mae'])

    model.fit(train_X, train_Y, epochs=100)

    model.save("tf_model")

    try:
        model.save("tf_model", save_format="tf")
    except:
        model.save("tf_model.h5")

    art = wandb.Artifact("tf_model", type="model")
    art.add_dir("tf_model")
    wandb.log_artifact(art)


if __name__ == "__main__":
    train_and_save_model()
