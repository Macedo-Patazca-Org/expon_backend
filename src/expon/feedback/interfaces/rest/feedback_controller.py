from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from src.expon.shared.infrastructure.dependencies import get_db
from src.expon.feedback.interfaces.rest.feedback_request import FeedbackRequest
from src.expon.feedback.interfaces.rest.feedback_response import FeedbackResponse
from src.expon.feedback.infrastructure.persistence.jpa.feedback_repository import FeedbackRepository
from src.expon.presentation.infrastructure.persistence.jpa.repositories.presentation_repository import PresentationRepository
from src.expon.feedback.application.internal.generate_feedback_service import GenerateFeedbackService

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/", response_model=FeedbackResponse)
def generate_feedback(request: FeedbackRequest, db: Session = Depends(get_db)):
    feedback_repo = FeedbackRepository(db)
    presentation_repo = PresentationRepository(db)
    service = GenerateFeedbackService(feedback_repo, presentation_repo)
    result = service.generate_feedback(request.presentation_id)
    return result


@router.get("/user/{user_id}", response_model=list[FeedbackResponse])
def get_feedback_by_user(user_id: UUID, db: Session = Depends(get_db)):
    repo = FeedbackRepository(db)
    results = repo.get_by_user(user_id)
    return results


@router.get("/presentation/{presentation_id}", response_model=list[FeedbackResponse])
def get_feedback_by_presentation(presentation_id: UUID, db: Session = Depends(get_db)):
    repo = FeedbackRepository(db)
    results = repo.get_by_presentation(presentation_id)
    return results
