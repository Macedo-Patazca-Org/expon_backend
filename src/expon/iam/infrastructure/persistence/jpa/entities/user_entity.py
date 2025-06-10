from sqlalchemy import Column, String, DateTime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from src.expon.shared.infrastructure.database import Base


class UserEntity(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
