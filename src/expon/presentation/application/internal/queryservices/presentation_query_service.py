from typing import List, Optional
from src.expon.presentation.infrastructure.persistence.jpa.repositories.presentation_repository import PresentationRepository
from src.expon.presentation.domain.model.aggregates.presentation import Presentation

class PresentationQueryService:
    def __init__(self, repository: PresentationRepository):
        self.repository = repository

    def get_presentations_by_user(self, user_id: int) -> List[Presentation]:
        return self.repository.get_by_user_id(user_id)

    def get_presentation_by_id_and_user(self, presentation_id: int, user_id: int) -> Optional[Presentation]:
        return self.repository.get_by_id_and_user(presentation_id, user_id)
