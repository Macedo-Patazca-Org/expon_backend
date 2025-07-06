from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 👈 nuevo

# routers
from src.expon.iam.interfaces.rest.controllers.auth_controller import router as auth_router
from src.expon.profile.interfaces.rest.controllers.profile_controller import router as profile_router
from src.expon.presentation.interfaces.rest.controllers.presentation_controller import router as presentation_router
from src.expon.feedback.interfaces.rest.feedback_controller import router as feedback_router
from src.expon.subscription.interfaces.rest.controllers.subscription_controller import router as subscription_router
from src.expon.feedback.infrastructure.persistence.jpa.feedback_orm import FeedbackORM
from src.expon.shared.infrastructure.database import Base, engine

app = FastAPI(
    title="Expon Backend API",
    version="1.0.0",
    description="Backend estructurado por bounded contexts con FastAPI"
)

# 👇 middleware CORS
origins = [
    "https://expon-frontend.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(profile_router, prefix="/api/v1/profile", tags=["Profile"])
app.include_router(presentation_router, prefix="/api/v1/presentation", tags=["Presentations"])
app.include_router(feedback_router, prefix="/api/v1/feedback", tags=["Feedback"])
app.include_router(subscription_router, prefix="/api/v1/subscription", tags=["Subscriptions"])

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"mensaje": "¡Expon backend funcionando con estructura profesional!"}
