from jsonschema import validate
import pytest
import requests


def test_get_users():
    headers = {"x-api-key": "reqres-free-v1"}
    response = requests.get("https://reqres.in/api/users?page=2", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data


schema = {
    "type": "object",
    "properties": {
        "page": {"type": "number"},
        "data": {"type": "array"}
    }
}


def test_get_users_schema():
    headers = {"x-api-key": "reqres-free-v1"}
    response = requests.get("https://reqres.in/api/users?page=2", headers=headers)
    assert validate(response.json(), schema) is None


def test_create_user():
    payload = {"name": "Alice", "job": "Engineer"}
    headers = {"x-api-key": "reqres-free-v1"}
    response = requests.post("https://reqres.in/api/users", json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json()["id"] is not None


@pytest.mark.parametrize("name, job", [("Bob", "QA"), ("Eve", "DevOps")])
def test_create_user_params(name, job):
    headers = {"x-api-key": "reqres-free-v1"}
    response = requests.post("https://reqres.in/api/users", json={"name": name, "job": job}, headers=headers)
    assert response.status_code == 201


def test_invalid_login():
    headers = {"x-api-key": "reqres-free-v1"}
    response = requests.post("https://reqres.in/api/login", json={"email": "test@test"}, headers=headers)
    assert response.status_code == 400
    assert "error" in response.json()


def test_not_found():
    headers = {"x-api-key": "reqres-free-v1"}
    response = requests.get("https://reqres.in/api/users/999", headers=headers)
    assert response.status_code == 404
