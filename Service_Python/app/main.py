from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, chat, actions, history, backups, config
from app.core.config import settings
from app.core.database import init_db

init_db()

app = FastAPI(
    title="VB6 AI Assistant Local Bridge",
    version=settings.SERVICE_VERSION,
    description="FastAPI Local Service for Visual Basic 6.0 AI Assistant"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(actions.router, prefix="/api/v1", tags=["actions"])
app.include_router(history.router, prefix="/api/v1", tags=["history"])
app.include_router(backups.router, prefix="/api/v1", tags=["backups"])
app.include_router(config.router, prefix="/api/v1", tags=["config"])

@app.get("/")
def read_root():
    return {
        "name": "VB6 AI Assistant Bridge",
        "version": settings.SERVICE_VERSION,
        "status": "ONLINE",
        "docs": "/docs"
    }
