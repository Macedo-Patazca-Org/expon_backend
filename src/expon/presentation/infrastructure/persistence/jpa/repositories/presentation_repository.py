from sqlalchemy.orm import Session
from src.expon.presentation.domain.model.aggregates.presentation import Presentation
from src.expon.presentation.domain.model.valueobjects.audio_metadata import AudioMetadata
from src.expon.presentation.infrastructure.persistence.jpa.models.presentation_orm import PresentationORM

class PresentationRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, presentation: Presentation) -> None:
        db_model = PresentationORM(
            id=presentation.id,
            user_id=presentation.user_id,
            filename=presentation.filename,
            transcript=presentation.transcript,
            dominant_emotion=presentation.dominant_emotion,
            emotion_probabilities=presentation.emotion_probabilities,
            confidence=presentation.confidence,
            duration=presentation.metadata.duration,
            sample_rate=presentation.metadata.sample_rate,
            language=presentation.metadata.language,
            created_at=presentation.created_at
        )
        self.db.add(db_model)
        self.db.commit()
        # return db_model  # Descomenta si necesitas retornar el objeto guardado
