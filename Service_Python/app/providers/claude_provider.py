import json
import httpx
from typing import Dict, Any, List
from app.providers.base import BaseAIProvider
from app.core.config import settings
from app.core.vb6_prompt import get_vb6_system_prompt, VB6_SYSTEM_PROMPT
from app.core.jobs import Job, job_manager

class ClaudeProvider(BaseAIProvider):
    @property
    def name(self) -> str:
        return "claude"

    MODELS = [
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022",
        "claude-3-opus-20240229"
    ]

    async def check_health(self) -> Dict[str, Any]:
        has_key = bool(settings.ANTHROPIC_API_KEY and len(settings.ANTHROPIC_API_KEY) > 5)
        return {
            "available": has_key,
            "message": "Anthropic Claude configurado con API Key." if has_key else "Requiere ANTHROPIC_API_KEY en .env",
            "models": self.MODELS
        }

    async def get_models(self) -> List[str]:
        return self.MODELS

    async def generate_stream(self, prompt: str, context: str, model: str, job: Job, language: str = 'es'):
        if not settings.ANTHROPIC_API_KEY:
            job_manager.fail_job(job.id, "No se encontró ANTHROPIC_API_KEY. Configure su clave en Configuración o en Service_Python/.env")
            return

        full_prompt = ""
        if context:
            full_prompt += f"CONTEXTO DE VISUAL BASIC 6:\n```vb\n{context}\n```\n\n"
        full_prompt += f"SOLICITUD DEL USUARIO:\n{prompt}"

        target_model = model if model else "claude-3-5-sonnet-20241022"
        headers = {
            "x-api-key": settings.ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }

        payload = {
            "model": target_model,
            "max_tokens": 4096,
            "system": get_vb6_system_prompt(language),
            "messages": [
                {"role": "user", "content": full_prompt}
            ],
            "stream": True
        }

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream("POST", "https://api.anthropic.com/v1/messages", headers=headers, json=payload) as response:
                    if response.status_code != 200:
                        err_text = await response.aread()
                        job_manager.fail_job(job.id, f"Claude HTTP {response.status_code}: {err_text.decode('utf-8', 'ignore')}")
                        return

                    async for line in response.aiter_lines():
                        if job.is_cancelled:
                            break
                        if not line or not line.startswith("data: "):
                            continue
                        data_str = line[6:].strip()
                        try:
                            event = json.loads(data_str)
                            event_type = event.get("type", "")
                            if event_type == "content_block_delta":
                                delta = event.get("delta", {})
                                token = delta.get("text", "")
                                if token:
                                    job_manager.append_chunk(job.id, token)
                            elif event_type == "message_stop":
                                break
                        except Exception:
                            continue

            if not job.is_cancelled:
                job_manager.complete_job(job.id)

        except Exception as e:
            job_manager.fail_job(job.id, f"Error Claude: {str(e)}")
