from sqlalchemy.orm import Session
from uuid import UUID
from src.expon.profile.infrastructure.persistence.jpa.models.user_profile_orm import UserProfileORM
from src.expon.profile.infrastructure.persistence.jpa.mappers.user_profile_mapper import to_domain, to_orm

class ProfileRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: UUID):
        orm = self.db.query(UserProfileORM).filter(UserProfileORM.user_id == user_id).first()
        return to_domain(orm) if orm else None

    def save_or_update(self, domain_profile):
        orm = self.db.query(UserProfileORM).filter(UserProfileORM.user_id == domain_profile.user_id).first()
        if orm:
            orm.full_name = domain_profile.full_name
            orm.university = domain_profile.university
            orm.career = domain_profile.career
            orm.first_name = domain_profile.first_name
            orm.last_name = domain_profile.last_name
            orm.gender = domain_profile.gender
            orm.profile_picture = domain_profile.profile_picture
            orm.preferred_presentation = domain_profile.preferred_presentation
        else:
            orm = to_orm(domain_profile)
            self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return to_domain(orm)
    
    def get_all(self):
        orm_profiles = self.db.query(UserProfileORM).all()
        return [to_domain(orm) for orm in orm_profiles]

