import os
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

class TextGenerationService:
    def __init__(self, model="gemini-1.5-flash"):
        self.model_name = model
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY no encontrada en variables de entorno")
        
        genai.configure(api_key=api_key)
        # Usar modelo sin configuración fija para permitir ajustes dinámicos
        self.model = genai.GenerativeModel(model)

    def generate_structured_feedback(self, transcription: str, emotion: str, confidence: float, anxiety: float) -> tuple[str, str, str, str, str]:
        # Contexto base con información de la presentación
        context = (
            f"ANÁLISIS DE PRESENTACIÓN ACADÉMICA\n"
            f"====================================\n"
            f"Transcripción: \"{transcription}\"\n\n"
            f"Métricas detectadas:\n"
            f"- Emoción dominante: {emotion}\n"
            f"- Nivel de confianza: {int(confidence * 100)}%\n"
            f"- Nivel de ansiedad: {int(anxiety * 100)}%\n"
        )

        def ask(prompt: str) -> str:
            try:
                # Crear el prompt completo con contexto
                full_prompt = f"""Eres un experto en análisis de presentaciones académicas.

{context}

{prompt}

IMPORTANTE: Responde en máximo 60 palabras, de forma directa y profesional, sin usar comillas dobles."""

                # Configuración dinámica como sugiere GPT
                response = self.model.generate_content(
                    full_prompt, 
                    generation_config={
                        "temperature": 0.7, 
                        "max_output_tokens": 100
                    }
                )
                
                # Limpiar caracteres de escape y limitaciones
                clean_text = response.text.strip().replace('\\"', '"').replace('\\n', ' ')
                # Limitar palabras si es muy largo
                words = clean_text.split()
                if len(words) > 60:
                    clean_text = ' '.join(words[:60]) + "..."
                return clean_text
            except Exception as e:
                print(f"Error al generar feedback con Gemini: {e}")
                return f"Error al generar análisis. Verifique la configuración de la API."

        # Pedir feedback por secciones con prompts más específicos
        general = ask("Analiza brevemente la presentación general: fortalezas principales y área de mejora más importante.")
        language = ask("Evalúa el lenguaje: ¿es académico o informal? Menciona 2 mejoras específicas para el vocabulario.")
        confidence_fb = ask("¿Cómo se percibe la confianza del orador? Analiza el tono y seguridad proyectada.")
        anxiety_fb = ask("¿Se detecta ansiedad? Proporciona 2 técnicas específicas para reducirla.")
        suggestions = ask("Lista exactamente 3 mejoras concretas y accionables para futuras presentaciones.")

        return general, language, confidence_fb, anxiety_fb, suggestions
