# presentation/infrastructure/services/transcription/assemblyai_service.py
import requests
import time

ASSEMBLYAI_API_KEY = "550f6809220c48b29da16e609ab5ae44"
UPLOAD_ENDPOINT = "https://api.assemblyai.com/v2/upload"
TRANSCRIPT_ENDPOINT = "https://api.assemblyai.com/v2/transcript"

headers = {
    "authorization": ASSEMBLYAI_API_KEY
}

def upload_audio(file_path: str) -> str:
    with open(file_path, "rb") as f:
        response = requests.post(UPLOAD_ENDPOINT, headers=headers, files={'file': f})
    response.raise_for_status()
    return response.json()["upload_url"]

def transcribe_audio(upload_url: str) -> dict:
    transcript_request = {
        "audio_url": upload_url,
        "language_code": "es"  # Español
    }
    response = requests.post(TRANSCRIPT_ENDPOINT, json=transcript_request, headers=headers)
    response.raise_for_status()
    transcript_id = response.json()["id"]

    # Polling: esperar hasta que se procese
    while True:
        polling_response = requests.get(f"{TRANSCRIPT_ENDPOINT}/{transcript_id}", headers=headers)
        polling_data = polling_response.json()
        if polling_data["status"] == "completed":
            return polling_data
        elif polling_data["status"] == "error":
            raise Exception(f"Transcripción falló: {polling_data['error']}")
        time.sleep(3)
