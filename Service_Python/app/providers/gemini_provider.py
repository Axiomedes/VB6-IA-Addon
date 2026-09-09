import json
import httpx
from typing import Dict, Any, List
from app.providers.base import BaseAIProvider
from app.core.config import settings
from app.core.vb6_prompt import get_vb6_system_prompt, VB6_SYSTEM_PROMPT
from app.core.jobs import Job, job_manager

class GeminiProvider(BaseAIProvider):
    @property
    def name(self) -> str:
        return "gemini"

    MODELS = [
        "gemini-flash-latest",
        "gemini-pro-latest",
        "gemini-3.6-flash",
        "gemini-3.5-flash",
        "gemini-2.5-flash-lite"
    ]

    async def check_health(self) -> Dict[str, Any]:
        has_key = bool(settings.GEMINI_API_KEY and len(settings.GEMINI_API_KEY) > 5)
        models = await self.get_models()
        return {
            "available": has_key,
            "message": "Google Gemini configurado con API Key." if has_key else "Requiere GEMINI_API_KEY en .env",
            "models": models
        }

    async def get_models(self) -> List[str]:
        if not settings.GEMINI_API_KEY:
            return self.MODELS
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={settings.GEMINI_API_KEY}"
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.get(url)
                if r.status_code == 200:
                    data = r.json()
                    models_list = data.get("models", [])
                    gen_models = [m["name"].replace("models/", "") for m in models_list if "generateContent" in m.get("supportedGenerationMethods", [])]
                    if gen_models:
                        # Prioritize flash / pro latest
                        return sorted(gen_models, key=lambda x: ("flash" not in x, "pro" not in x, x))
        except Exception:
            pass
        return self.MODELS

    async def generate_stream(self, prompt: str, context: str, model: str, job: Job, language: str = 'es'):
        if not settings.GEMINI_API_KEY:
            job_manager.fail_job(job.id, "No se encontró GEMINI_API_KEY. Configure su clave en Configuración o en Service_Python/.env")
            return

        sys_prompt = get_vb6_system_prompt(language)
        full_prompt = f"{sys_prompt}\n\n"
        if context:
            full_prompt += f"CONTEXTO DE VISUAL BASIC 6:\n```vb\n{context}\n```\n\n"
        full_prompt += f"SOLICITUD DEL USUARIO:\n{prompt}"

        target_model = model if model else "gemini-flash-latest"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{target_model}:streamGenerateContent?key={settings.GEMINI_API_KEY}&alt=sse"

        payload = {
            "contents": [
                {
                    "parts": [{"text": full_prompt}]
                }
            ]
        }

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream("POST", url, json=payload) as response:
                    if response.status_code != 200:
                        err_text = await response.aread()
                        job_manager.fail_job(job.id, f"Gemini HTTP {response.status_code}: {err_text.decode('utf-8', 'ignore')}")
                        return

                    async for line in response.aiter_lines():
                        if job.is_cancelled:
                            break
                        if not line or not line.startswith("data: "):
                            continue
                        data_str = line[6:].strip()
                        try:
                            chunk = json.loads(data_str)
                            candidates = chunk.get("candidates", [])
                            if candidates:
                                content = candidates[0].get("content", {})
                                parts = content.get("parts", [])
                                for p in parts:
                                    token = p.get("text", "")
                                    if token:
                                        job_manager.append_chunk(job.id, token)
                        except Exception:
                            continue

            if not job.is_cancelled:
                job_manager.complete_job(job.id)

        except Exception as e:
            job_manager.fail_job(job.id, f"Error Gemini: {str(e)}")
