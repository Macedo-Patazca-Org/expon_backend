from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_presentations():
    return {"mensaje": "Lista de presentaciones"}
