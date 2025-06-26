from pydantic import BaseModel
from uuid import UUID

class FeedbackRequest(BaseModel):
    presentation_id: UUID
