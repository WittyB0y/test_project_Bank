import requests

from .conftest import URL


def test_create_wallet(sign_up_pre_sign_in_for_creation_wallet):
    """use fixture to get authToken, and create new wallet"""
    response = requests.post(url=f'{URL}wallets/', data=sign_up_pre_sign_in_for_creation_wallet[1],
                             headers=sign_up_pre_sign_in_for_creation_wallet[0])
    assert response.status_code == 201, f'Received status code is not equal to 201!!!,\nbut gotten {response.status_code}'


def test_create_max_wallets(sign_up_pre_sign_in_for_creation_max_wallets):
    """use fixture to create 5 wallets, and try to create 6th wallet"""
    header, data = sign_up_pre_sign_in_for_creation_max_wallets[0], sign_up_pre_sign_in_for_creation_max_wallets[2]
    response = requests.post(url=f'{URL}wallets/', data=data, headers=header)
    assert response.status_code == 400, 'The user can not create more than 5 wallets!'


def test_delete_wallets(sign_up_pre_sign_in_for_delete_wallets):
    """use fixture to create wallet, and try to delete wallet"""
    wallet, token = sign_up_pre_sign_in_for_delete_wallets[1], sign_up_pre_sign_in_for_delete_wallets[0]
    response = requests.delete(url=f'{URL}wallets/{wallet}/', headers=token)
    assert response.status_code == 200, f'User can not delete the wallet!!!\n{wallet=}'