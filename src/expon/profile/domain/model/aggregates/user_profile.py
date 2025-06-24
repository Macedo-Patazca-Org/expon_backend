from dataclasses import dataclass
from uuid import UUID
from typing import Optional

@dataclass
class UserProfile:
    id: Optional[UUID]
    user_id: UUID

    full_name: Optional[str]
    university: Optional[str]
    career: Optional[str]

    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[str]
    profile_picture: Optional[str]
    preferred_presentation: Optional[str]
