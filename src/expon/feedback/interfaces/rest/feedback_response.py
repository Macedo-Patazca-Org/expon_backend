from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class FeedbackResponse(BaseModel):
    id: UUID
    user_id: UUID
    presentation_id: UUID
    general_feedback: str
    language_feedback: str
    confidence_feedback: str
    anxiety_feedback: str
    suggestions: str
    created_at: datetime
