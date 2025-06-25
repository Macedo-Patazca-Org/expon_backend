from transformers import pipeline
from typing import Dict
from huggingface_hub import login
import shutil
import os

class SentimentAnalysisService:
    def __init__(self):
        try:
            print("[LOG] Intentando iniciar sesión en Hugging Face...")
            token = os.getenv("HUGGINGFACE_TOKEN")
            if not token:
                raise ValueError("No se encontró HUGGINGFACE_TOKEN en variables de entorno")
            login(token)
            print("[LOG] Sesión iniciada correctamente.")
        except Exception as e:
            print("[ERROR] Falló el login:", e)
            raise

        try:
            print("[LOG] Cargando pipeline...")
            self.pipeline = pipeline(
                "text2text-generation",  # ← importante: este es el task correcto para T5
                model="mrm8488/t5-base-finetuned-emotion"  # ← nombre correcto del modelo
            )
            print("[LOG] Pipeline cargado correctamente.")
        except Exception as e:
            print("[ERROR] Falló la carga del modelo:", e)
            raise

    def analyze(self, transcript: str) -> Dict:
        print("[LOG] Análisis de transcripción recibido.")
        prompt = f"emocion: {transcript}"
        try:
            output = self.pipeline(prompt, max_length=20)
            print("[LOG] Resultado del modelo:", output)
            raw_emotion = output[0]['generated_text'].strip().lower()
        except Exception as e:
            print("[ERROR] Falló la predicción:", e)
            return {
                "dominant_emotion": "error",
                "emotion_probabilities": {},
                "confidence": 0.0
            }

        emotion_mapping = {
            "confianza": "motivado",
            "alegría": "entusiasta",
            "tristeza": "desmotivado",
            "miedo": "ansioso",
            "enfado": "frustrado",
            "amor": "conectado",
            "sorpresa": "sorprendido",
            # etiquetas del modelo (en inglés)
            "joy": "entusiasta",
            "fear": "ansioso",
            "anger": "frustrado",
            "love": "conectado",
            "surprise": "sorprendido",
            "sadness": "desmotivado",
            "trust": "motivado"
        }


        mapped_emotion = emotion_mapping.get(raw_emotion, "desconocido")

        return {
            "dominant_emotion": mapped_emotion,
            "emotion_probabilities": {
                mapped_emotion: 1.0
            },
            "confidence": 1.0
        }
