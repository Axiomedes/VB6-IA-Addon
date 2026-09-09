import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from app.core.config import settings
from app.providers.ollama_provider import OllamaProvider
from app.providers.openrouter_provider import OpenRouterProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.groq_provider import GroqProvider
from app.providers.openai_provider import OpenAIProvider
from app.providers.claude_provider import ClaudeProvider

router = APIRouter()

providers_map = {
    "ollama": OllamaProvider(),
    "openrouter": OpenRouterProvider(),
    "gemini": GeminiProvider(),
    "groq": GroqProvider(),
    "openai": OpenAIProvider(),
    "claude": ClaudeProvider()
}

class ConfigUpdateRequest(BaseModel):
    ollama_host: Optional[str] = None
    openrouter_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

class ProviderTestRequest(BaseModel):
    api_key: Optional[str] = None
    host: Optional[str] = None
    model: Optional[str] = None

@router.get("/config")
async def get_config():
    return {
        "success": True,
        "ollama_host": settings.OLLAMA_HOST,
        "openrouter_api_key": settings.OPENROUTER_API_KEY,
        "groq_api_key": settings.GROQ_API_KEY,
        "gemini_api_key": settings.GEMINI_API_KEY,
        "openai_api_key": settings.OPENAI_API_KEY,
        "anthropic_api_key": settings.ANTHROPIC_API_KEY,
        "has_openrouter": bool(settings.OPENROUTER_API_KEY),
        "has_groq": bool(settings.GROQ_API_KEY),
        "has_gemini": bool(settings.GEMINI_API_KEY),
        "has_openai": bool(settings.OPENAI_API_KEY),
        "has_claude": bool(settings.ANTHROPIC_API_KEY),
        "version": settings.SERVICE_VERSION
    }

@router.post("/config")
async def update_config(req: ConfigUpdateRequest):
    updates = {}
    if req.ollama_host is not None:
        updates["OLLAMA_HOST"] = req.ollama_host
    if req.openrouter_api_key is not None:
        updates["OPENROUTER_API_KEY"] = req.openrouter_api_key
    if req.groq_api_key is not None:
        updates["GROQ_API_KEY"] = req.groq_api_key
    if req.gemini_api_key is not None:
        updates["GEMINI_API_KEY"] = req.gemini_api_key
    if req.openai_api_key is not None:
        updates["OPENAI_API_KEY"] = req.openai_api_key
    if req.anthropic_api_key is not None:
        updates["ANTHROPIC_API_KEY"] = req.anthropic_api_key

    settings.save_env(updates)
    return {
        "success": True,
        "message": "Configuración guardada y recargada correctamente."
    }

@router.get("/providers/{provider}/models")
async def get_provider_models(provider: str):
    p_key = provider.lower().replace(" (local)", "").replace("google ", "").replace("anthropic ", "")
    p_inst = providers_map.get(p_key)
    if not p_inst:
        raise HTTPException(status_code=404, detail=f"Proveedor '{provider}' no reconocido.")

    models = await p_inst.get_models()
    return {
        "success": True,
        "provider": p_key,
        "models": models
    }

