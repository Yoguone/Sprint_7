import allure
import requests

class TestOrderList :

    @allure.title("Получение списка заказов")
    def test_get_order_list_successful(self):
        url = "https://qa-scooter.praktikum-services.ru/api/v1/orders"
        response = requests.get(url)
        response_json = response.json()
        assert response.status_code == 200 and (response_json["orders"], list)