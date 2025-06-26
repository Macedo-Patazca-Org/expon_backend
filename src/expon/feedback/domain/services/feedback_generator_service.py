import re
from typing import Tuple


class FeedbackGeneratorService:

    def analyze_emotion_consistency(self, emotion: str, transcription: str) -> str:
        """
        Evalúa si el contenido de la presentación es coherente con la emoción dominante detectada.
        """
        keywords = {
            "motivado": ["lograr", "puedo", "importante", "avanzar"],
            "ansioso": ["eh", "bueno", "mmm", "no sé", "tal vez"],
            "entusiasta": ["me encanta", "disfruté", "fue genial"],
            "seguro": ["claramente", "sin duda", "obviamente"],
            "inseguro": ["creo", "quizás", "podría ser"]
        }
        palabras = transcription.lower().split()
        count = sum(p in palabras for p in keywords.get(emotion, []))

        if count >= 2:
            return f"La emoción detectada ({emotion}) fue coherente con el contenido del discurso."
        else:
            return f"La emoción detectada ({emotion}) parece no coincidir completamente con lo expresado verbalmente. Podrías trabajar en alinear tu expresión emocional con tus ideas."

    def analyze_language_quality(self, transcription: str) -> str:
        """
        Detecta uso de jerga, muletillas y falta de conectores.
        """
        muletillas = ["eh", "mmm", "bueno", "o sea", "este"]
        jergas = ["chévere", "cool", "super", "bacán"]
        conectores_formales = ["por lo tanto", "además", "en conclusión", "sin embargo"]
        repetidas = set([w for w in transcription.lower().split() if transcription.lower().split().count(w) > 4])

        issues = []

        if any(m in transcription.lower() for m in muletillas):
            issues.append("Se detectaron muletillas frecuentes, como 'eh' o 'bueno'. Esto puede restar claridad.")

        if any(j in transcription.lower() for j in jergas):
            issues.append("El uso de jerga informal no es recomendable en presentaciones académicas.")

        if not any(c in transcription.lower() for c in conectores_formales):
            issues.append("No se identificaron conectores formales. Usarlos ayuda a organizar mejor tus ideas.")

        if len(repetidas) > 0:
            issues.append("Detectamos repetición excesiva de algunas palabras, lo que puede afectar la riqueza del discurso.")

        return " ".join(issues) if issues else "El lenguaje utilizado fue adecuado, claro y apropiado para el contexto académico."

    def evaluate_confidence(self, confidence_score: float) -> str:
        if confidence_score >= 0.8:
            return "Tu nivel de confianza fue alto. Mantuviste un discurso fluido y seguro."
        elif confidence_score >= 0.5:
            return "Confianza aceptable, aunque con espacio para mejorar la entonación o firmeza."
        else:
            return "Bajo nivel de confianza detectado. Practicar la presentación con antelación puede ayudarte a mejorar."

    def evaluate_anxiety(self, anxiety_score: float) -> str:
        if anxiety_score < 0.3:
            return "Se detectó buen control de ansiedad durante tu exposición."
        elif anxiety_score < 0.6:
            return "Ansiedad moderada. Considera técnicas como respiración profunda o pausas conscientes."
        else:
            return "Alta ansiedad percibida. Practica con simulaciones o ensayos en voz alta para mejorar tu seguridad."

    def generate_suggestions(self) -> str:
        return "Prueba practicar en voz alta usando grabaciones. Mejora tu entonación, usa conectores y reduce muletillas."

    def generate_structured_feedback(
        self,
        emotion: str,
        transcription: str,
        confidence_score: float,
        anxiety_score: float
    ) -> Tuple[str, str, str, str, str]:
        """
        Devuelve feedback completo dividido en cinco secciones.
        """
        general = self.analyze_emotion_consistency(emotion, transcription)
        language = self.analyze_language_quality(transcription)
        confidence = self.evaluate_confidence(confidence_score)
        anxiety = self.evaluate_anxiety(anxiety_score)
        suggestions = self.generate_suggestions()

        return general, language, confidence, anxiety, suggestions
