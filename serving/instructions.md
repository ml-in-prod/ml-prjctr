```
export PYTHONPATH=.
export WANDB_API_KEY=********
```

## Streamlit

```
cd serving
streamlit run streamlit.py
```

## Fast-api

### run locally

```
cd serving
uvicorn fast_api_server:app --reload
```

### run in docker
```
docker run -e WANDB_API_KEY=***** -p 8000:8000  -it fast-api:latest  /bin/bash
uvicorn fast_api_server:app --host 0.0.0.0
```

### tests
```
cd serving/test
pytest -l test_fast_api.py
```

## Seldon

```
cd serving/k8s
```

### Create kind cluster 

```
kind create cluster --name ml-in-production --image=kindest/node:v1.21.2 --config=kind.yaml
```

### Install with helm

```
kubectl apply -f https://github.com/datawire/ambassador-operator/releases/latest/download/ambassador-operator-crds.yaml
kubectl apply -n ambassador -f https://github.com/datawire/ambassador-operator/releases/latest/download/ambassador-operator-kind.yaml
kubectl wait --timeout=180s -n ambassador --for=condition=deployed ambassadorinstallations/ambassador

kubectl create namespace seldon-system

helm install seldon-core seldon-core-operator \
    --repo https://storage.googleapis.com/seldon-charts \
    --set usageMetrics.enabled=true \
    --set ambassador.enabled=true \
    --namespace seldon-system
```
### Port forward 

```
kubectl port-forward  --address 0.0.0.0 -n ambassador svc/ambassador 7777:80
```

### Iris example
```
kubectl create -f seldon.yaml

http://0.0.0.0:7777/seldon/default/iris-model/api/v1.0/doc/#/
{ "data": { "ndarray": [[1,2,3,4]] } }

curl -X POST "http://0.0.0.0:7777/seldon/default/iris-model/api/v1.0/predictions" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"data\":{\"ndarray\":[[1,2,3,4]]}}"
```