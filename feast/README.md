```
export WANDB_API_KEY=********
```

### Instal feast

```
pip install feast
cd feast/feature_repo
feast apply
```

### Run training
```
cd feast
python train.py
```

### Run inference
```
cd feast
uvicorn inference:app --reload
```





