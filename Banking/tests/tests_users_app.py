from .conftest import USER, PASSWORD, EMAIL, URL, endpoints
import requests


def test_user_sign_up():
    """test for registration user"""
    data = {
        'username': USER,
        'password': PASSWORD,
        'email': EMAIL,
    }
    response = requests.post(url=f'{URL}register/', data=data)
    assert response.status_code == 201, f'Received status code is not equal to 201!!!,\nbut gotten {response.status_code}'
    assert response.json() == {'username': USER, 'email': EMAIL}, 'Received data is not equal!!!'


def test_sign_in():
    """test for login, getting Token"""
    data = {
        'username': USER,
        'password': PASSWORD,
    }
    response = requests.post(url=f'{URL}login/', data=data)
    assert len(response.json()['token']) == 40, 'The length token should be 40!!!'
    assert response.status_code == 200, f'Received status code is not equal to 200!!!,\nbut gotten {response.status_code}'


def test_log_out(sign_in):
    """use fixture to get authToken, and then logout"""
    data = {'Authorization': f'Token {sign_in}'}
    response = requests.post(url=f'{URL}logout/', headers=data)
    assert response.status_code == 200, f'Received status code is not equal to 200!!!,\nbut gotten {response.status_code}'
    assert response.json().get('detail') == "Successfully logged out.", 'The response was unexcepted!!!'


def test_unauthorized_access_to_protected_endpoints():
    """Test unauthorized access to protected endpoints"""

    for endpoint in endpoints:
        response = requests.post(url=f'{URL}{endpoint}')
        assert response.status_code == 401, f'Received status code is not equal to 401!!!,\nbut gotten {response.status_code}'