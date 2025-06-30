from dataclasses import dataclass

@dataclass
class AudioMetadata:
    duration: float  # en segundos
    sample_rate: int
    language: str
