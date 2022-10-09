import typer

from inference import get_data, train_model, run_inference_process_pool
import time

app = typer.Typer()

@app.command()
def data(path: str):
    x_train, y_train, x_test = get_data(path)
    train_model(x_train, y_train)


@app.command()
def inference(path: str):
    x_train, y_train, x_test = get_data(path)
    
    s = time.monotonic()
    _ = run_inference_process_pool(x_test=x_test, max_workers=1)
    print(f"Inference one worker {time.monotonic() - s}")


@app.command()
def inferencepool(path: str):
    x_train, y_train, x_test = get_data(path)
    
    s = time.monotonic()
    max_workers = 8
    _ = run_inference_process_pool(x_test=x_test, path="model_autokeras", max_workers=max_workers)
    print(f"Inference {max_workers} workers {time.monotonic() - s}")

if __name__ == "__main__":
    app()