from pydantic import EmailStr


class GetUserByEmailQuery:
    def __init__(self, email: EmailStr):
        self.email = email
