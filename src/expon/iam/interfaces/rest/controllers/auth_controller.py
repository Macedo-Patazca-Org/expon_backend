from fastapi import APIRouter

router = APIRouter()

@router.get("/login")
def login_demo():
    return {"mensaje": "Login de prueba funcionando"}
