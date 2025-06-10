from passlib.context import CryptContext


class HashingService:
    def __init__(self):
        # Puedes ajustar el esquema si deseas usar otro algoritmo como argon2
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