@router.post("/providers/{provider}/test")
async def test_provider_connection(provider: str, req: ProviderTestRequest):
    p_key = provider.lower().replace(" (local)", "").replace("google ", "").replace("anthropic ", "")
    api_key = req.api_key or ""
    
    # 1. Ollama
    if p_key == "ollama":
        host = req.host or settings.OLLAMA_HOST
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get(f"{host}/api/tags")
                if r.status_code == 200:
                    models = [m.get("name") for m in r.json().get("models", [])]
                    return {"success": True, "message": f"Conexión exitosa a Ollama ({len(models)} modelos detectados)", "models": models}
                return {"success": False, "message": f"Ollama respondió con código HTTP {r.status_code}"}
        except Exception as e:
            return {"success": False, "message": f"No se pudo conectar con Ollama en {host}: {str(e)}"}

    # 2. OpenRouter
    elif p_key == "openrouter":
        key = api_key or settings.OPENROUTER_API_KEY
        if not key:
            return {"success": False, "message": "API Key no proporcionada."}
        headers = {"Authorization": f"Bearer {key}"}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.get("https://openrouter.ai/api/v1/auth/key", headers=headers)
                if r.status_code == 200:
                    # fetch free models
                    r_m = await client.get("https://openrouter.ai/api/v1/models", headers=headers)
                    free_m = []
                    if r_m.status_code == 200:
                        free_m = [m["id"] for m in r_m.json().get("data", []) if ":free" in m["id"] or m.get("pricing", {}).get("prompt") == "0"]
                    return {
                        "success": True,
                        "message": f"API Key de OpenRouter válida. {len(free_m)} modelos gratuitos disponibles.",
                        "models": ["openrouter/free"] + sorted(free_m)
                    }
                return {"success": False, "message": f"Error de autenticación OpenRouter: {r.text}"}
        except Exception as e:
            return {"success": False, "message": f"Error conectando a OpenRouter: {str(e)}"}

    # 3. Gemini
    elif p_key == "gemini":
        key = api_key or settings.GEMINI_API_KEY
        if not key:
            return {"success": False, "message": "API Key no proporcionada."}
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.get(url)
                if r.status_code == 200:
                    models = [m["name"].replace("models/", "") for m in r.json().get("models", []) if "generateContent" in m.get("supportedGenerationMethods", [])]
                    return {
                        "success": True,
                        "message": f"API Key de Google Gemini válida ({len(models)} modelos disponibles).",
                        "models": sorted(models, key=lambda x: ("flash" not in x, "pro" not in x, x))
                    }
                return {"success": False, "message": f"Error de autenticación Gemini (HTTP {r.status_code}): {r.text}"}
        except Exception as e:
            return {"success": False, "message": f"Error conectando a Google Gemini: {str(e)}"}

    # 4. Groq
    elif p_key == "groq":
        key = api_key or settings.GROQ_API_KEY
        if not key:
            return {"success": False, "message": "API Key no proporcionada."}
        headers = {"Authorization": f"Bearer {key}"}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.get("https://api.groq.com/openai/v1/models", headers=headers)
                if r.status_code == 200:
                    models = [m["id"] for m in r.json().get("data", [])]
                    return {"success": True, "message": f"API Key de Groq válida ({len(models)} modelos disponibles).", "models": models}
                return {"success": False, "message": f"Error de autenticación Groq: {r.text}"}
        except Exception as e:
            return {"success": False, "message": f"Error conectando a Groq: {str(e)}"}

    # 5. OpenAI
    elif p_key == "openai":
        key = api_key or settings.OPENAI_API_KEY
        if not key:
            return {"success": False, "message": "API Key no proporcionada."}
        headers = {"Authorization": f"Bearer {key}"}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.get("https://api.openai.com/v1/models", headers=headers)
                if r.status_code == 200:
                    models = [m["id"] for m in r.json().get("data", []) if any(k in m["id"] for k in ["gpt", "o1", "o3"])]
                    return {"success": True, "message": f"API Key de OpenAI válida ({len(models)} modelos detectados).", "models": sorted(models)}
                return {"success": False, "message": f"Error de autenticación OpenAI: {r.text}"}
        except Exception as e:
            return {"success": False, "message": f"Error conectando a OpenAI: {str(e)}"}

    # 6. Claude
    elif p_key == "claude":
        key = api_key or settings.ANTHROPIC_API_KEY
        if not key:
            return {"success": False, "message": "API Key no proporcionada."}
        return {"success": True, "message": "API Key de Anthropic Claude configurada.", "models": ClaudeProvider.MODELS}

    return {"success": False, "message": f"Proveedor '{provider}' no soportado."}
