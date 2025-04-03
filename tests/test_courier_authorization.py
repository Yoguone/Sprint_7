import allure
import requests
from helpers import register_new_courier_and_return_login_password
from urls import Urls

class TestCourierAuthorization:

    @allure.title("Успешная авторизация курьера")
    def test_courier_authorization_successful(self, delete_courier):
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        courier_authorization_url = Urls.courier_authorization
        authorization_data = {"login": login,
                   "password": password}
        response = requests.post(courier_authorization_url, authorization_data)
        response_json = response.json()
        assert response.status_code == 200 and 'id' in response_json
        courier_id = response_json['id']
        delete_response = delete_courier(courier_id)
        delete_response_json = delete_response.json()
        assert delete_response.status_code == 200 and delete_response_json == {"ok":True}

    @allure.title("Авторизация курьера без пароля")
    def test_courier_authorization_without_password_failed(self):
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        courier_authorization_url = Urls.courier_authorization
        authorization_data = {"login": login}
        response = requests.post(courier_authorization_url, authorization_data)
        response_json = response.json()
        assert response.status_code == 400 and response_json["message"] == "Недостаточно данных для входа"

    @allure.title("Авторизация курьера с неправильным паролем")
    def test_courier_authorization_wrong_password_error(self):
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        courier_authorization_url = Urls.courier_authorization
        authorization_data = {"login": login,
                   "password": "123456"}
        response = requests.post(courier_authorization_url, authorization_data)
        response_json = response.json()
        assert response.status_code == 404 and response_json["message"] == "Учетная запись не найдена"

    @allure.title("Авторизация несуществующим курьером")
    def test_courier_authorization_without_courier_data_in_data_base(self):
        courier_authorization_url = Urls.courier_authorization
        authorization_data = {"login": "Loginov",
                              "password": "123456"}
        response = requests.post(courier_authorization_url, authorization_data)
        response_json = response.json()
        assert response.status_code == 404 and response_json["message"] == "Учетная запись не найдена"