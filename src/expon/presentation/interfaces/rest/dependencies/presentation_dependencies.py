from src.expon.presentation.application.internal.commandservices.audio_upload_service import AudioUploadService
from src.expon.presentation.domain.services.transcription_service import TranscriptionService
from src.expon.presentation.domain.services.sentiment_analysis_service import SentimentAnalysisService

# MOCKS temporales
from src.expon.presentation.infrastructure.services.storage.local_storage_service import LocalStorageService
from src.expon.presentation.infrastructure.persistence.jpa.repositories.presentation_repository import PresentationRepository

def get_audio_upload_service() -> AudioUploadService:
    storage_service = LocalStorageService()  # → luego implementaremos
    transcription_service = TranscriptionService()
    sentiment_service = SentimentAnalysisService()
    repository = PresentationRepository()  # → luego implementaremos

    return AudioUploadService(
        storage_service=storage_service,
        transcription_service=transcription_service,
        sentiment_service=sentiment_service,
        repository=repository
    )
