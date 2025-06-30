from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Dict
from src.expon.presentation.domain.model.valueobjects.audio_metadata import AudioMetadata

@dataclass
class Presentation:
    id: UUID
    user_id: UUID
    filename: str
    transcript: str
    dominant_emotion: str  # <- antes era 'sentiment'
    emotion_probabilities: Dict[str, float]  # <- nuevo campo
    confidence: float
    created_at: datetime
    metadata: AudioMetadata
