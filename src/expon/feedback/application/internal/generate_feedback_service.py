from datetime import datetime
from uuid import uuid4
from src.expon.feedback.domain.model.feedback import Feedback
from src.expon.feedback.infrastructure.services.text_generation_service import TextGenerationService
from src.expon.presentation.infrastructure.persistence.jpa.repositories.presentation_repository import PresentationRepository
from src.expon.feedback.infrastructure.persistence.jpa.feedback_repository import FeedbackRepository
from src.expon.presentation.infrastructure.persistence.jpa.models.presentation_orm import PresentationORM

class GenerateFeedbackService:
    def __init__(self, feedback_repo: FeedbackRepository, presentation_repo: PresentationRepository):
        self.feedback_repo = feedback_repo
        self.presentation_repo = presentation_repo
        self.text_gen_service = TextGenerationService()

    def generate_feedback(self, presentation_id: str) -> Feedback:
        # 1. Buscar presentación
        presentation: PresentationORM = self.presentation_repo.get_by_id(presentation_id)

        if presentation is None:
            raise ValueError("Presentación no encontrada")

        user_id = presentation.user_id
        emotion = presentation.dominant_emotion
        transcription = presentation.transcript or ""
        confidence = presentation.confidence or 0.0
        anxiety = 0.3

        # 2. Generar contenido dinámico con IA
        general, language, confidence_fb, anxiety_fb, suggestions = self.text_gen_service.generate_structured_feedback(
            transcription=transcription,
            emotion=emotion,
            confidence=confidence,
            anxiety=anxiety
        )

        feedback = Feedback(
            id=uuid4(),
            user_id=user_id,
            presentation_id=presentation_id,
            general_feedback=general,
            language_feedback=language,
            confidence_feedback=confidence_fb,
            anxiety_feedback=anxiety_fb,
            suggestions=suggestions,
            created_at=datetime.utcnow()
        )

        self.feedback_repo.save(feedback)
        return feedback

