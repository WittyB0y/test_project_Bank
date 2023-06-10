from .test_config import *


def test_crud_transaction(create_wallet):
    wallets_data = create_wallet
    header = {'Authorization': f'Token {wallets_data["token"]}'}
    data = {
        "transfer_amount": "140.00",
        "sender": wallets_data[1],
        "receiver": wallets_data[2],
    }
    # post
    create_transaction = requests.post(url=f'{URL}wallets/transactions/', data=data, headers=header)
    assert create_transaction.status_code == 201, 'User can not create transactions!!!'
    assert create_transaction.json()['success'] == 'Transaction created', 'User can not create transactions!!!'
    # get
    get_transaction = requests.get(url=f'{URL}wallets/transactions/{wallets_data[1]}/', headers=header)
    assert get_transaction.status_code == 200, 'User can not get detail data about transaction'
    # update
    update_transaction = requests.put(url=f'{URL}wallets/transactions/{wallets_data[1]}/', headers=header)
    assert update_transaction.status_code == 405, 'User should not have access to update data'
    assert update_transaction.json()['detail'] == 'Method "PUT" not allowed.', 'This method should not be allowed'
    # delete
    delete_transaction = requests.delete(url=f'{URL}wallets/transactions/{wallets_data[1]}/', headers=header)
    assert delete_transaction.status_code == 405, 'User should not have access to delete data'
    assert delete_transaction.json()['detail'] == 'Method "DELETE" not allowed.', 'This method should not be allowed'
