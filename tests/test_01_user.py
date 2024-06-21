import pytest
from tools import new_request, TEST_URL

def test_root():
    req = new_request(TEST_URL, {}, 'GET')
    assert req.json() == {'message': 'hola mundo', 'success': True}

@pytest.mark.parametrize(
    "user_name, password",
    [
        ('masiosare','elextrañoenemigo'),
        ('',''),
        (None, None)
    ]
)
def test_create_user(user_name:str, password: str):
    url = f'{TEST_URL}/create_user'
    if user_name==None and password==None:
        json = dict()
    else:
        json = {"user_name":user_name,"password":password}
    req = new_request(url, json, 'POST')

    if user_name == '' or password == '':
        assert req.json() == {'message': 'Unauthorized'} and req.status_code == 401
    elif user_name==None or password==None:
        assert req.json() == {'message': 'Bad Request'} and req.status_code == 400
    else:
        assert req.json() == {"success":True} and req.status_code == 200

@pytest.mark.parametrize(
    "user_name, password",
    [
        ('masiosare','elextrañoenemigo'),
        ('masiosare',''),
        ('',''),
        (None, None)
    ]
)
def test_login(user_name:str, password: str):
    url = f'{TEST_URL}/login'
    if user_name==None and password==None:
        json = dict()
    else:
        json = {"user_name":user_name,"password":password}

    req = new_request(url, json, 'POST')

    if user_name == '' or password == '':
        assert req.json() == {'message': 'Unauthorized'} and req.status_code == 401
    elif user_name==None or password==None:
        assert req.json() == {'message': 'Bad Request'} and req.status_code == 400
    else:
        response : dict = req.json()
        assert response.get('success') and response.get('token') != None and req.status_code == 200