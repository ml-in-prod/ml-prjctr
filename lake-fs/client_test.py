from re import I
from weakref import ref
import pytest
import uuid
from pathlib import Path
from client import LakeFsClient


@pytest.fixture()
def repository_name() -> str:
    return "example"


@pytest.fixture()
def branch_name() -> str:
    return "main"


@pytest.fixture()
def file() -> str:
    return "train.csv"


@pytest.fixture()
def lake_fs_client() -> LakeFsClient:
    return LakeFsClient()


class TestMinioClient:
    def test_upload_file(self, lake_fs_client: LakeFsClient, repository_name: str, branch_name: str, file: str):
        result = lake_fs_client.upload_file(
            repository=repository_name, branch=branch_name, path=file)

        assert type(result) == str

    def test_get_file(self, lake_fs_client: LakeFsClient, repository_name: str, branch_name: str, file: str):
        result = lake_fs_client.get_file(
            repository=repository_name, ref=branch_name, path=file)

        assert result != None

    def test_delete_file(self, lake_fs_client: LakeFsClient, repository_name: str, branch_name: str, file: str):
        result = lake_fs_client.delete_fle(
            repository=repository_name, branch=branch_name, path=file)

        assert type(result) == str
