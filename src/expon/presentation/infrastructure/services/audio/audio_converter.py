import ffmpeg
import uuid
import os

class AudioConverterService:
    def convert_to_pcm(self, input_path: str) -> str:
        output_path = f"temp_{uuid.uuid4().hex}.wav"
        try:
            (
                ffmpeg
                .input(input_path)
                .output(output_path, ac=1, ar=16000, sample_fmt='s16')
                .overwrite_output()
                .run(quiet=True)
            )
            return output_path
        except ffmpeg.Error as e:
            raise RuntimeError("Error al convertir el archivo a formato PCM 16-bit mono") from e
