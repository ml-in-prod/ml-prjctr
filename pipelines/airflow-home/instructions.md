### Airflow


1. Install and run airflow

```
pip install apache-airflow apache-airflow-providers-cncf-kubernetes
cd pipelines
export AIRFLOW_HOME=$PWD/airflow-home
airflow standalone
```

Run to configure storage
```
cd pipelines/airflow-home
kubectl create -f airflow-volumes.yaml
```