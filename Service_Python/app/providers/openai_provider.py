import json
import httpx
from typing import Dict, Any, List
from app.providers.base import BaseAIProvider
from app.core.config import settings
from app.core.vb6_prompt import get_vb6_system_prompt, VB6_SYSTEM_PROMPT
from app.core.jobs import Job, job_manager

class OpenAIProvider(BaseAIProvider):
    @property
    def name(self) -> str:
        return "openai"

    MODELS = [
        "gpt-4o-mini",
        "gpt-4o",
        "o3-mini",
        "gpt-4-turbo"
    ]

    async def check_health(self) -> Dict[str, Any]:
        has_key = bool(settings.OPENAI_API_KEY and len(settings.OPENAI_API_KEY) > 5)
        return {
            "available": has_key,
            "message": "OpenAI configurado con API Key." if has_key else "Requiere OPENAI_API_KEY en .env",
            "models": self.MODELS
        }

    async def get_models(self) -> List[str]:
        if not settings.OPENAI_API_KEY:
            return self.MODELS
        try:
            headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.get("https://api.openai.com/v1/models", headers=headers)
                if r.status_code == 200:
                    data = r.json()
                    models = [m["id"] for m in data.get("data", []) if any(k in m["id"] for k in ["gpt", "o1", "o3"])]
                    return sorted(models) if models else self.MODELS
        except Exception:
            pass
        return self.MODELS

    async def generate_stream(self, prompt: str, context: str, model: str, job: Job, language: str = 'es'):
        if not settings.OPENAI_API_KEY:
            job_manager.fail_job(job.id, "No se encontró OPENAI_API_KEY. Configure su clave en Configuración o en Service_Python/.env")
            return

        full_prompt = ""
        if context:
            full_prompt += f"CONTEXTO DE VISUAL BASIC 6:\n```vb\n{context}\n```\n\n"
        full_prompt += f"SOLICITUD DEL USUARIO:\n{prompt}"

        target_model = model if model else "gpt-4o-mini"
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
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
                async with client.stream("POST", "https://api.openai.com/v1/chat/completions", headers=headers, json=payload) as response:
                    if response.status_code != 200:
                        err_text = await response.aread()
                        job_manager.fail_job(job.id, f"OpenAI HTTP {response.status_code}: {err_text.decode('utf-8', 'ignore')}")
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
            job_manager.fail_job(job.id, f"Error OpenAI: {str(e)}")
