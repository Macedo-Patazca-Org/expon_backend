from fastapi import FastAPI

# Importar routers (aún no existen, pero dejaré como ejemplo base)
from src.expon.iam.interfaces.rest.controllers.auth_controller import router as auth_router
from src.expon.profile.interfaces.rest.controllers.profile_controller import router as profile_router
from src.expon.presentation.interfaces.rest.controllers.presentation_controller import router as presentation_router
from src.expon.feedback.interfaces.rest.controllers.feedback_controller import router as feedback_router
from src.expon.subscription.interfaces.rest.controllers.subscription_controller import router as subscription_router

app = FastAPI(
    title="Expon Backend API",
    version="1.0.0",
    description="Backend estructurado por bounded contexts con FastAPI"
)

# Incluir routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Autenticación"])
app.include_router(profile_router, prefix="/api/v1/profile", tags=["Perfil"])
app.include_router(presentation_router, prefix="/api/v1/presentation", tags=["Presentaciones"])
app.include_router(feedback_router, prefix="/api/v1/feedback", tags=["Feedback"])
app.include_router(subscription_router, prefix="/api/v1/subscription", tags=["Suscripciones"])

# Ruta raíz temporal
@app.get("/")
def read_root():
    return {"mensaje": "¡Expon backend funcionando con estructura profesional!"}
