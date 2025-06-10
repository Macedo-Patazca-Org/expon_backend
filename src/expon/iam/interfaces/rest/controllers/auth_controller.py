from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.expon.iam.domain.model.commands.sign_up_command import SignUpCommand
from src.expon.iam.domain.services.user_command_service import UserCommandService
from src.expon.iam.infrastructure.persistence.jpa.repositories.user_repository import UserRepository
from src.expon.iam.infrastructure.hashing.bcrypt.services.hashing_service import HashingService
from src.expon.shared.infrastructure.dependencies import get_db

router = APIRouter()


@router.post("/signup")
def signup(command: SignUpCommand, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    hashing_service = HashingService()
    user_command_service = UserCommandService(user_repository, hashing_service)

    existing_user = user_repository.find_by_email(command.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user = user_command_service.handle_sign_up(command)
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat()
    }
