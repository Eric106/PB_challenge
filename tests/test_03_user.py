import pytest
from tools import new_request, TEST_URL

@pytest.mark.parametrize(
    "user_name, password",
    [
        ('masiosare','elextrañoenemigo'),
        (None, None)
    ]
)
def test_delete_user(user_name:str, password: str):
    url = f'{TEST_URL}/delete_user'
    login_data = {"user_name":user_name,"password":password}
    login_req : dict = new_request(f'{TEST_URL}/login',login_data, method='POST').json()
    token = login_req.get('token')

    req = new_request(url, dict(), 'DELETE', token)

    if token == None:
        assert req.json() == {'message': 'Unauthorized'} and req.status_code == 401
    else:
        assert req.json() == {"success":True} and req.status_code == 200