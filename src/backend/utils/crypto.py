import random
import hmac
import hashlib
import jwt

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
            "exp": None,
            "payload": payload
        }
        return jwt.encode(base_message, self.secret, algorithm="HS256")
