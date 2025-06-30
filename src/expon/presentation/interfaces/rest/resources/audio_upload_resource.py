from fastapi import APIRouter, UploadFile, File, Depends
from src.expon.presentation.application.internal.commandservices.audio_upload_service import AudioUploadService

router = APIRouter()

# Este endpoint recibe un archivo y lo procesa
@router.post("/upload-audio")
async def upload_audio(
    file: UploadFile = File(...),
    service: AudioUploadService = Depends()
):
    presentation = service.upload_and_analyze(file)
    return {
        "id": str(presentation.id),
        "filename": presentation.filename,
        "transcript": presentation.transcript,
        "dominant_emotion": presentation.dominant_emotion,
        "emotion_probabilities": presentation.emotion_probabilities,
        "confidence": presentation.confidence,
        "metadata": {
            "duration": presentation.metadata.duration,
            "sample_rate": presentation.metadata.sample_rate,
            "language": presentation.metadata.language,
        },
        "created_at": presentation.created_at.isoformat()
    }
