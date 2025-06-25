import os
import requests
import time
from tempfile import NamedTemporaryFile

ASSEMBLYAI_API_KEY = "550f6809220c48b29da16e609ab5ae44"
UPLOAD_URL = "https://api.assemblyai.com/v2/upload"
TRANSCRIBE_URL = "https://api.assemblyai.com/v2/transcript"

class TranscriptionService:
    def transcribe(self, file_path: str) -> dict:
        print(f"[DEBUG] Transcribiendo desde archivo: {file_path}")
        if not os.path.exists(file_path):
            raise Exception("Archivo no encontrado para transcripción")

        if os.path.getsize(file_path) == 0:
            raise Exception("El archivo está vacío. Verifica que se haya subido correctamente.")

        try:
            # Paso 1: Subir archivo
            with open(file_path, "rb") as f:
                upload_res = requests.post(
                    UPLOAD_URL,
                    headers={"authorization": ASSEMBLYAI_API_KEY},
                    data=f
                )
            upload_res.raise_for_status()
            audio_url = upload_res.json()["upload_url"]

            # Paso 2: Solicitar transcripción
            transcript_res = requests.post(
                TRANSCRIBE_URL,
                json={"audio_url": audio_url, "language_code": "es"},
                headers={"authorization": ASSEMBLYAI_API_KEY}
            )
            transcript_res.raise_for_status()
            transcript_id = transcript_res.json()["id"]

            # Paso 3: Polling
            while True:
                poll_res = requests.get(f"{TRANSCRIBE_URL}/{transcript_id}", headers={"authorization": ASSEMBLYAI_API_KEY})
                poll_data = poll_res.json()
                if poll_data["status"] == "completed":
                    return {
                        "text": poll_data["text"],
                        "confidence": poll_data.get("confidence", 1.0)
                    }
                elif poll_data["status"] == "error":
                    raise Exception(f"Error en AssemblyAI: {poll_data['error']}")
                time.sleep(3)

        except Exception as e:
            print(f"[ERROR] Error en transcripción: {e}")
            raise
