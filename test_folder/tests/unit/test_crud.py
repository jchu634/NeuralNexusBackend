from pathlib import Path
import pytest
from library.database.crud import *

test_user = {
    "username": "pytestDatabase",
    "email": "pytest@test.test",
    "password": "pytestpassworddatabase"
}


def test_create_and_get_user(get_db):
    create_user(get_db, username=test_user["username"],
                email=test_user["email"], password=test_user["password"])
    user = get_users_by_username(get_db, test_user["username"])
    assert user.id != None
    assert user.username == test_user["username"]
    assert user.email == test_user["email"]
    assert user.password_hash != test_user["password"]
    assert user.is_admin == False
    return user


@pytest.mark.dependency(depends=["test_create_and_get_user"])
def test_set_admin(get_db, username=test_user["username"]):
    set_user_admin_by_username(get_db, username, True)
    user = get_users_by_username(get_db, username)
    assert user.is_admin == True
    return user
