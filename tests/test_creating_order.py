import allure
import pytest
import requests
from urls import Urls

class TestOrders:
    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    @allure.title("Заказ самоката в разных вариациях цвета")
    def test_choose_one_scooter_color(self, color):
        url = Urls.orders
        payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+78003553535",
        "rentTime": 2,
        "deliveryDate": "2025-03-30",
        "comment": "Saske, come back to Konoha",
        "color": color
        }
        response = requests.post(url, data = payload)
        response_json = response.json()
        assert response.status_code == 201 and "track" in response_json