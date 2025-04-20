import allure

@allure.feature('Логин пользователя')
class TestUserLogin:
    @allure.story('Успешный логин')
    def test_login_success(self, api, authorized_user):
        response = api.login_user(
            email=authorized_user["email"],
            password=authorized_user["password"]
        )

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

    @allure.story('Логин с неверными данными')
    def test_login_with_invalid_credentials(self, api):
        response = api.login_user(
            email="wrong@email.com",
            password="wrongpassword"
        )

        assert response.status_code == 401
        assert response.json()["success"] is False