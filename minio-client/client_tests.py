from re import I
import pytest
import uuid
from pathlib import Path
from client import MinioClient


@pytest.fixture()
def bucket_name() -> str:
    return "test"


@pytest.fixture()
def bucket_to_remove_name() -> str:
    return "remove"


@pytest.fixture()
def minio_client() -> MinioClient:
    return MinioClient()


@pytest.fixture()
def file_to_save(tmp_path: Path) -> Path:
    _file_to_save = tmp_path / f"{uuid.uuid4()}.mock"
    open(_file_to_save, "a").close()
    return _file_to_save


class TestMinioClient:
    def test_get_buckets(self, minio_client: MinioClient):
        buckets = minio_client.get_buckets()

        assert type(buckets) == list

    def test_create_bucket(self, minio_client: MinioClient, bucket_name: str, bucket_to_remove_name: str):
        minio_client.create_bucket(bucket_name)

        minio_client.create_bucket(bucket_to_remove_name)

        found = minio_client.get_bucket(bucket_name)

        assert type(found) == str

    def test_upload_file(self, minio_client: MinioClient, bucket_name: str, file_to_save: Path, tmp_path: Path):
        result = minio_client.upload_file(bucket_name, file_to_save)
        assert result == 'uploaded'

    def test_download_file(self, minio_client: MinioClient, bucket_name: str, file_to_save: Path, tmp_path: Path):
        minio_client.upload_file(bucket_name, file_to_save)
        path_to_save = tmp_path / "saved_file.mock"
        minio_client.download_file(bucket_name,
                                   object_name=file_to_save.name, file_path=path_to_save)
        assert path_to_save.exists()

    def test_remove_file(self, minio_client: MinioClient, bucket_name: str, file_to_save: Path, tmp_path: Path):
        minio_client.upload_file(bucket_name, file_to_save)

        result = minio_client.remove_file(
            bucket_name,  object_name=file_to_save.name)

        assert result == "removed"

    def test_remove_bucket(self, minio_client: MinioClient, bucket_to_remove_name: str):
        minio_client.remove_bucket(bucket_to_remove_name)

        found = minio_client.get_bucket(bucket_to_remove_name)

        assert found == None
