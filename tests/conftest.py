import pytest
import random
import string
from helpers.api_client import ApiClient


def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


@pytest.fixture(scope="session")
def api():
    return ApiClient()


@pytest.fixture
def random_user_data():
    return {
        "email": f"test_{generate_random_string()}@test.com",
        "password": generate_random_string(8),
        "name": f"Test User {generate_random_string(5)}"
    }


@pytest.fixture
def authorized_user(api, random_user_data):
    response = api.create_user(**random_user_data)
    assert response.status_code == 200

    response = api.login_user(
        email=random_user_data["email"],
        password=random_user_data["password"]
    )
    token = response.json()["accessToken"]

    yield {**random_user_data, "token": token}

    api.delete_user(token)
