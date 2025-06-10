from pydantic import BaseModel, EmailStr, Field


class SignUpCommand(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

    class Config:
        arbitrary_types_allowed = True
