import os
import uuid
from typing import Optional

import kfp
import typer
from kfp import dsl
from kubernetes.client.models import V1EnvVar

IMAGE = "ghcr.io/ml-in-prod/ml-test:latest"

# WANDB_PROJECT = os.getenv("WANDB_PROJECT")
WANDB_API_KEY = os.getenv("WANDB_API_KEY")


@dsl.pipeline(name="training_pipeline", description="training_pipeline")
def training_pipeline():
    load_data = dsl.ContainerOp(
        name="load_data",
        command="python cli.py data ./test.csv".split(),
        image=IMAGE,
        file_outputs={"train": "/usr/src/app/train.csv", "val": "/usr/src/app/val.csv", "test": "/usr/src/app/test_val.csv"}
    )

    load_data.execution_options.caching_strategy.max_cache_staleness = "P0D"

    train_model = dsl.ContainerOp(
        name="train_model ",
        command="python cli.py train ./test.csv".split(),
        image=IMAGE,
        artifact_argument_paths=[
            dsl.InputArgumentPath(load_data.outputs["train"], path="/usr/src/app/train.csv"),
            dsl.InputArgumentPath(load_data.outputs["val"], path="/usr/src/app/val.csv"),
            dsl.InputArgumentPath(load_data.outputs["test"], path="/usr/src/app/test_val.csv"),
        ],
    )

    env_var_password = V1EnvVar(name="WANDB_API_KEY", value=WANDB_API_KEY)
    train_model = train_model.add_env_variable(env_var_password)


def compile_pipeline() -> str:
    path = "/tmp/training_pipeline.yaml"
    kfp.compiler.Compiler().compile(training_pipeline, path)
    return path


def create_pipeline(client: kfp.Client, namespace: str):
    print("Creating experiment")
    _ = client.create_experiment("training", namespace=namespace)

    print("Uploading pipeline")
    name = "sample-training"
    if client.get_pipeline_id(name) is not None:
        print("Pipeline exists - upload new version.")
        pipeline_prev_version = client.get_pipeline(client.get_pipeline_id(name))
        version_name = f"{name}-{uuid.uuid4()}"
        pipeline = client.upload_pipeline_version(
            pipeline_package_path=compile_pipeline(),
            pipeline_version_name=version_name,
            pipeline_id=pipeline_prev_version.id,
        )
    else:
        pipeline = client.upload_pipeline(pipeline_package_path=compile_pipeline(), pipeline_name=name)
    print(f"pipeline {pipeline.id}")


def auto_create_pipelines(
    host: str,
    namespace: Optional[str] = None,
):
    client = kfp.Client(host=host)
    create_pipeline(client=client, namespace=namespace)


if __name__ == "__main__":
    typer.run(auto_create_pipelines)