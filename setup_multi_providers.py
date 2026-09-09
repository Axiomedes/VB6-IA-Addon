import os

base_dir = r"d:\Programming\Antigravity\VB6 IA Addon\Service_Python"

# 1. app/core/config.py con soporte de .env y API Keys

from pydantic import BaseModel

# Cargar .env manualmente si existe

if os.path.exists(env_path):

        for line in f:

            if line and not line.startswith("#") and "=" in line:

                os.environ[k.strip()] = v.strip().strip('"').strip("'")

class Settings(BaseModel):

    PORT: int = 8765

    

    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    DEFAULT_PROVIDER: str = "ollama"

    SERVICE_VERSION: str = "1.1.0"

settings = Settings()



openrouter_content = """import json

from typing import Dict, Any, List

from app.core.config import settings

from app.core.jobs import Job, job_manager

class OpenRouterProvider(BaseAIProvider):

    def name(self) -> str:



        "deepseek/deepseek-r1:free",

        "qwen/qwen-2.5-coder-32b-instruct:free",

        "google/gemini-2.0-flash-exp:free"



        has_key = bool(settings.OPENROUTER_API_KEY and len(settings.OPENROUTER_API_KEY) > 5)

            "available": has_key,

            "models": self.FREE_MODELS



        return self.FREE_MODELS

    async def generate_stream(self, prompt: str, context: str, model: str, job: Job):

            job_manager.fail_job(job.id, "No se encontro OPENROUTER_API_KEY. Configure su clave gratuita en el archivo Service_Python/.env")



        if context:

        full_prompt += f"SOLICITUD DEL USUARIO:\\n{prompt}"

        target_model = model if model and "/" in model else "deepseek/deepseek-r1:free"

        headers = {

            "HTTP-Referer": "http://127.0.0.1:8765",

            "Content-Type": "application/json"



            "model": target_model,

                {"role": "system", "content": VB6_SYSTEM_PROMPT},

            ],

        }

        try:

                async with client.stream("POST", "https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload) as response:

                        err_text = await response.aread()

                        return

                    async for line in response.aiter_lines():

                            break

                            continue

                        if data_str == "[DONE]":

                        try:

                            choices = chunk.get("choices", [])

                                delta = choices[0].get("delta", {})

                                if token:

                        except Exception:



                job_manager.complete_job(job.id)

        except Exception as e:

"""

# 3. app/providers/groq_provider.py

import httpx

from app.providers.base import BaseAIProvider

