from src.expon.profile.infrastructure.persistence.jpa.repositories.profile_repository import ProfileRepository
from src.expon.profile.domain.model.aggregates.user_profile import UserProfile

class ProfileCommandService:
    def __init__(self, repository: ProfileRepository):
        self.repository = repository

    def get_profile_by_user(self, user_id):
        return self.repository.get_by_user_id(user_id)

    def update_profile(self, user_id, data: dict):
        existing = self.repository.get_by_user_id(user_id)
        if not existing:
            raise Exception("Profile not found")

        # Actualiza solo los campos presentes en el dict
        for key, value in data.items():
            if hasattr(existing, key):
                setattr(existing, key, value)

        return self.repository.save_or_update(existing)


    def get_all_profiles(self):
        return self.repository.get_all()