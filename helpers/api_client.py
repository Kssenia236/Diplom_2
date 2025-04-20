import requests
import allure
from typing import Dict, Optional


class ApiClient:
    def __init__(self):
        self.base_url = "https://stellarburgers.nomoreparties.site/api"
        self.headers = {
            "Content-Type": "application/json"
        }

    @allure.step("Создание пользователя")
    def create_user(self, email: str = None, password: str = None, name: str = None) -> requests.Response:
        data = {}
        if email is not None:
            data["email"] = email
        if password is not None:
            data["password"] = password
        if name is not None:
            data["name"] = name

        return requests.post(
            f"{self.base_url}/auth/register",
            json=data,
            headers=self.headers
        )

    @allure.step("Логин пользователя")
    def login_user(self, email: str, password: str) -> requests.Response:
        data = {
            "email": email,
            "password": password
        }
        return requests.post(
            f"{self.base_url}/auth/login",
            json=data,
            headers=self.headers
        )

    @allure.step("Обновление данных пользователя")
    def update_user(self, token: str, data: Dict) -> requests.Response:
        headers = self.headers.copy()
        headers["Authorization"] = token
        return requests.patch(
            f"{self.base_url}/auth/user",
            json=data,
            headers=headers
        )

    @allure.step("Удаление пользователя")
    def delete_user(self, token: str) -> requests.Response:
        headers = self.headers.copy()
        headers["Authorization"] = token
        return requests.delete(
            f"{self.base_url}/auth/user",
            headers=headers
        )

    @allure.step("Получение данных пользователя")
    def get_user(self, token: str) -> requests.Response:
        headers = self.headers.copy()
        headers["Authorization"] = token
        return requests.get(
            f"{self.base_url}/auth/user",
            headers=headers
        )

    @allure.step("Создание заказа")
    def create_order(self, ingredients: list, token: Optional[str] = None) -> requests.Response:
        headers = self.headers.copy()
        if token:
            headers["Authorization"] = token
        return requests.post(
            f"{self.base_url}/orders",
            json={"ingredients": ingredients},
            headers=headers
        )

    @allure.step("Получение заказов пользователя")
    def get_user_orders(self, token: Optional[str] = None) -> requests.Response:
        headers = self.headers.copy()
        if token:
            headers["Authorization"] = token
        return requests.get(
            f"{self.base_url}/orders",
            headers=headers
        )

    @allure.step("Получение списка ингредиентов")
    def get_ingredients(self) -> requests.Response:
        return requests.get(
            f"{self.base_url}/ingredients",
            headers=self.headers
        )

    @allure.step("Выход из системы")
    def logout_user(self, token: str) -> requests.Response:
        data = {"token": token}
        return requests.post(
            f"{self.base_url}/auth/logout",
            json=data,
            headers=self.headers
        )

    @allure.step("Обновление токена")
    def refresh_token(self, token: str) -> requests.Response:
        data = {"token": token}
        return requests.post(
            f"{self.base_url}/auth/token",
            json=data,
            headers=self.headers
        )
