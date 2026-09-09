import json
import httpx
from typing import Dict, Any, List
from app.providers.base import BaseAIProvider
from app.core.config import settings
from app.core.vb6_prompt import get_vb6_system_prompt, VB6_SYSTEM_PROMPT
from app.core.jobs import Job, job_manager

class OpenRouterProvider(BaseAIProvider):
    @property
    def name(self) -> str:
        return "openrouter"

    FREE_MODELS = [
        "openrouter/free",
        "nvidia/nemotron-3.5-lightning:free",
        "google/gemma-4-31b-it:free",
        "google/gemma-4-26b-a4b-it:free",
        "cohere/north-mini-code:free",
        "poolside/laguna-s-2.1:free",
        "thinkingmachines/inkling:free",
        "liquid/lfm-2.5-2.6b:free",
        "inclusionai/ling-3.0-flash-sante:free"
    ]

    async def check_health(self) -> Dict[str, Any]:
        has_key = bool(settings.OPENROUTER_API_KEY and len(settings.OPENROUTER_API_KEY) > 5)
        models = await self.get_models()
        return {
            "available": has_key,
            "message": "OpenRouter configurado con API Key." if has_key else "Requiere OPENROUTER_API_KEY en .env",
            "models": models
        }

    async def get_models(self) -> List[str]:
        if not settings.OPENROUTER_API_KEY:
            return self.FREE_MODELS
        try:
            headers = {"Authorization": f"Bearer {settings.OPENROUTER_API_KEY}"}
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.get("https://openrouter.ai/api/v1/models", headers=headers)
                if r.status_code == 200:
                    data = r.json()
                    models_list = data.get("data", [])
                    free_m = [m["id"] for m in models_list if ":free" in m["id"] or m.get("pricing", {}).get("prompt") == "0"]
                    if free_m:
                        return ["openrouter/free"] + sorted(free_m)
        except Exception:
            pass
        return self.FREE_MODELS

    async def generate_stream(self, prompt: str, context: str, model: str, job: Job, language: str = 'es'):
        if not settings.OPENROUTER_API_KEY:
            job_manager.fail_job(job.id, "No se encontró OPENROUTER_API_KEY. Configure su clave en Configuración o en Service_Python/.env")
            return

        full_prompt = ""
        if context:
            full_prompt += f"CONTEXTO DE VISUAL BASIC 6:\n```vb\n{context}\n```\n\n"
        full_prompt += f"SOLICITUD DEL USUARIO:\n{prompt}"

        target_model = model if model else "openrouter/free"

        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "HTTP-Referer": "http://127.0.0.1:8765",
            "X-Title": "VB6 AI Assistant",
            "Content-Type": "application/json"
        }

        payload = {
            "model": target_model,
            "messages": [
                {"role": "system", "content": get_vb6_system_prompt(language)},
                {"role": "user", "content": full_prompt}
            ],
            "stream": True
        }

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream("POST", "https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload) as response:
                    if response.status_code != 200:
                        err_text = await response.aread()
                        job_manager.fail_job(job.id, f"OpenRouter HTTP {response.status_code}: {err_text.decode('utf-8', 'ignore')}")
                        return

                    async for line in response.aiter_lines():
                        if job.is_cancelled:
                            break
                        if not line or not line.startswith("data: "):
                            continue
                        data_str = line[6:].strip()
                        if data_str == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data_str)
                            choices = chunk.get("choices", [])
                            if choices:
                                delta = choices[0].get("delta", {})
                                token = delta.get("content", "")
                                if token:
                                    job_manager.append_chunk(job.id, token)
                        except Exception:
                            continue

            if not job.is_cancelled:
                job_manager.complete_job(job.id)

        except Exception as e:
            job_manager.fail_job(job.id, f"Error OpenRouter: {str(e)}")
