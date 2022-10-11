import os
import uuid
from typing import Optional

import kfp
import typer
from kfp import dsl
from kubernetes.client.models import V1EnvVar

IMAGE = "ghcr.io/ml-in-prod/ml-test:latest"

WANDB_API_KEY = os.getenv("WANDB_API_KEY")


@dsl.pipeline(name="inference_pipeline", description="inference_pipeline")
def inference_pipeline():
    inference_single = dsl.ContainerOp(
        name="inference_single",
        command="python cli.py inference ./test.csv".split(),
        image=IMAGE
    )

    inference_single.execution_options.caching_strategy.max_cache_staleness = "P0D"

    inference_multiple = dsl.ContainerOp(
        name="inference_multiple ",
        command="python cli.py inferencepool ./test.csv".split(),
        image=IMAGE,
        # artifact_argument_paths=[
        #     dsl.InputArgumentPath(load_data.outputs["train"], path="/tmp/data/train.csv"),
        #     dsl.InputArgumentPath(load_data.outputs["val"], path="/tmp/data/val.csv"),
        #     dsl.InputArgumentPath(load_data.outputs["test"], path="/tmp/data/test.csv"),
        # ],
        # file_outputs={
        #     "config": "/tmp/results/config.json",
        #     "model": "/tmp/results/model.bin",
        #     "tokenizer": "/tmp/results/tokenizer.json",
        #     "tokenizer_config": "/tmp/results/tokenizer_config.json",
        #     "special_tokens_map": "/tmp/results/special_tokens_map.json",
        #     "model_card": "/tmp/results/README.md",
        # },
    )

    # upload_model = dsl.ContainerOp(
    #     name="upload_model",
    #     command="python nlp_sample/cli.py upload-to-registry kfp-pipeline /tmp/results".split(),
    #     image=IMAGE,
    #     artifact_argument_paths=[
    #         dsl.InputArgumentPath(train_model.outputs["config"], path="/tmp/results/config.json"),
    #         dsl.InputArgumentPath(train_model.outputs["model"], path="/tmp/results/pytorch_model.bin"),
    #         dsl.InputArgumentPath(train_model.outputs["tokenizer"], path="/tmp/results/tokenizer.json"),
    #         dsl.InputArgumentPath(train_model.outputs["tokenizer_config"], path="/tmp/results/tokenizer_config.json"),
    #         dsl.InputArgumentPath(
    #             train_model.outputs["special_tokens_map"], path="/tmp/results/special_tokens_map.json"
    #         ),
    #         dsl.InputArgumentPath(train_model.outputs["model_card"], path="/tmp/results/README.md"),
    #     ],
    # )

    env_var_password = V1EnvVar(name="WANDB_API_KEY", value=WANDB_API_KEY)
    inference_single = inference_single.add_env_variable(env_var_password)


    # # TODO: should be a secret, but out of scope for this webinar
    env_var_password = V1EnvVar(name="WANDB_API_KEY", value=WANDB_API_KEY)
    inference_multiple = inference_multiple.add_env_variable(env_var_password)



def compile_pipeline() -> str:
    path = "/tmp/inference_pipeline.yaml"
    kfp.compiler.Compiler().compile(inference_pipeline, path)
    return path


def create_pipeline(client: kfp.Client, namespace: str):
    print("Creating experiment")
    _ = client.create_experiment("training", namespace=namespace)

    print("Uploading pipeline")
    name = "sample-inference"
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