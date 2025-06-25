# presentation/infrastructure/services/audio/transcriber_vosk.py
from vosk import Model, KaldiRecognizer
import wave
import json
import os
from audio_converter import convert_to_pcm16_mono

model = Model("models/vosk-model-small-es-0.42")

def transcribe_audio(file_path: str) -> str:
    converted_path = convert_to_pcm16_mono(file_path)

    wf = wave.open(converted_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    result_text = []

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            result_text.append(res.get("text", ""))

    final = json.loads(rec.FinalResult())
    result_text.append(final.get("text", ""))

    wf.close()
    if converted_path != file_path:
        try:
            os.remove(converted_path)
        except Exception:
            pass

    return " ".join(result_text)
