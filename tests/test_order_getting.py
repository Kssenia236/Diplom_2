import allure


@allure.feature('Получение заказов')
class TestOrderGetting:

    @allure.story('Получение заказов авторизованного пользователя')
    def test_get_orders_with_auth(self, api, authorized_user):
        response = api.get_user_orders(authorized_user["token"])

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)

    @allure.story('Получение заказов без авторизации')
    def test_get_orders_without_auth(self, api):
        response = api.get_user_orders()

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert "message" in response.json()

    @allure.story('Получение заказов с неверным токеном')
    def test_get_orders_with_invalid_token(self, api):
        response = api.get_user_orders("invalid_token")

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert "message" in response.json()

    @allure.story('Получение заказов с просроченным токеном')
    def test_get_orders_with_expired_token(self, api):
        expired_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY0MDJmYjZjOWQyZmU0MDAxYjJjZDYyNSIsImlhdCI6MTY3NzkyMDEwOCwiZXhwIjoxNjc3OTIxMzA4fQ.SqFZpnpNhXFXfv5q0CLXiBkEmH-X7kKqXl1QgUYE4Kw"

        response = api.get_user_orders(expired_token)

        assert response.status_code == 403
        assert response.json()["success"] is False
        assert "message" in response.json()

    @allure.story('Проверка структуры заказа в ответе')
    def test_order_structure(self, api, authorized_user):
        ingredients_response = api.get_ingredients()
        ingredient_ids = [ingredients_response.json()["data"][0]["_id"]]
        api.create_order(ingredient_ids, authorized_user["token"])
        response = api.get_user_orders(authorized_user["token"])

        assert response.status_code == 200
        assert response.json()["success"] is True

        if response.json()["orders"]:
            order = response.json()["orders"][0]
            required_fields = ["_id", "ingredients", "status", "name",
                               "createdAt", "updatedAt", "number"]

            for field in required_fields:
                assert field in order