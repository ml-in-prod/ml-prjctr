to connect to minicube run

```
k port-forward minio-deployment 9000:9000
```

to run tests
```
cd minio-client
pytest -q client_tests.py
```

to run benchmark
```
cd minio-client
python benchmark.py
```
Program will generate dataset and save it to different formats then will save and download each file to minio. Batchmarks will be saved to png files.
