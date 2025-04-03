import allure
from random import randint
import requests
from helpers import register_new_courier_and_return_login_password
from urls import Urls

class TestCreatingCourier:

    @allure.title("Успешная регистрация курьера")
    def test_register_new_courier_successful(self):
        url = Urls.creating_courier
        payload = {"login": f"Testov + {randint(1, 999)}",
                   "password": "123456",
                   "firstName": "Testik"}
        response = requests.post(url, data=payload)
        response_json = response.json()
        assert response.status_code == 201 and response_json == {'ok': True}

    @allure.title("Ошибка создания 2 идентичных курьеров")
    def test_register_two_identical_courier_failed(self):
        first_courier = register_new_courier_and_return_login_password()
        login, password, first_name = first_courier
        url = Urls.creating_courier
        second_courier = {"login": login,
        "password": '123456',
        "firstName": 'Stepan'}
        second_courier_response = requests.post(url, data = second_courier)
        second_courier_response_json = second_courier_response.json()
        assert (second_courier_response.status_code == 409
                and second_courier_response_json['message'] == "Этот логин уже используется")

    @allure.title("Ошибка регистрации с незаполненным паролем")
    def test_register_new_courier_without_password_failed(self):
        url = Urls.creating_courier
        courier = register_new_courier_and_return_login_password()
        login, password, first_name  = courier
        payload = {"login": login,
                   "firstName": first_name}
        response = requests.post(url, data = payload)
        response_json = response.json()
        assert response.status_code == 400 and response_json['message'] == "Недостаточно данных для создания учетной записи"

    @allure.title("Возвращение ошибки при незаполненном пароле")
    def test_register_new_courier_without_password_return_400(self):
        url = Urls.creating_courier
        courier = register_new_courier_and_return_login_password()
        login, password, first_name  = courier
        payload = {"login": login,
                   "firstName": first_name}
        response = requests.post(url, data=payload)
        status_code = 400
        response_json = response.json()
        assert response.status_code == status_code and response_json['message'] == "Недостаточно данных для создания учетной записи"

    @allure.title("Тело ответа содержит 'ok: True'")
    def test_register_new_courier_return_201(self):
        url = Urls.creating_courier
        payload = {"login": f"Testov + {randint(1, 999)}",
                   "password": "123456",
                   "firstName": "Testik"}
        response = requests.post(url, data=payload)
        assert response.json() == {"ok":True} and response.status_code == 201

    @allure.title("Регистрация курьера без имени")
    def test_register_new_courier_without_first_name_successful(self):
        url = Urls.creating_courier
        payload = {"login": f"Testov + {randint(1, 999)}",
                   "password": '123456'}
        response = requests.post(url,data = payload)
        assert response.status_code == 201 and response.json() == {'ok': True}

    @allure.title("Регистрация курьера, который уже есть в базе данных")
    def test_register_new_courier_with_login_in_data_base(self):
        url = Urls.creating_courier
        courier = register_new_courier_and_return_login_password()
        login, password, first_name = courier
        second_courier = {"login": login,
                   "password": password,
                   "firstName": first_name}
        second_courier_response = requests.post(url, second_courier)
        assert second_courier_response.status_code == 409 and second_courier_response.json() == {"message": "Этот логин уже используется"}