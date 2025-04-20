import allure


@allure.feature('Обновление данных пользователя')
class TestUserUpdate:
    @allure.story('Обновление с авторизацией')
    def test_update_authorized_user(self, api, authorized_user):
        new_data = {"name": "New Name"}
        response = api.update_user(authorized_user["token"], new_data)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"]["name"] == "New Name"

    @allure.story('Обновление без авторизации')
    def test_update_unauthorized_user(self, api):
        response = api.update_user("", {"name": "New Name"})

        assert response.status_code == 401
        assert response.json()["success"] is False