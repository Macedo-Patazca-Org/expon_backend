from sqlalchemy.orm import Session
from src.expon.feedback.infrastructure.persistence.jpa.feedback_orm import FeedbackORM
from src.expon.feedback.domain.model.feedback import Feedback
from datetime import datetime
import uuid

class FeedbackRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, feedback: Feedback):
        orm_obj = FeedbackORM(
            id=uuid.uuid4(),
            user_id=feedback.user_id,
            presentation_id=feedback.presentation_id,
            general_feedback=feedback.general_feedback,
            language_feedback=feedback.language_feedback,
            confidence_feedback=feedback.confidence_feedback,
            anxiety_feedback=feedback.anxiety_feedback,
            suggestions=feedback.suggestions,
            created_at=datetime.utcnow()
        )
        self.db.add(orm_obj)
        self.db.commit()

    def get_all(self):
        return self.db.query(FeedbackORM).all()

    def get_by_user(self, user_id):
        return self.db.query(FeedbackORM).filter_by(user_id=user_id).all()

    def get_by_presentation(self, presentation_id):
        return self.db.query(FeedbackORM).filter_by(presentation_id=presentation_id).all()
