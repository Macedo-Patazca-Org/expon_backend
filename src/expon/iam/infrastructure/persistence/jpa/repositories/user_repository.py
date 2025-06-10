from sqlalchemy.orm import Session
from src.expon.iam.infrastructure.persistence.jpa.entities.user_entity import UserEntity
from src.expon.iam.domain.model.aggregates.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, user: User) -> User:
        entity = UserEntity(
            id=user.id,
            username=user.username,
            email=user.email,
            password=user.password,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return user

    def find_by_email(self, email: str) -> User | None:
        entity = self.db.query(UserEntity).filter_by(email=email).first()
        if not entity:
            return None
        return User(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            password=entity.password,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
