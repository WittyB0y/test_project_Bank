import random
import pytest
import requests

URL = 'http://127.0.0.1:8000/api/v1/'
RANDINT = random.randint(1000, 999999999999)
USER = f'TEST_USER_{RANDINT}'
PASSWORD = f')(+_9{RANDINT}38434#$'
EMAIL = f'{RANDINT}test@test.com'
currencies = ['RUB', "USD", "EUR"]
types = ['Visa', 'Mastercard']
endpoints = ['logout/']


@pytest.fixture
def sign_in():
    data = {
        'username': USER,
        'password': PASSWORD,
    }
    response = requests.post(url=f'{URL}login/', data=data)
    return response.json()['token']


@pytest.fixture
def sign_up_pre_sign_in():
    data = {
        'username': USER,
        'password': PASSWORD,
        'email': EMAIL,
    }
    response = requests.post(url=f'{URL}register/', data=data)
    return sign_in


@pytest.fixture
def create_wallet():
    data_wallets = {}
    token = sign_up_pre_sign_in.__wrapped__().__wrapped__()
    header = {'Authorization': f'Token {token}'}
    data = {
        "type": 'Visa',
        "currency": 'USD'
    }
    data_wallets['token'] = token
    for num in range(1, 3):
        response = requests.post(url=f'{URL}wallets/', data=data, headers=header)
        data_wallets[num] = response.json().get('name')
    return data_wallets
