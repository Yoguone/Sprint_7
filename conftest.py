import requests
from urls import Urls
import pytest

@pytest.fixture
def delete_courier():
    def _delete_courier(courier_id):
        delete_courier_url = Urls.delete_courier_url
        response = requests.delete(f'{delete_courier_url}/{courier_id}')
        return response
    return _delete_courier



