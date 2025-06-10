from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class User:
    id: UUID
    username: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime
