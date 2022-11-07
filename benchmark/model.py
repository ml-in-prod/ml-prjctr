from pathlib import Path
import pytest

# from inference import get_data, train_model, predict
from tensorflow.keras.models import load_model
import autokeras as ak
from sklearn.model_selection import train_test_split

import wandb
from wandb.keras import WandbCallback

import numpy
import timeit

import cProfile, pstats

if __name__ == '__main__':
    test_text = '''At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.'''

    wandb.init(project="ml-in-prod")

    wandb.config = {
       "learning_rate": 0.001,
       "epochs": 5,
       "batch_size": 128
    }

    artifact = wandb.use_artifact("securims/ml-in-prod/model_autokeras:latest", type="model")
    artifact_dir = artifact.download(root='model_autokeras')

    profiler = cProfile.Profile()
    profiler.enable()
    model = load_model('model_autokeras', custom_objects=ak.CUSTOM_OBJECTS)

    model.predict([test_text])

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('tottime')
    stats.print_stats()   

