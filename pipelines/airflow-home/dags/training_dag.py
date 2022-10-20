from datetime import datetime

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import models as k8s

volume = k8s.V1Volume(name="training-storage", persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name="training-storage"),)
volume_mount = k8s.V1VolumeMount(name="training-storage", mount_path="/", sub_path=None)


IMAGE = "ghcr.io/ml-in-prod/ml-test:latest"

with DAG(start_date=datetime(2021, 1, 1), catchup=False, schedule_interval=None, dag_id="training_dag") as dag:

    load_data = KubernetesPodOperator(
        name="load_data",
        image=IMAGE,
        cmds=["python", "cli.py", "data", "./test.csv"],
        task_id="load_data",
        in_cluster=False,
        namespace="default",
        volumes=[volume],
        volume_mounts=[volume_mount],
    )

    train_and_upload_model = KubernetesPodOperator(
        name="train_and_upload_model",
        image=IMAGE,
        cmds=["python", "cli.py", "train", "./test.csv"],
        task_id="train_and_upload_model",
        in_cluster=False,
        env_vars={"WANDB_API_KEY": ""},
        namespace="default",
        volumes=[volume],
        volume_mounts=[volume_mount],
    )
   
    load_data >> train_and_upload_model