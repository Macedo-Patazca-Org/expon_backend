from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.datastructures import UploadFile as StarletteUploadFile
from uuid import UUID  # 👈 Agregado

from src.expon.shared.infrastructure.dependencies import get_db
from src.expon.iam.infrastructure.authorization.sfs.auth_bearer import get_current_user

from src.expon.presentation.application.internal.commandservices.audio_upload_service import AudioUploadService
from src.expon.presentation.application.internal.queryservices.presentation_query_service import PresentationQueryService

from src.expon.presentation.infrastructure.persistence.jpa.repositories.presentation_repository import PresentationRepository
from src.expon.presentation.infrastructure.services.storage.local_storage_service import LocalStorageService
from src.expon.presentation.domain.services.transcription_service import TranscriptionService
from src.expon.presentation.domain.services.sentiment_analysis_service import SentimentAnalysisService

from src.expon.presentation.interfaces.rest.responses.presentation_response import (
    PresentationResponse,
    AudioMetadataResponse,
    PresentationSummaryResponse
)

router = APIRouter()


@router.post("/upload", response_model=PresentationResponse)
def upload_presentation(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        contents = file.file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="El archivo está vacío.")
        file.file.seek(0)

        repository = PresentationRepository(db)
        storage_service = LocalStorageService()
        transcription_service = TranscriptionService()
        sentiment_service = SentimentAnalysisService()

        service = AudioUploadService(
            storage_service=storage_service,
            transcription_service=transcription_service,
            sentiment_service=sentiment_service,
            repository=repository
        )

        presentation = service.upload_and_analyze(file, current_user.id)

        return PresentationResponse(
            id=presentation.id,
            transcript=presentation.transcript,
            dominant_emotion=presentation.dominant_emotion,
            emotion_probabilities=presentation.emotion_probabilities,
            confidence=presentation.confidence,
            filename=presentation.filename,
            metadata=AudioMetadataResponse(
                duration=presentation.metadata.duration,
                sample_rate=presentation.metadata.sample_rate,
                language=presentation.metadata.language
            ),
            created_at=presentation.created_at
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")

@router.get("/summary", response_model=list[PresentationSummaryResponse])
def get_presentations_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    repository = PresentationRepository(db)
    query_service = PresentationQueryService(repository)
    presentations = query_service.get_presentations_by_user(current_user.id)

    return [
        PresentationSummaryResponse(
            id=p.id,
            filename=p.filename,
            dominant_emotion=p.dominant_emotion,
            confidence=p.confidence,
            created_at=p.created_at
        ) for p in presentations
    ]

@router.get("/{presentation_id}", response_model=PresentationResponse)
def get_presentation_by_id(
    presentation_id: UUID,  # 👈 Cambiado de int a UUID
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    repository = PresentationRepository(db)
    query_service = PresentationQueryService(repository)
    presentation = query_service.get_presentation_by_id_and_user(presentation_id, current_user.id)

    if presentation is None:
        raise HTTPException(status_code=404, detail="Presentación no encontrada")

    return PresentationResponse(
        id=presentation.id,
        transcript=presentation.transcript,
        dominant_emotion=presentation.dominant_emotion,
        emotion_probabilities=presentation.emotion_probabilities,
        confidence=presentation.confidence,
        filename=presentation.filename,
        metadata=AudioMetadataResponse(
            duration=presentation.metadata.duration,
            sample_rate=presentation.metadata.sample_rate,
            language=presentation.metadata.language
        ),
        created_at=presentation.created_at
    )


