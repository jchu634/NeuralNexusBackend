import pytest
from library import create_app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    my_app = create_app(config={
        "ENV_TYPE": "production",
        "IMAGE_DEFAULT_EXPIRY_PERIOD": 5,
        "CACHE_TIMEOUT_PERIOD": 10,
        "AUTH_SECRET_KEY": "570caa4d8df41bd1176dfb267757af96835de1a1381543a680be1f7531fc521c",
        "MEMORY_DATABASE": True

        # 'WTF_CSRF_ENABLED': False,                       # test_client will not send a CSRF token, so disable validation.
    })

    return TestClient(my_app)


@pytest.fixture()
def test_user():
    return {"username": "test", "password": "testpassword"}


# class AuthenticationManager:
#     def __init__(self, client):
#         self.__client = client

    # def login(self, user_name='thorke', password='cLQ^C#oFXloS'):
    #     return self.__client.post(
    #         'authentication/login',
    #         data={'user_name': user_name, 'password': password}
    #     )

    # def logout(self):
    #     return self.__client.get('/auth/logout')


# @pytest.fixture
# def auth(client):
#     return AuthenticationManager(client)
