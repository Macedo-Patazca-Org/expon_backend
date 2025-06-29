from src.expon.presentation.domain.model.aggregates.presentation import Presentation
from src.expon.presentation.domain.model.valueobjects.audio_metadata import AudioMetadata
from src.expon.presentation.infrastructure.persistence.jpa.models.presentation_orm import PresentationORM

class PresentationMapper:

    def to_domain(self, orm: PresentationORM) -> Presentation:
        metadata = AudioMetadata(
            duration=orm.duration,
            sample_rate=orm.sample_rate,
            language=orm.language
        )
        return Presentation(
            id=orm.id,
            user_id=orm.user_id,
            filename=orm.filename,
            transcript=orm.transcript,
            dominant_emotion=orm.dominant_emotion,
            emotion_probabilities=orm.emotion_probabilities,
            confidence=orm.confidence,
            metadata=metadata,
            created_at=orm.created_at
        )

    def to_orm(self, entity: Presentation) -> PresentationORM:
        return PresentationORM(
            id=entity.id,
            user_id=entity.user_id,
            filename=entity.filename,
            transcript=entity.transcript,
            dominant_emotion=entity.dominant_emotion,
            emotion_probabilities=entity.emotion_probabilities,
            confidence=entity.confidence,
            duration=entity.metadata.duration,
            sample_rate=entity.metadata.sample_rate,
            language=entity.metadata.language,
            created_at=entity.created_at
        )
