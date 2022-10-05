import sys
sys.path.append('../inference')

from pathlib import Path
import pytest

from inference import get_data, train_model, predict
from tensorflow.keras.models import load_model
import autokeras as ak

import numpy

@pytest.fixture()
def test_file_path() -> str:
    return "./test.csv"

@pytest.fixture()
def test_text() -> str:
    return '''At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.'''


def test_train_and_save_model(test_file_path: str):
    x_train, y_train, x_test = get_data(test_file_path)

    train_model(x_train, y_train)
    
    path = str(Path().parent.resolve())
    
    model_path = Path(path + '/model_autokeras')
    regressor_path = Path(path + '/text_regressor')

    assert model_path.exists()
    assert regressor_path.exists()
    assert model_path.is_dir()
    assert regressor_path.is_dir()


def test_prediction(test_text: str):
    model = load_model("model_autokeras", custom_objects=ak.CUSTOM_OBJECTS)
    res = predict(model, [""])
    assert type(res[0][0]) == numpy.float32

