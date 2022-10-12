## Inference 
to run inference to test 1 and 8 workers
`cd inference
export PYTHONPATH=.
python inference.py`

results can be visible in `one-worker.png` and `8-workers.png`
`1 worker- 70.7
8 workers- 57.3`

## Training results 
`
wandb data available in `https://wandb.ai/securims/ml-in-prod/overview`
`


## Build Container 

```
make build
```

## Run Container

```
make run_dev
```

## Run tests

```
make test
```
