from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from src.expon.shared.infrastructure.database import Base
import uuid

class UserProfileORM(Base):
    __tablename__ = "user_profiles"

    id = Column(PGUUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)

    full_name = Column(String, nullable=True)
    university = Column(String, nullable=True)
    career = Column(String, nullable=True)

    # Nuevos campos
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)
    preferred_presentation = Column(String, nullable=True)
