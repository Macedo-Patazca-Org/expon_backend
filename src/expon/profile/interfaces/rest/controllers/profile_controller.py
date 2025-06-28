from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.expon.shared.infrastructure.dependencies import get_db
from src.expon.iam.infrastructure.authorization.sfs.auth_bearer import get_current_user
from src.expon.profile.infrastructure.persistence.jpa.repositories.profile_repository import ProfileRepository
from src.expon.profile.application.internal.commandservices.profile_command_service import ProfileCommandService
from fastapi import HTTPException
from src.expon.profile.domain.model.aggregates.user_profile import UserProfile
from src.expon.profile.interfaces.rest.requests.user_profile_request import UserProfileRequest 

router = APIRouter()

@router.get("/me")
def get_my_profile(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = ProfileCommandService(ProfileRepository(db))
    return service.get_profile_by_user(current_user.id)

@router.put("/me")
def update_my_profile(
    data: UserProfileRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = ProfileCommandService(ProfileRepository(db))
    return service.update_profile(current_user.id, data.dict(exclude_unset=True)) 

@router.post("/me")
def create_my_profile(
    data: UserProfileRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = ProfileCommandService(ProfileRepository(db))

    existing = service.get_profile_by_user(current_user.id)
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")

    profile = UserProfile(
        id=None,
        user_id=current_user.id,
        full_name=data.full_name,
        university=data.university,
        career=data.career,
        first_name=data.first_name,
        last_name=data.last_name,
        gender=data.gender,
        profile_picture=data.profile_picture,
        preferred_presentation=data.preferred_presentation
    )
    return service.repository.save_or_update(profile)


@router.get("/")
def get_all_profiles(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = ProfileCommandService(ProfileRepository(db))
    return service.get_all_profiles()