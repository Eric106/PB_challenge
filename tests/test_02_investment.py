import pytest
from tools import new_request, TEST_URL

@pytest.mark.parametrize(
    "user_name, password, data",
    [
        ('masiosare','elextrañoenemigo', dict()),
        ('masiosare','elextrañoenemigo', {'total_investment':20000,'pb_points':1000, 'pay_method':'VISA/MC'}),
        ('masiosare','elextrañoenemigo', {'total_investment':20000,'pb_points':1000, 'pay_method':'SPEI'}),
        ('masiosare','elextrañoenemigo', {'total_investment':None,'pb_points':None, 'pay_method':None}),
        (None, None, dict())
    ]
)
def test_calc_investment(user_name:str, password: str, data: dict):
    url = f'{TEST_URL}/calc_investment'
    login_data = {"user_name":user_name,"password":password}
    login_req : dict = new_request(f'{TEST_URL}/login',login_data, method='POST').json()
    token = login_req.get('token')

    req = new_request(url, data, 'POST', token)
    response : dict = req.json()

    desired_args = ['total_investment','pb_points','pay_method']
    any_param_missing : bool = any([ data.get(arg) == None for arg in desired_args])

    if token == None:
        assert response == {'message': 'Unauthorized'} and req.status_code == 401
    elif any_param_missing:
        assert response == {'message': 'Bad Request'} and req.status_code == 400
    else:
        assert response.get('success') and response.get('investment') != None and req.status_code == 200


@pytest.mark.parametrize(
    "user_name, password, data",
    [
        ('masiosare','elextrañoenemigo', dict()),
        ('masiosare','elextrañoenemigo', {'total_investment':20000,'pb_points':1000, 'pay_method':'VISA/MC'}),
        ('masiosare','elextrañoenemigo', {'total_investment':20000,'pb_points':1000, 'pay_method':'SPEI'}),
        ('masiosare','elextrañoenemigo', {'total_investment':None,'pb_points':None, 'pay_method':None}),
        (None, None, dict())
    ]
)
def test_create_investment(user_name:str, password: str, data: dict):
    url = f'{TEST_URL}/create_investment'
    login_data = {"user_name":user_name,"password":password}
    login_req : dict = new_request(f'{TEST_URL}/login',login_data, method='POST').json()
    token = login_req.get('token')

    req = new_request(url, data, 'POST', token)
    response : dict = req.json()

    desired_args = ['total_investment','pb_points','pay_method']
    any_param_missing : bool = any([ data.get(arg) == None for arg in desired_args])

    if token == None:
        assert response == {'message': 'Unauthorized'} and req.status_code == 401
    elif any_param_missing:
        assert response == {'message': 'Bad Request'} and req.status_code == 400
    else:
        assert response.get('success') and response.get('investment') != None and req.status_code == 200