import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from fast_api_server import app

client = TestClient(app)

def test_server_started():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Server started"


def test_predict():
    response = client.post("/predict", json={"text": "this is test text for fast api server"})
    print(response)
    assert response.status_code == 200