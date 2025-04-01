import allure
import requests

class TestCourierAuthorization:

    @allure.title("Успешная авторизация курьера")
    def test_courier_authorization_successful(self, register_new_courier_and_return_login_password):
        courier_data = register_new_courier_and_return_login_password
        login, password, first_name = courier_data
        courier_authorization_url = 'https://qa-scooter.praktikum-services.ru/api/v1/courier/login'
        authorization_data = {"login": login,
                   "password": password}
        response = requests.post(courier_authorization_url, authorization_data)
        assert response.status_code == 200 and 'id' in response.json()

    @allure.title("Авторизация курьера без пароля")
    def test_courier_authorization_without_password_failed(self, register_new_courier_and_return_login_password):
        courier_data = register_new_courier_and_return_login_password
        login, password, first_name = courier_data
        courier_authorization_url = 'https://qa-scooter.praktikum-services.ru/api/v1/courier/login'
        authorization_data = {"login": login}
        response = requests.post(courier_authorization_url, authorization_data)
        response_json = response.json()
        assert response.status_code == 400 and response_json["message"] == "Недостаточно данных для входа"

    @allure.title("Авторизация курьера с неправильным паролем")
    def test_courier_authorization_wrong_password_error(self, register_new_courier_and_return_login_password):
        courier_data = register_new_courier_and_return_login_password
        login, password, first_name = courier_data
        courier_authorization_url = 'https://qa-scooter.praktikum-services.ru/api/v1/courier/login'
        authorization_data = {"login": login,
                   "password": "123456"}
        response = requests.post(courier_authorization_url, authorization_data)
        response_json = response.json()
        assert response.status_code == 404 and response_json["message"] == "Учетная запись не найдена"

    @allure.title("Авторизация несуществующим курьером")
    def test_courier_authorization_without_courier_data_in_data_base(self, register_new_courier_and_return_login_password):
        courier_authorization_url = 'https://qa-scooter.praktikum-services.ru/api/v1/courier/login'
        authorization_data = {"login": "Loginov",
                              "password": "123456"}
        response = requests.post(courier_authorization_url, authorization_data)
        response_json = response.json()
        assert response.status_code == 404 and response_json["message"] == "Учетная запись не найдена"