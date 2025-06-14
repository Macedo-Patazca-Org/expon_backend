import jwt
from datetime import datetime, timedelta
from src.expon.iam.domain.model.aggregates.user import User
from decouple import config  # usa python-decouple para leer tu .env

class TokenService:
    SECRET_KEY = config("JWT_SECRET_KEY", default="secret")  # asegúrate que esté en .env
    ALGORITHM = "HS256"
    EXPIRE_MINUTES = 60

    @classmethod
    def generate_token(cls, user: User) -> str:
        payload = {
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(minutes=cls.EXPIRE_MINUTES)
        }
        return jwt.encode(payload, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def decode_token(cls, token: str) -> dict | None:
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
