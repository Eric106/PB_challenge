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

    calc_data : dict = new_request(f'{TEST_URL}/calc_investment', data, 'POST', token).json()
    calc_ok : bool = calc_data.get('investment') != None
    if calc_ok: calc_data = calc_data.get('investment')

    req = new_request(url, calc_data, 'POST', token)
    response : dict = req.json()

    if token == None:
        assert response == {'message': 'Unauthorized'} and req.status_code == 401
    elif not calc_ok:
        assert response == {'message': 'Bad Request'} and req.status_code == 400
    else:
        assert response.get('success') and response.get('investment') != None and req.status_code == 200

@pytest.mark.parametrize(
    "user_name, password, bad_investment_id",
    [
        ('masiosare','elextrañoenemigo',False),
        ('masiosare','elextrañoenemigo',True),
        ('','',False),
        (None, None,False)
    ]
)
def test_get_investment(user_name:str, password: str, bad_investment_id:bool):
    url = f'{TEST_URL}/get_investment'
    login_data = {"user_name":user_name,"password":password}
    login_req : dict = new_request(f'{TEST_URL}/login',login_data, method='POST').json()
    token = login_req.get('token')

    investments_data : dict = new_request(f'{TEST_URL}/get_investments', dict(), 'GET', token).json()
    investments_ok: bool = investments_data.get('investments') != None
    investments : list[dict] = investments_data.get('investments') if investments_ok else []
    investments_ok: bool = len(investments) > 0
    investment : dict = investments[0] if investments_ok else dict()
    investment = {'investment_id':'BAD_ID'} if bad_investment_id else investment

    req = new_request(url, investment, 'GET', token)
    response : dict = req.json()
    
    if token == None:
        assert response == {'message': 'Unauthorized'} and req.status_code == 401
    elif not investments_ok:
        assert response == {'message': 'Bad Request'} and req.status_code == 400
    elif bad_investment_id:
        assert response == {'message': 'Not Found'} and req.status_code == 404
    else:
        assert response.get('success') and response.get('investment') != None and req.status_code == 200


@pytest.mark.parametrize(
    "user_name, password, bad_investment_id",
    [
        ('masiosare','elextrañoenemigo',False),
        ('masiosare','elextrañoenemigo',True),
        ('masiosare','elextrañoenemigo',False),
        ('','',False),
        (None, None,False)
    ]
)

def test_update_investment(user_name:str, password: str, bad_investment_id:bool):
    url = f'{TEST_URL}/update_investment'
    login_data = {"user_name":user_name,"password":password}
    login_req : dict = new_request(f'{TEST_URL}/login',login_data, method='POST').json()
    token = login_req.get('token')

    investments_data : dict = new_request(f'{TEST_URL}/get_investments', dict(), 'GET', token).json()
    investments_ok: bool = investments_data.get('investments') != None
    investments : list[dict] = investments_data.get('investments') if investments_ok else []
    investments_ok: bool = len(investments) > 0
    investment : dict = investments[0] if investments_ok else dict()
    investment = {'investment_id':'BAD_ID'} if bad_investment_id else investment
    investment['pay_method'] = 'VISA/MC' if investment.get('pay_method') != 'VISA/MC' else 'SPEI'

    print(investment)

    req = new_request(url, investment, 'POST', token)
    response : dict = req.json()
    
    if token == None:
        assert response == {'message': 'Unauthorized'} and req.status_code == 401
    elif not investments_ok:
        assert response == {'message': 'Bad Request'} and req.status_code == 400
    elif bad_investment_id:
        assert response == {'message': 'Not Found'} and req.status_code == 404
    else:
        assert response.get('success') and response.get('investment') != None and req.status_code == 200

@pytest.mark.parametrize(
    "user_name, password, bad_investment_id",
    [
        ('masiosare','elextrañoenemigo',False),
        ('masiosare','elextrañoenemigo',True),
        ('masiosare','elextrañoenemigo',False),
        ('','',False),
        (None, None,False)
    ]
)
def test_delete_investment(user_name:str, password: str, bad_investment_id:bool):
    url = f'{TEST_URL}/delete_investment'
    login_data = {"user_name":user_name,"password":password}
    login_req : dict = new_request(f'{TEST_URL}/login',login_data, method='POST').json()
    token = login_req.get('token')

    investments_data : dict = new_request(f'{TEST_URL}/get_investments', dict(), 'GET', token).json()
    investments_ok: bool = investments_data.get('investments') != None
    investments : list[dict] = investments_data.get('investments') if investments_ok else []
    investments_ok: bool = len(investments) > 0
    investment : dict = investments[0] if investments_ok else dict()
    investment = {'investment_id':'BAD_ID'} if bad_investment_id else investment

    req = new_request(url, investment, 'DELETE', token)
    response : dict = req.json()
    
    if token == None:
        assert response == {'message': 'Unauthorized'} and req.status_code == 401
    elif not investments_ok:
        assert response == {'message': 'Bad Request'} and req.status_code == 400
    elif bad_investment_id:
        assert response == {'message': 'Not Found'} and req.status_code == 404
    else:
        assert response.get('success') and response.get('investment') != None and req.status_code == 200