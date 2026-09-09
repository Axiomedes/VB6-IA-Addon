import json

import httpx

from typing import Dict, Any, List

from app.providers.base import BaseAIProvider

from app.core.config import settings

from app.core.vb6_prompt import get_vb6_system_prompt, VB6_SYSTEM_PROMPT

from app.core.jobs import Job, job_manager



class GroqProvider(BaseAIProvider):

    @property

    def name(self) -> str:

        return "groq"



    MODELS = [

        "llama-3.3-70b-versatile",

        "llama-3.1-8b-instant",

        "deepseek-r1-distill-llama-70b"

    ]



    async def check_health(self) -> Dict[str, Any]:

        has_key = bool(settings.GROQ_API_KEY and len(settings.GROQ_API_KEY) > 5)

        return {

            "available": has_key,

            "message": "Groq configurado con API Key." if has_key else "Requiere GROQ_API_KEY en .env",

            "models": self.MODELS

        }



    async def get_models(self) -> List[str]:

        return self.MODELS



    async def generate_stream(self, prompt: str, context: str, model: str, job: Job, language: str = 'es'):

        if not settings.GROQ_API_KEY:

            job_manager.fail_job(job.id, "No se encontro GROQ_API_KEY. Configure su clave gratuita de Groq en Service_Python/.env")

            return



        full_prompt = ""

        if context:

            full_prompt += f"CONTEXTO DE VISUAL BASIC 6:\n```vb\n{context}\n```\n\n"

        full_prompt += f"SOLICITUD DEL USUARIO:\n{prompt}"



        target_model = model if model else "llama-3.3-70b-versatile"



        headers = {

            "Authorization": f"Bearer {settings.GROQ_API_KEY}",

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

                async with client.stream("POST", "https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload) as response:

                    if response.status_code != 200:

                        err_text = await response.aread()

                        job_manager.fail_job(job.id, f"Groq HTTP {response.status_code}: {err_text.decode('utf-8', 'ignore')}")

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

            job_manager.fail_job(job.id, f"Error Groq: {str(e)}")

