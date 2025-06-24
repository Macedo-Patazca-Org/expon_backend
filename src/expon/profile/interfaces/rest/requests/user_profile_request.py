from pydantic import BaseModel
from typing import Optional

class UserProfileRequest(BaseModel):
    full_name: Optional[str]
    university: Optional[str]
    career: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[str]
    profile_picture: Optional[str]
    preferred_presentation: Optional[str]
