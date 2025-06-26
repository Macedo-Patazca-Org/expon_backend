from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID as SA_UUID
from src.expon.shared.infrastructure.database import Base
import uuid
import datetime

class FeedbackORM(Base):
    __tablename__ = "feedback"

    id = Column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(SA_UUID(as_uuid=True), nullable=False)
    presentation_id = Column(SA_UUID(as_uuid=True), nullable=False)
    general_feedback = Column(String, nullable=False)
    language_feedback = Column(String, nullable=False)
    confidence_feedback = Column(String, nullable=False)
    anxiety_feedback = Column(String, nullable=False)
    suggestions = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
