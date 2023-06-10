from .test_config import *


def test_create_wallet(sign_up_pre_sign_in):
    """use fixture to get authToken, and create new wallet"""
    token = sign_up_pre_sign_in.__wrapped__()
    currency = random.choice(currencies)
    type_wallet = random.choice(types)
    data = {
        "type": type_wallet,
        "currency": currency
    }
    header = {'Authorization': f'Token {token}'}
    response = requests.post(url=f'{URL}wallets/', data=data, headers=header)
    assert response.status_code == 201, f'Received status code is not equal to 201!!!,\nbut gotten {response.status_code}'


def test_create_max_wallets_and_test_delete(sign_up_pre_sign_in):
    token = sign_up_pre_sign_in.__wrapped__()
    names_wallets = []
    for num in range(1, 7):
        currency = random.choice(currencies)
        type_wallet = random.choice(types)
        header = {'Authorization': f'Token {token}'}
        data = {
            "type": type_wallet,
            "currency": currency
        }
        response = requests.post(url=f'{URL}wallets/', data=data, headers=header)
        match num:
            case 6:
                assert response.status_code == 400, 'The user can not create more than 5 wallets!'
            case _:
                names_wallets.append(response.json().get('name'))
                assert response.status_code == 201, f'User can not create a wallet!\nToken: {token}\n{type_wallet=} {currency=}'
    for name in names_wallets:
        response = requests.delete(url=f'{URL}wallets/{name}/', headers=header)
        assert response.status_code == 200, f'User can not delete the wallet!!!\n{name=}'