import requests
from .conftest import URL


def test_get_all_transactions(create_wallets_for_transaction):
    """test for getting all transactions"""
    get_transaction = requests.get(url=f'{URL}wallets/transactions/', headers=create_wallets_for_transaction[1])
    assert get_transaction.status_code == 200, 'User can not get detail data about transaction'


def test_update_transaction(create_wallets_for_transaction):
    """test for update information about transaction, user can't change data"""
    update_transaction = requests.put(url=f'{URL}wallets/transactions/{create_wallets_for_transaction[0][1]}/',
                                      headers=create_wallets_for_transaction[1])
    assert update_transaction.status_code == 405, 'User should not have access to update data'
    assert update_transaction.json()['detail'] == 'Method "PUT" not allowed.', 'This method should not be allowed'


def test_delete_transaction(create_wallets_for_transaction):
    """test for delete transaction, user can't delete transaction"""
    delete_transaction = requests.delete(url=f'{URL}wallets/transactions/{create_wallets_for_transaction[0][1]}/',
                                         headers=create_wallets_for_transaction[1])
    assert delete_transaction.status_code == 405, 'User should not have access to delete data'
    assert delete_transaction.json()['detail'] == 'Method "DELETE" not allowed.', 'This method should not be allowed'
