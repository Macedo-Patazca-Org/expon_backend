from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from src.expon.shared.infrastructure.database import Base
from sqlalchemy.dialects.postgresql import JSONB
import datetime

class PresentationORM(Base):
    __tablename__ = "presentations"

    id = Column(PGUUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    filename = Column(String, nullable=False)
    transcript = Column(String, nullable=True)
    dominant_emotion = Column(String, nullable=True)  # <- antes 'sentiment'
    emotion_probabilities = Column(JSONB, nullable=True)  # requiere PostgreSQL
    confidence = Column(Float, nullable=True)

    duration = Column(Float, nullable=True)
    sample_rate = Column(Float, nullable=True)
    language = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
