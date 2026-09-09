import json

import httpx

from typing import Dict, Any, List

from app.providers.base import BaseAIProvider

from app.core.config import settings

from app.core.vb6_prompt import get_vb6_system_prompt, VB6_SYSTEM_PROMPT

from app.core.jobs import Job, job_manager



class OllamaProvider(BaseAIProvider):

    @property

    def name(self) -> str:

        return "ollama"



    DEFAULT_FALLBACK_MODELS = [

        "qwen3:1.7b",

        "VB6-IA:latest",

        "hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0",

        "codellama",

        "llama3",

        "deepseek-coder:6.7b",

        "qwen2.5-coder:7b"

    ]



    async def check_health(self) -> Dict[str, Any]:

        try:

            async with httpx.AsyncClient(timeout=3.0) as client:

                r = await client.get(f"{settings.OLLAMA_HOST}/api/tags")

                if r.status_code == 200:

                    data = r.json()

                    installed = [m.get("name") for m in data.get("models", [])]

                    # Asegurar que los modelos clave esten en la lista si no estan ya

                    models = list(installed)

                    if "qwen3:1.7b" not in models:

                        models.insert(0, "qwen3:1.7b")

                    return {

                        "available": True,

                        "message": f"Ollama conectado correctamente ({len(installed)} modelos locales detectados).",

                        "models": models

                    }

        except Exception as e:

            return {

                "available": False,

                "message": f"No se pudo conectar a Ollama en {settings.OLLAMA_HOST}. Asegúrese de que Ollama esté iniciado.",

                "models": self.DEFAULT_FALLBACK_MODELS

            }



    async def get_models(self) -> List[str]:

        health = await self.check_health()

        return health.get("models", self.DEFAULT_FALLBACK_MODELS)



    async def generate_stream(self, prompt: str, context: str, model: str, job: Job, language: str = 'es'):

        full_prompt = ""

        if context:

            full_prompt += f"CONTEXTO DE VISUAL BASIC 6:\n```vb\n{context}\n```\n\n"

        full_prompt += f"SOLICITUD DEL USUARIO:\n{prompt}"



        # Resolver modelo objetivo

        target_model = model if model else "qwen3:1.7b"

        

        # Si el usuario pidio qwen3:1.7b, verificar si tiene tags locales equivalentes

        try:

            async with httpx.AsyncClient(timeout=3.0) as client:

                r = await client.get(f"{settings.OLLAMA_HOST}/api/tags")

                if r.status_code == 200:

                    tags = [m.get("name") for m in r.json().get("models", [])]

                    if target_model not in tags:

                        # Buscar coincidencias como VB6-IA:latest o Qwen3

                        for t in tags:

                            if "qwen3" in t.lower() or "vb6-ia" in t.lower():

                                target_model = t

                                break

        except Exception:

            pass



        payload = {

            "model": target_model,

            "prompt": full_prompt,

            "system": get_vb6_system_prompt(language),

            "stream": True,

            "options": {

                "num_ctx": 4096

            }

        }



        try:

            async with httpx.AsyncClient(timeout=180.0) as client:

                async with client.stream("POST", f"{settings.OLLAMA_HOST}/api/generate", json=payload) as response:

                    if response.status_code != 200:

                        err_text = await response.aread()

                        job_manager.fail_job(job.id, f"Ollama respondió con código {response.status_code}: {err_text.decode('utf-8', 'ignore')}")

                        return



                    async for line in response.aiter_lines():

                        if job.is_cancelled:

                            break

                        if not line:

                            continue

                        try:

                            chunk_data = json.loads(line)

                            token = chunk_data.get("response", "")

                            if token:

                                job_manager.append_chunk(job.id, token)

                            if chunk_data.get("done", False):

                                break

                        except Exception:

                            continue



            if not job.is_cancelled:

                job_manager.complete_job(job.id)



        except Exception as e:

            job_manager.fail_job(job.id, f"Error durante la generación de Ollama: {str(e)}")

