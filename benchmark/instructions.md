
```
export PYTHONPATH=.
export WANDB_API_KEY=********
```

### Locust test 

```
cd serving
uvicorn fast_api_server:app --reload
```

cd benchmark
locust

### Model test

```
cd benchmark
python -m cProfile -o results.prof model.py
snakeviz results.prof
```


### Deployments

```
cd benchmark/k8s
kubectl apply -f fastapi-server.yaml
streamlit.yaml
```

### Optimisation
In benchmark folder you can find model.png and optimised.png files.

optimised.png - profiling model trained in inference folder. Model weight 31.6mb and overall has better performance

model.png - profiling model trained in benchmark folder. Model weight 8.4mb

