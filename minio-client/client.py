from minio import Minio
from pathlib import Path

ACCESS_KEY = "minio"
SECRET_KEY = "minio123"
ENDPOINT = "localhost:9000"


class MinioClient:
    def __init__(self) -> None:
        client = Minio(ENDPOINT, access_key=ACCESS_KEY,
                       secret_key=SECRET_KEY, secure=False)
        self.client = client

    def get_bucket(self, bucket_name: str):
        found = self.client.bucket_exists(bucket_name=bucket_name)
        if found:
            return "Bucket existed"
        else:
            return None

    def get_buckets(self):
        return self.client.list_buckets()

    def create_bucket(self, bucket_name: str):
        found = self.client.bucket_exists(bucket_name)
        if not found:
            self.client.make_bucket(bucket_name)
        else:
            print("Bucket already exists")

    def remove_bucket(self, bucket_name: str):
        self.client.remove_bucket(bucket_name)

    def upload_file(self, bucket_name: str, file_path: Path):
        self.client.fput_object(bucket_name, file_path.name, file_path)
        return "uploaded"

    def download_file(self, bucket_name, object_name: str, file_path: Path):
        self.client.fget_object(
            bucket_name, object_name, file_path=str(file_path))

    def remove_file(self, bucket_name: str, object_name: str):
        self.client.remove_object(bucket_name, object_name)
        return "removed"
