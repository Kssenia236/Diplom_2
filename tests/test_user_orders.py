import allure


@allure.feature('Получение заказов пользователя')
class TestUserOrders:
    @allure.story('Получение заказов авторизованным пользователем')
    def test_get_orders_authorized(self, api, authorized_user):
        response = api.get_user_orders(authorized_user["token"])

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.story('Получение заказов без авторизации')
    def test_get_orders_unauthorized(self, api):
        response = api.get_user_orders()

        assert response.status_code == 401
        assert response.json()["success"] is False