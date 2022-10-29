import random  
import string  
from tensorflow.keras.models import load_model

import wandb
import autokeras as ak
import numpy

wandb.init(project="ml-in-prod")


artifact = wandb.use_artifact("securims/ml-in-prod/model_autokeras:latest", type="model")
artifact_dir = artifact.download(root='model_autokeras')

model = load_model('model_autokeras', custom_objects=ak.CUSTOM_OBJECTS)


def upper_lower_string(length) -> str:   
    result = ''.join((random.choice(string.ascii_lowercase) for x in range(length))) # run loop until the define length  
    return result 

def predict():
    test_text = upper_lower_string(10000)
    return model.predict([test_text])

def test_my_stuff(benchmark):
    #for i in range(0,1000):
    res = benchmark(predict)

    assert type(res[0][0]) == numpy.float32
