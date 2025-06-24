from src.expon.profile.domain.model.aggregates.user_profile import UserProfile
from src.expon.profile.infrastructure.persistence.jpa.models.user_profile_orm import UserProfileORM

def to_domain(model: UserProfileORM) -> UserProfile:
    return UserProfile(
        id=model.id,
        user_id=model.user_id,
        full_name=model.full_name,
        university=model.university,
        career=model.career,
        first_name=model.first_name,
        last_name=model.last_name,
        gender=model.gender,
        profile_picture=model.profile_picture,
        preferred_presentation=model.preferred_presentation
    )

def to_orm(domain: UserProfile) -> UserProfileORM:
    return UserProfileORM(
        id=domain.id,
        user_id=domain.user_id,
        full_name=domain.full_name,
        university=domain.university,
        career=domain.career,
        first_name=domain.first_name,
        last_name=domain.last_name,
        gender=domain.gender,
        profile_picture=domain.profile_picture,
        preferred_presentation=domain.preferred_presentation
    )
