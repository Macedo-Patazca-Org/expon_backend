from uuid import uuid4
from datetime import datetime
from src.expon.iam.domain.model.aggregates.user import User
from src.expon.iam.domain.model.commands.sign_up_command import SignUpCommand
from src.expon.iam.infrastructure.persistence.jpa.repositories.user_repository import UserRepository
from src.expon.iam.infrastructure.hashing.bcrypt.services.hashing_service import HashingService


class UserCommandService:
    def __init__(self, user_repository: UserRepository, hashing_service: HashingService):
        self.user_repository = user_repository
        self.hashing_service = hashing_service

    def handle_sign_up(self, command: SignUpCommand) -> User:
        hashed_password = self.hashing_service.hash(command.password)

        user = User(
            id=uuid4(),
            username=command.username,
            email=command.email,
            password=hashed_password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        return self.user_repository.save(user)
