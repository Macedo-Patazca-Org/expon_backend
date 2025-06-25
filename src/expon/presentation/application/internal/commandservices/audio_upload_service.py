from uuid import UUID, uuid4
from datetime import datetime, timezone
from fastapi import UploadFile
from pydub.utils import mediainfo

from src.expon.presentation.domain.model.aggregates.presentation import Presentation
from src.expon.presentation.domain.model.valueobjects.audio_metadata import AudioMetadata
from src.expon.presentation.domain.services.transcription_service import TranscriptionService
from src.expon.presentation.domain.services.sentiment_analysis_service import SentimentAnalysisService
from src.expon.presentation.infrastructure.persistence.jpa.repositories.presentation_repository import PresentationRepository
from src.expon.presentation.infrastructure.services.storage.local_storage_service import LocalStorageService

import os

class AudioUploadService:
    def __init__(
        self,
        storage_service: LocalStorageService,
        transcription_service: TranscriptionService,
        sentiment_service: SentimentAnalysisService,
        repository: PresentationRepository
    ):
        self.storage_service = storage_service
        self.transcription_service = transcription_service
        self.sentiment_service = sentiment_service
        self.repository = repository

    def upload_and_analyze(self, file: UploadFile, user_id: UUID = UUID("00000000-0000-0000-0000-000000000000")):
        # 1. Guardar archivo original
        file_path = self.storage_service.save(file)

        # 2. Transcribir directamente con AssemblyAI
        result = self.transcription_service.transcribe(file_path)

        transcript = result["text"]
        confidence = result.get("confidence", 1.0)

        # 3. Simular metadata básica (AssemblyAI no devuelve duración ni sample_rate)
        metadata = AudioMetadata(
            duration=0.0,           # Placeholder, se puede estimar si se requiere
            sample_rate=16000,      # Valor asumido estándar
            language="es"
        )

        # 4. Analizar emoción
        emotion_data = self.sentiment_service.analyze(transcript)
        print("[DEBUG] Transcripción exitosa. Texto:", transcript[:50])

        # 5. Crear entidad Presentation
        presentation = Presentation(
            id=uuid4(),
            user_id=user_id,
            filename=file.filename,
            transcript=transcript,
            dominant_emotion=emotion_data["dominant_emotion"],
            emotion_probabilities=emotion_data["emotion_probabilities"],
            confidence=emotion_data["confidence"],
            metadata=metadata,
            created_at=datetime.now(timezone.utc)
        )

        # 6. Guardar en base de datos
        self.repository.save(presentation)

        # 7. Eliminar archivo temporal
        try:
            os.remove(file_path)
        except Exception:
            pass

        return presentation
