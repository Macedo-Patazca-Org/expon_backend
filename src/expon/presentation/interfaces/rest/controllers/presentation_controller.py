from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from src.expon.shared.infrastructure.dependencies import get_db
from src.expon.iam.infrastructure.authorization.sfs.auth_bearer import get_current_user
from src.expon.presentation.application.internal.commandservices.audio_upload_service import AudioUploadService
from src.expon.presentation.infrastructure.persistence.jpa.repositories.presentation_repository import PresentationRepository
from src.expon.presentation.infrastructure.services.storage.local_storage_service import LocalStorageService
from src.expon.presentation.domain.services.transcription_service import TranscriptionService
from src.expon.presentation.domain.services.sentiment_analysis_service import SentimentAnalysisService
from io import BytesIO
from starlette.datastructures import UploadFile as StarletteUploadFile


router = APIRouter(prefix="/presentations", tags=["Presentations"])

@router.post("/upload")
def upload_presentation(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        contents = file.file.read()
        if not contents:
            return {"success": False, "message": "El archivo está vacío."}
        file.file.seek(0)  # Rebobina para que pueda ser leído por los servicios

        # Crear instancias de los servicios
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

        return {
            "success": True,
            "message": "Transcripción y análisis completados correctamente",
            "data": {
                "transcript": presentation.transcript,
                "dominant_emotion": presentation.dominant_emotion,
                "emotion_probabilities": presentation.emotion_probabilities,
                "confidence": presentation.confidence,
                "filename": presentation.filename,
                "metadata": {
                    "duration": presentation.metadata.duration,
                    "sample_rate": presentation.metadata.sample_rate,
                    "language": presentation.metadata.language
                },
                "created_at": presentation.created_at.isoformat()
            }
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error al procesar el archivo: {str(e)}"
        }
