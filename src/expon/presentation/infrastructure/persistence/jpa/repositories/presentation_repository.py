from sqlalchemy.orm import Session
from src.expon.presentation.domain.model.aggregates.presentation import Presentation
from src.expon.presentation.domain.model.valueobjects.audio_metadata import AudioMetadata
from src.expon.presentation.infrastructure.persistence.jpa.models.presentation_orm import PresentationORM
from typing import List, Optional
from src.expon.presentation.infrastructure.persistence.jpa.mappers.presentation_mapper import PresentationMapper

class PresentationRepository:
    def __init__(self, db: Session):
        self.db = db
        self.mapper = PresentationMapper()

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
        
    def get_by_id(self, presentation_id: str) -> Optional[PresentationORM]:
        return self.db.query(PresentationORM).filter(PresentationORM.id == presentation_id).first()

    def get_by_user_id(self, user_id: int) -> List[Presentation]:
        entities = self.db.query(PresentationORM).filter_by(user_id=user_id).all()
        return [self.mapper.to_domain(e) for e in entities]

    def get_by_id_and_user(self, presentation_id: int, user_id: int) -> Optional[Presentation]:
        entity = self.db.query(PresentationORM).filter_by(id=presentation_id, user_id=user_id).first()
        return self.mapper.to_domain(entity) if entity else None
