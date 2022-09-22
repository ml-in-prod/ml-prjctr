import lakefs_client
from lakefs_client import models
from lakefs_client.client import LakeFSClient

import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')


class LakeFsClient:
    def __init__(self) -> None:
        configuration = lakefs_client.Configuration()
        configuration.username = USERNAME
        configuration.password = PASSWORD
        configuration.host = HOST
        client = LakeFSClient(configuration)

        self.client = client

    def upload_file(self, repository: str, branch: str, path: str):
        try:
            with open(path, 'rb') as f:
                self.client.objects.upload_object(
                    repository=repository, branch=branch, path=path, content=f)

                return 'uploaded'
        except:
            return None

    def get_file(self, repository: str, ref: str, path: str):
        try:
            return self.client.objects.get_object(repository=repository, ref=ref, path=path)
        except:
            return None

    def delete_fle(self, repository: str, branch: str, path: str):
        try:
            self.client.objects.delete_object(
                repository=repository, branch=branch, path=path)

            return 'deleted'
        except:
            return None


LakeFSClient()
