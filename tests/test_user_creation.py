import pytest
import allure


@allure.feature('Создание пользователя')
class TestUserCreation:
    @allure.story('Создание уникального пользователя')
    def test_create_unique_user(self, api, random_user_data):
        response = api.create_user(**random_user_data)

        assert response.status_code == 200
        assert response.json()["success"] is True

        token = api.login_user(
            random_user_data["email"],
            random_user_data["password"]
        ).json()["accessToken"]
        api.delete_user(token)

    @allure.story('Создание дубликата пользователя')
    def test_create_duplicate_user(self, api, authorized_user):
        response = api.create_user(
            email=authorized_user["email"],
            password=authorized_user["password"],
            name=authorized_user["name"]
        )

        assert response.status_code == 403
        assert response.json()["success"] is False

    @allure.story('Создание пользователя без обязательного поля')
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field(self, api, random_user_data, missing_field):
        data = {
            "email": random_user_data["email"] if missing_field != "email" else None,
            "password": random_user_data["password"] if missing_field != "password" else None,
            "name": random_user_data["name"] if missing_field != "name" else None
        }

        data = {k: v for k, v in data.items() if v is not None}

        try:
            response = api.create_user(**data)
            assert response.status_code == 403
            assert response.json()["success"] is False
        except TypeError:
            pass