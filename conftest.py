import requests
from urls import Urls
import pytest
from helpers import register_new_courier_and_return_login_password

@pytest.fixture
def delete_courier():
    courier_data = register_new_courier_and_return_login_password()
    yield courier_data
    login, password, first_name = courier_data
    authorization_data = {"login": login,
                          "password": password}
    response = requests.post(Urls.courier_authorization, authorization_data)
    response_json = response.json()
    courier_id = response_json['id']
    delete_courier_url = Urls.delete_courier_url
    requests.delete(f'{delete_courier_url}/{courier_id}')






