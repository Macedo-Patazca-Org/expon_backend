from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Commands y modelos
from src.expon.iam.domain.model.commands.sign_up_command import SignUpCommand
from src.expon.iam.domain.model.aggregates.user import User

# Servicios de dominio
from src.expon.iam.application.internal.commandservices.user_command_service import UserCommandService

# Infraestructura: hashing y token
from src.expon.iam.infrastructure.hashing.bcrypt.services.hashing_service import HashingService
from src.expon.iam.infrastructure.tokens.jwt.services.token_service_impl import TokenService

# Infraestructura: repositorio e inyección de dependencias
from src.expon.iam.infrastructure.persistence.jpa.repositories.user_repository import UserRepository
from src.expon.shared.infrastructure.dependencies import get_db

# Middleware JWT
from src.expon.iam.infrastructure.authorization.sfs.auth_bearer import get_current_user

# Esquemas (DTOs REST)
from src.expon.iam.interfaces.rest.schemas.login_request import LoginRequest
from src.expon.iam.interfaces.rest.schemas.auth_response import AuthResponse

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


@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    hashing_service = HashingService()

    user = user_repository.find_by_email(request.email)
    if not user or not hashing_service.verify(request.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = TokenService.generate_token(user)
    return AuthResponse(
        access_token=token,
        token_type="bearer",
        user_id=str(user.id)
    )


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email
    }
