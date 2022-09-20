from unicodedata import numeric
import pandas as pd
import numpy as np
from client import MinioClient
from pathlib import Path

import time
import matplotlib.pyplot as plt


n_rows = 100000


def benchmark(format: str):
    path = Path("dataset." + format).resolve()
    start_save = time.time()
    minio_client.upload_file("benchmark", path)
    end_save = time.time()

    start_load = time.time()
    minio_client.download_file("benchmark", path.name, path)
    end_load = time.time()

    save_time.append(end_save - start_save)
    load_time.append(end_load - start_load)


def build_plot(time, plot_name, file_name):
    plt.bar(range(6), time)
    ax = plt.subplot()
    plt.suptitle(plot_name)
    ax.set_xticks(range(6))
    ax.set_xticklabels(formats)
    plt.xlabel("Results")
    plt.savefig(file_name)
    plt.clf()


# generate dataset
dataset = pd.DataFrame(
    data={
        'string': np.random.choice(('apple', 'banana', 'carrot'), size=n_rows),
        'timestamp': pd.date_range("20130101", periods=n_rows, freq="s"),
        'integer': np.random.choice(range(0, 10), size=n_rows),
        'float': np.random.uniform(size=n_rows),
    },
)

dataset.info()

# create datasets in different formats
dataset.to_csv('dataset.csv', index=False)
dataset.to_feather('dataset.feather')
dataset.to_parquet('dataset.parquet')
dataset.to_hdf('dataset.h5', key='dataset', mode='w')
dataset.to_xarray().to_netcdf('dataset.nc', engine='h5netcdf')
dataset.to_json("dataset.json")


formats = ['csv', 'json', 'feather', 'parquet', 'h5', 'nc']
save_time = []
load_time = []

minio_client = MinioClient()
minio_client.create_bucket("benchmark")

for format in formats:
    benchmark(format)


build_plot(save_time, 'Save Benchmark', 'save_benchmark.png')

build_plot(load_time, 'Load Benchmark', 'load_benchmark.png')
