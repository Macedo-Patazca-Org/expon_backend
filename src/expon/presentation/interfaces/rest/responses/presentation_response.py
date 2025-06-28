from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime
from uuid import UUID

class AudioMetadataResponse(BaseModel):
    duration: float
    sample_rate: int
    language: str

class PresentationResponse(BaseModel):
    transcript: str
    dominant_emotion: Optional[str]
    emotion_probabilities: Dict[str, float]
    confidence: float
    filename: str
    metadata: AudioMetadataResponse
    created_at: datetime

class PresentationSummaryResponse(BaseModel):
    id: UUID
    filename: str
    dominant_emotion: str
    confidence: float
    created_at: datetime