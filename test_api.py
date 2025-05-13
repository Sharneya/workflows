import requests
import pytest
from jsonschema import validate

# Тест для GET запроса
def test_get_users():
    response = requests.get("https://reqres.in/api/users?page=2")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)

# Схема для валидации
schema = {
    "type": "object",
    "properties": {
        "page": {"type": "number"},
        "per_page": {"type": "number"},
        "total": {"type": "number"},
        "total_pages": {"type": "number"},
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "number"},
                    "email": {"type": "string"},
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "avatar": {"type": "string"}
                },
                "required": ["id", "email", "first_name", "last_name", "avatar"]
            }
        },
        "support": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "text": {"type": "string"}
            },
            "required": ["url", "text"]
        }
    },
    "required": ["page", "per_page", "total", "total_pages", "data", "support"]
}

# Тест валидации схемы
def test_get_users_schema():
    response = requests.get("https://reqres.in/api/users?page=2")
    validate(instance=response.json(), schema=schema)

# Тест POST запроса
def test_create_user():
    payload = {"name": "Alice", "job": "Engineer"}
    response = requests.post("https://reqres.in/api/users", json=payload)
    assert response.status_code == 201
    response_data = response.json()
    assert "id" in response_data
    assert response_data["name"] == payload["name"]
    assert response_data["job"] == payload["job"]

# Параметризованный тест
@pytest.mark.parametrize("name, job", [("Bob", "QA"), ("Eve", "DevOps")])
def test_create_user_params(name, job):
    response = requests.post(
        "https://reqres.in/api/users",
        json={"name": name, "job": job}
    )
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["name"] == name
    assert response_data["job"] == job

# Тест обработки ошибок
def test_invalid_login():
    response = requests.post(
        "https://reqres.in/api/login",
        json={"email": "test@test"}
    )
    assert response.status_code == 400
    assert "error" in response.json()

# Тест несуществующего ресурса
def test_not_found():
    response = requests.get("https://reqres.in/api/users/999")
    assert response.status_code == 404
