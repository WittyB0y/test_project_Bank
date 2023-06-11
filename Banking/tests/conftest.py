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


@pytest.fixture
def sign_up_pre_sign_in_for_creation_wallet():
    """do register user, then login user and returns tuple with header-data and body-data"""
    data = {
        'username': USER,
        'password': PASSWORD,
        'email': EMAIL,
    }
    response = requests.post(url=f'{URL}register/', data=data)
    token = sign_in.__wrapped__()
    currency = random.choice(currencies)
    type_wallet = random.choice(types)
    data_wallet = {
        "type": type_wallet,
        "currency": currency
    }
    header = {'Authorization': f'Token {token}'}
    return header, data_wallet


@pytest.fixture
def sign_up_pre_sign_in_for_creation_max_wallets():
    """do register user, then get authToken and create max wallets"""
    token = sign_in.__wrapped__()
    wallets_name = []
    header = {'Authorization': f'Token {token}'}
    currency = random.choice(currencies)
    type_wallet = random.choice(types)
    data_wallet = {
        "type": type_wallet,
        "currency": currency
    }
    for wallet in range(1, 6):
        response = requests.post(url=f'{URL}wallets/', data=data_wallet, headers=header)
        wallets_name.append(response.json().get('name'))
    return header, wallets_name, data_wallet


@pytest.fixture
def sign_up_pre_sign_in_for_delete_wallets():
    wallet = create_wallet.__wrapped__()
    header ={'Authorization': f'Token {wallet["token"]}'}
    wallet = wallet[1]

    return header, wallet


@pytest.fixture
def create_wallets_for_transaction():
    data_wallet = create_wallet.__wrapped__()
    header = {'Authorization': f'Token {data_wallet["token"]}'}
    data = {
        "transfer_amount": f"{random.randint(10, 500)}.00",
        "sender": data_wallet[1],
        "receiver": data_wallet[2],
    }
    return data_wallet, header, data