from app.core.vb6_prompt import VB6_SYSTEM_PROMPT



    @property

        return "groq"

    MODELS = [

        "llama-3.1-8b-instant",

    ]

    async def check_health(self) -> Dict[str, Any]:

        return {

            "message": "Groq configurado con API Key." if has_key else "Requiere GROQ_API_KEY en .env",

        }

    async def get_models(self) -> List[str]:



        if not settings.GROQ_API_KEY:

            return

        full_prompt = ""

            full_prompt += f"CONTEXTO DE VISUAL BASIC 6:\\n```vb\\n{context}\\n```\\n\\n"





            "Authorization": f"Bearer {settings.GROQ_API_KEY}",

        }

        payload = {

            "messages": [

                {"role": "user", "content": full_prompt}

            "stream": True



            async with httpx.AsyncClient(timeout=120.0) as client:

                    if response.status_code != 200:

                        job_manager.fail_job(job.id, f"Groq HTTP {response.status_code}: {err_text.decode('utf-8', 'ignore')}")



                        if job.is_cancelled:

                        if not line or not line.startswith("data: "):

                        data_str = line[6:].strip()

                            break

                            chunk = json.loads(data_str)

                            if choices:

                                token = delta.get("content", "")

                                    job_manager.append_chunk(job.id, token)

                            continue

            if not job.is_cancelled:



            job_manager.fail_job(job.id, f"Error Groq: {str(e)}")



gemini_content = """import json

from typing import Dict, Any, List

from app.core.config import settings

from app.core.jobs import Job, job_manager

class GeminiProvider(BaseAIProvider):

    def name(self) -> str:



        "gemini-2.0-flash",

        "gemini-1.5-pro"



        has_key = bool(settings.GEMINI_API_KEY and len(settings.GEMINI_API_KEY) > 5)

            "available": has_key,

            "models": self.MODELS



        return self.MODELS

    async def generate_stream(self, prompt: str, context: str, model: str, job: Job):

            job_manager.fail_job(job.id, "No se encontro GEMINI_API_KEY. Configure su clave en Service_Python/.env")



        if context:

        full_prompt += f"SOLICITUD DEL USUARIO:\\n{prompt}"

        target_model = model if model else "gemini-2.0-flash"



            "contents": [

                    "parts": [{"text": full_prompt}]

            ]



            async with httpx.AsyncClient(timeout=120.0) as client:

                    if response.status_code != 200:

                        job_manager.fail_job(job.id, f"Gemini HTTP {response.status_code}: {err_text.decode('utf-8', 'ignore')}")



                        if job.is_cancelled:

                        if not line or not line.startswith("data: "):

                        data_str = line[6:].strip()

                            chunk = json.loads(data_str)

                            if candidates:

                                parts = content.get("parts", [])

                                    token = p.get("text", "")

                                        job_manager.append_chunk(job.id, token)

                            continue

            if not job.is_cancelled:



            job_manager.fail_job(job.id, f"Error Gemini: {str(e)}")



health_content = """from fastapi import APIRouter

from app.providers.ollama_provider import OllamaProvider

from app.providers.groq_provider import GroqProvider



ollama_provider = OllamaProvider()

groq_provider = GroqProvider()



async def get_health():

    openrouter_status = await openrouter_provider.check_health()

    gemini_status = await gemini_provider.check_health()

    return {

        "service": "VB6 AI Assistant Local Bridge",

        "providers": {

            "openrouter": openrouter_status,

            "gemini": gemini_status

    }



chat_content = """from fastapi import APIRouter, BackgroundTasks, HTTPException

from typing import Optional

from app.providers.ollama_provider import OllamaProvider

from app.providers.groq_provider import GroqProvider



ollama_p = OllamaProvider()

groq_p = GroqProvider()



    prompt: str

    provider: Optional[str] = "ollama"



async def start_chat(req: ChatStartRequest, background_tasks: BackgroundTasks):

        raise HTTPException(status_code=400, detail="El prompt no puede estar vacío.")

    prov = (req.provider or "ollama").lower()

    



    if "openrouter" in prov:

    elif "groq" in prov:

    elif "gemini" in prov:

    else:

        background_tasks.add_task(ollama_p.generate_stream, prompt=req.prompt, context=req.context or "", model=model, job=job)

    return {

        "job_id": job.id,

        "message": f"Tarea de generacion iniciada con {prov}."



async def get_job_status(job_id: str):

    if not job:



        "success": True,

        "status": job.status,

        "is_completed": (job.status in ["COMPLETED", "FAILED", "CANCELLED"]),

    }

@router.post("/chat/jobs/{job_id}/cancel")

    job = job_manager.get_job(job_id)

        raise HTTPException(status_code=404, detail=f"Job {job_id} no encontrado.")

    job_manager.cancel_job(job_id)

        "success": True,

        "status": "CANCELLED"

"""

# 7. Plantilla .env

# CONFIGURACIÓN DE PROVEEDORES DE IA (VB6 AI Assistant)



OLLAMA_HOST=http://127.0.0.1:11434

# 2. OpenRouter (Modelos gratuitos como deepseek-r1:free, llama-3.3-70b:free)

OPENROUTER_API_KEY=

# 3. Groq (Ultra-rápido, tier gratuito)

GROQ_API_KEY=

# 4. Google Gemini (Tier gratuito de Google AI Studio)

GEMINI_API_KEY=

# 5. OpenAI (Opcional)

"""

files = {

    "app/providers/openrouter_provider.py": openrouter_content,

    "app/providers/gemini_provider.py": gemini_content,

    "app/api/routes/chat.py": chat_content,

}

for rel_path, content in files.items():

    os.makedirs(os.path.dirname(fpath), exist_ok=True)

        f.write(content)



env_file = os.path.join(base_dir, ".env")

    with open(env_file, "w", encoding="utf-8") as f:

    print("Created .env file template")

