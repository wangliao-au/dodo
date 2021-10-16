import pytest
import requests
import pytest
from src.error import AccessError, InputError

BASE_URL = 'http://localhost:8080'

def test_http_register_basic():
    open('database.json', 'w').close()
    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    get_response =  requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    assert get_response == 200
    



