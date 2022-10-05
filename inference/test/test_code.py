import sys
sys.path.append('../inference')


from pathlib import Path
import pytest

from inference import get_data, run_inference, train_model, run_inference_process_pool
from tensorflow.keras.models import load_model
import autokeras as ak

import numpy as np

@pytest.fixture()
def test_file_path() -> str:
    return "./test.csv"

@pytest.fixture()
def test_text() -> str:
    return '''At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.'''


def test_load_data(test_file_path: str):
    x_train, y_train, x_test = get_data(test_file_path)

    assert type(x_train) == np.ndarray
    assert type(y_train) == np.ndarray
    assert type(x_test) == np.ndarray


def test_inference(test_file_path: str):
    x_train, y_train, x_test = get_data(test_file_path)
    
    train_model(x_train, y_train)

    path = str(Path().parent.resolve())
    model_path = Path(path + '/model_autokeras')
    
    res = run_inference(x_test, model_path)
    assert type(res) == np.ndarray


# def test_inference_process_pool(test_file_path: str):
#     x_train, y_train, x_test = get_data(test_file_path)
    
#     train_model(x_train, y_train)

#     path = str(Path().parent.resolve())
#     model_path = Path(path + '/model_autokeras')

#     res = run_inference_process_pool(x_test, model_path)
#     assert type(res) == np.ndarray

