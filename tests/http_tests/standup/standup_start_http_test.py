import time
import requests
from src import config

BASE_URL = config.url

def test_http_invalid_channel_id():
    '''
    Test when the channel_id is invalid
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    owner = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': owner['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    standup_start_praram = {
        'token': owner['token'],
        'channel_id': channel['channel_id'] + 999,
        'length': 100
    }
    response = requests.post(f"{BASE_URL}/standup/start/v1", json = standup_start_praram)
    assert response.status_code == 400

def test_http_length_negative():
    ''''
    Test when the length is negative
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    owner = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': owner['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    invalid_length = -1

    standup_start_praram = {
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'length': invalid_length
    }
    response = requests.post(f"{BASE_URL}/standup/start/v1", json = standup_start_praram)
    assert response.status_code == 400

def test_http_invalid_token():
    '''
    Test when the token is invalid.
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    owner = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': owner['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    standup_start_praram = {
        'token': owner['token'] + '999',
        'channel_id': channel['channel_id'],
        'length': 10
    }
    response = requests.post(f"{BASE_URL}/standup/start/v1", json = standup_start_praram)
    assert response.status_code == 403

def test_http_auth_not_member():
    '''
    Test when the auth user is not a member of the channel.
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    owner = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': owner['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    register_param_1 = {
        "email": "liaowang@gmail.com",
        "password": "liaowang0207",
        "name_first": "wang",
        "name_last": "liao"
    }
    non_member = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    standup_start_praram = {
        'token': non_member['token'],
        'channel_id': channel['channel_id'],
        'length': 100
    }
    response = requests.post(f"{BASE_URL}/standup/start/v1", json = standup_start_praram)
    assert response.status_code == 403

def test_http_standup_is_running():
    '''
    Test if the standup is running in the currently channel.
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    owner = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': owner['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    standup_start_praram = {
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'length': 100
    }
    response = requests.post(f"{BASE_URL}/standup/start/v1", json = standup_start_praram)
    assert response.status_code == 200

    response = requests.post(f"{BASE_URL}/standup/start/v1", json = standup_start_praram)
    assert response.status_code == 400

def test_http_standup_start_basic():
    '''
    Test if standup working properly
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    owner = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': owner['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    standup_active_praram = {
        'token': owner['token'],
        'channel_id': channel['channel_id'],
    }
    response = requests.get(f"{BASE_URL}/standup/active/v1", params = standup_active_praram)
    assert response.status_code == 200
    assert not response.json()['is_active'] and response.json()['time_finish'] == None

    standup_start_praram = {
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'length': 1
    }
    response = requests.post(f"{BASE_URL}/standup/start/v1", json = standup_start_praram)
    assert response.status_code == 200
    time_finish =  response.json()['time_finish']

    standup_active_praram = {
        'token': owner['token'],
        'channel_id': channel['channel_id'],
    }
    response = requests.get(f"{BASE_URL}/standup/active/v1", params = standup_active_praram)
    assert response.status_code == 200

    time.sleep(1)
    assert response.json()['is_active'] and response.json()['time_finish'] == time_finish
    