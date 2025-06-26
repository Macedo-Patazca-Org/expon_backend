from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class Feedback(BaseModel):
    id: UUID
    user_id: UUID
    presentation_id: UUID
    general_feedback: str
    language_feedback: str
    confidence_feedback: str
    anxiety_feedback: str
    suggestions: str
    created_at: datetime

    class Config:
        orm_mode = True
