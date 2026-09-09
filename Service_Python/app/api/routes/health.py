from fastapi import APIRouter
from app.core.config import settings
from app.providers.ollama_provider import OllamaProvider
from app.providers.openrouter_provider import OpenRouterProvider
from app.providers.groq_provider import GroqProvider
from app.providers.gemini_provider import GeminiProvider

router = APIRouter()
ollama_p = OllamaProvider()
openrouter_p = OpenRouterProvider()
groq_p = GroqProvider()
gemini_p = GeminiProvider()

@router.get("/health")
async def health_check():
    ollama_status = await ollama_p.check_health()
    return {
        "status": "ONLINE",
        "version": settings.SERVICE_VERSION,
        "default_provider": settings.DEFAULT_PROVIDER,
        "ollama_host": settings.OLLAMA_HOST,
        "ollama_available": ollama_status["available"],
        "models": ollama_status["models"],
        "providers": {
            "ollama": ollama_status,
            "openrouter": await openrouter_p.check_health(),
            "gemini": await gemini_p.check_health(),
            "groq": await groq_p.check_health()
        }
    }
