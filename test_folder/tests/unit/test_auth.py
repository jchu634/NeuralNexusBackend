from pathlib import Path
import pytest
from test_folder.tests.unit.test_crud import test_set_admin

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scopes={
    "user": "Regular user permissions",
            "admin": "Admin priviledges (Admin API Access)"
})


# Test authentication api

test_user = {
    "username": "pytest",
    "email": "pytest@test.test",
    "password": "pytestpassword"
}
test_admin = {
    "username": "pytestadmin",
    "email": "pytest@test.test",
    "password": "pytestadminpassword"
}


def test_create_user(client, user=test_user):
    response = client.post(
        '/create_user',
        data=user
    )
    assert response.status_code == 200
    assert response.json() == {'success': 'user made'}


@pytest.mark.dependency(depends=["test_create_user", "test_set_admin"])
def test_create_admin(client, get_db):
    test_create_user(client, test_admin)
    test_set_admin(get_db, username=test_admin["username"])

    token = test_admin_login(client)
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]
    assert response.json()["username"] == test_user["username"]
    assert response.json()["uid"] != None
    assert response.json()["admin"] == True


@pytest.mark.dependency(depends=["test_create_user"])
def test_login(client):
    response = client.post("/token", data=test_user)
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
    return token

# Non-Functional, scope doesn't actually work properly


@pytest.mark.dependency(depends=["test_create_admin"])
def test_admin_login(client):
    response = client.post("/token", data={**test_admin, "scopes": "admin"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
    return token


@pytest.mark.dependency(depends=["test_login"])
def test_read_token(client):
    token = test_login(client)
    response = client.get(
        "/read_token",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {'token': token}


@pytest.mark.dependency(depends=["test_login"])
def test_get_user(client):
    token = test_login(client)
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]
    assert response.json()["username"] == test_user["username"]
    assert response.json()["uid"] != None
    assert response.json()["admin"] == False
