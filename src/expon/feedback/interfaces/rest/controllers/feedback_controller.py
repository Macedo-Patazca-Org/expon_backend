from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_feedback():
    return {"mensaje": "Análisis de feedback generado"}
