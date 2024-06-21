
from requests import post, get, delete, Response
import urllib3
from urllib3.connectionpool import InsecureRequestWarning

TEST_URL = 'https://192.168.169.170:65443'


def new_request(url:str, data:dict, method:str, token:str = None) -> Response:
    urllib3.disable_warnings(InsecureRequestWarning)
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    if token == None:
        headers.pop('Authorization')

    if method == 'GET':
        response : Response = get(url, headers=headers, json=data, verify=False)    
    elif method == 'POST':
        response : Response = post(url, headers=headers, json=data, verify=False)    
    elif method == 'DELETE':
        response : Response = delete(url, headers=headers, json=data, verify=False)    
    return response