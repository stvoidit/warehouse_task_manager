import hashlib
import hmac
import random
from datetime import date, datetime, timedelta

import jwt
import pytz


class CryptoGuard():
    secret: bytes
    def __init__(self, secret: str) -> None:
        self.secret = secret.encode()
        self.tz = pytz.timezone("Europe/Moscow")

    def generate_password(self, length=20):
        """ генерация пароля """
        alpha = [
            chr(33), chr(35), chr(37), chr(38), chr(42), chr(64),
            *[chr(i) for i in range(65, 90)],
            *[chr(i) for i in range(97, 122)],
        ]
        return "".join(random.choices(alpha, k=length))

    def hash_password( self, password: str):
        """ хэширование пароля """
        return hmac.new(self.secret, password.encode(), hashlib.sha256).hexdigest()

    def create_jwt(self, payload: dict):
        """
            создание jwt токена

            Токен генерируется сроком до полуночи, после этого он станет не валидным.
        """
        exp = datetime.combine(date.today() + timedelta(days=1), datetime.min.time())
        base_message = {
            "iss": "domain.local",
            "sub": "user-token",
            "exp": self.tz.localize(exp),
            "payload": payload
        }
        return jwt.encode(base_message, self.secret, algorithm="HS256")

    def validate_jwt(self, token: str) -> dict[str, any]:
        """
            валидация jwt токена

            В случае, если токен просрочен или не проходит проверку подписи, будет поднята ошибка.
            В случае прохождения валидации возвращается декодированные данные токена.
        """
        return jwt.decode(token, self.secret, leeway=timedelta(seconds=10), algorithms=["HS256"])
