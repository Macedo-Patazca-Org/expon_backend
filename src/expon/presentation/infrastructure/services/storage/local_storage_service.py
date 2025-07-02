import os
from fastapi import UploadFile
from uuid import uuid4
from pathlib import Path
import shutil

class LocalStorageService:
    def __init__(self, base_path: str = "storage/audio"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def save(self, file: UploadFile) -> str:
        
        filename = f"{uuid4()}_{file.filename}"
        file_path = os.path.join(self.base_path, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path
