import allure


@allure.feature('Создание заказа')
class TestOrderCreation:
    @allure.story('Создание заказа авторизованным пользователем')
    def test_create_order_authorized(self, api, authorized_user):
        ingredients = api.get_ingredients().json()["data"][:2]
        ingredient_ids = [item["_id"] for item in ingredients]

        response = api.create_order(ingredient_ids, authorized_user["token"])

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.story('Создание заказа без авторизации')
    def test_create_order_unauthorized(self, api):
        ingredients = api.get_ingredients().json()["data"][:2]
        ingredient_ids = [item["_id"] for item in ingredients]

        response = api.create_order(ingredient_ids)

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.story('Создание заказа без ингредиентов')
    def test_create_order_without_ingredients(self, api, authorized_user):
        response = api.create_order([], authorized_user["token"])

        assert response.status_code == 400
        assert response.json()["success"] is False

    @allure.story('Создание заказа с неверными ингредиентами')
    def test_create_order_with_invalid_ingredients(self, api, authorized_user):
        response = api.create_order(["invalid_id"], authorized_user["token"])

        assert response.status_code == 500