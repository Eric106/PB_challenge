import jwt
from pytz import timezone
from datetime import datetime, timedelta
from .config import CONFIG
from .model import User

class Auth_Service:
    
    jwt_key : str = CONFIG.jwt_key
    tz = timezone('America/Mexico_City')

    def get_token(self, user: User) -> str:
        payload : dict = {
            'iat': datetime.now(tz=self.tz),
            'exp': datetime.now(tz=self.tz) + timedelta(minutes=10),
            'user_id': user.user_id,
        }
        return jwt.encode(payload, self.jwt_key, algorithm="HS256")

    def verify_token(self, headers: dict) -> bool:
        return len(self.get_payload(headers).keys()) > 0
    
    def get_payload(self, headers: dict) -> dict:
        if 'Authorization' in headers.keys():
            auth : str = headers['Authorization']
            encoded_token = auth.split(" ")[1]
            if len(encoded_token) > 0:
                try:
                    return jwt.decode(encoded_token, self.jwt_key, algorithms=["HS256"])
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return dict()           
        return dict()