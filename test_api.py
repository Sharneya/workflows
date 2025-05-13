def test_get_users():  
    response = requests.get("https://reqres.in/api/users?page=2")  
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
    response = requests.get("https://reqres.in/api/users?page=2")  
    assert validate(response.json(), schema) is None  
def test_create_user():  
    payload = {"name": "Alice", "job": "Engineer"}  
    response = requests.post("https://reqres.in/api/users", json=payload)  
    assert response.status_code == 201  
    assert response.json()["id"] is not None  

import pytest  
@pytest.mark.parametrize("name, job", [("Bob", "QA"), ("Eve", "DevOps")])  
def test_create_user_params(name, job):  
    response = requests.post("https://reqres.in/api/users", json={"name": name, "job": job})  
    assert response.status_code == 201  


def test_invalid_login():  
    response = requests.post("https://reqres.in/api/login", json={"email": "test@test"})  
    assert response.status_code == 400  
    assert "error" in response.json()  


def test_not_found():  
    response = requests.get("https://reqres.in/api/users/999")  
    assert response.status_code == 404  
