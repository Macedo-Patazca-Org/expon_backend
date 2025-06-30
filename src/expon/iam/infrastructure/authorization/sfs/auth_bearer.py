from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from src.expon.iam.infrastructure.tokens.jwt.services.token_service_impl import TokenService
from src.expon.iam.infrastructure.persistence.jpa.repositories.user_repository import UserRepository
from src.expon.shared.infrastructure.dependencies import get_db
from fastapi.security import HTTPAuthorizationCredentials

oauth2_scheme = HTTPBearer()

def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db=Depends(get_db)
):
    payload = TokenService.decode_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    user_id = payload.get("sub")
    user_repo = UserRepository(db)
    user = user_repo.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user