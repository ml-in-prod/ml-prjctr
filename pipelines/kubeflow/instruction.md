### Install kind

`brew install kind`

### Create cluster

`kind create cluster`


### Install kubeflow
```
export PIPELINE_VERSION=1.8.5
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"
```

### Port forward
`kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80`

### Export WANDB env
`export WANDB_API_KEY=key`

### Create pipelines
```
python3 training-pipeline.py http://0.0.0.0:8080
python3 inference-pipeline.py http://0.0.0.0:8080
```