import logging
import numpy as np
logger = logging.getLogger('__mymodel__')

from typing import List
from tensorflow.keras.models import load_model

import autokeras as ak

import wandb
from wandb.keras import WandbCallback

class NLP_Model(object):

  def __init__(self):
    wandb.init(project="ml-in-prod")

    wandb.config = {
       "learning_rate": 0.001,
       "epochs": 5,
       "batch_size": 128
    }

    artifact = wandb.use_artifact("securims/ml-in-prod/model_autokeras:latest", type="model")
    artifact_dir = artifact.download(root="model_autokeras")

    self.model = load_model("model_autokeras", custom_objects=ak.CUSTOM_OBJECTS)
    
    wandb.finish()

    logger.info("model has been loaded and initialized...")

  def predict(self, X, features_names: List[str]):
    """ Seldon Core Prediction API """
    logger.info("predict called...")
    logger.info('converting tensor to image')

    if self.model:
      logger.info("perform inference here...")

    logger.info("returning prediction...")

    return self.model.predict(features_names)