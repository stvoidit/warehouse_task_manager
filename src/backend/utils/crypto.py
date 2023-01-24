import random
import hmac
import hashlib
import jwt
from datetime import datetime, date, timedelta

class CyptoPassword():
    secret: bytes
    def __init__(self, secret: str) -> None:
        self.secret = secret.encode()

    def generate_password(self, length=20):
        """ генерация пароля """
        alpha = [
            chr(33), chr(35), chr(37), chr(38), chr(42), chr(64),
            *[chr(i) for i in range(65, 90)],
            *[chr(i) for i in range(97, 122)],
        ]
        return "".join(random.choices(alpha, k=length))

    def hash_password( self, password: str):
        return hmac.new(self.secret, password.encode(), hashlib.sha256).hexdigest()

    def create_jwt(self, payload: dict):
        base_message = {
            "iss": "domain.local",
            "sub": "user-token",
            "exp": datetime.combine(date.today() + timedelta(days=1), datetime.min.time()),
            "payload": payload
        }
        print(base_message)
        return jwt.encode(base_message, self.secret, algorithm="HS256")

    def validate_jwt(self, token: str):
        print(jwt.decode(token, self.secret, algorithms=["HS256"]))
