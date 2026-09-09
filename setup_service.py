import os

base_dir = r"d:\Programming\Antigravity\VB6 IA Addon\Service_Python"

os.makedirs(os.path.join(base_dir, "app", "providers"), exist_ok=True)



req_content = """fastapi>=0.110.0

httpx>=0.27.0

"""

# 2. app/core/config.py

from pydantic import BaseModel

class Settings(BaseModel):

    PORT: int = 8765

    DEFAULT_PROVIDER: str = "ollama"

    SERVICE_VERSION: str = "1.0.0"

settings = Settings()



prompt_content = '''VB6_SYSTEM_PROMPT = """Eres un Ingeniero y Arquitecto Senior especializado exclusivamente en Microsoft Visual Basic 6.0 (SP6) y Win32 API.

REGLAS OBLIGATORIAS:

2. NUNCA utilices sintaxis ni caracteristicas de VB.NET (PROHIBIDO: Imports, Namespace, Async, Await, Task, Using, Try...Catch, Console.WriteLine, List(Of T), Dictionary(Of K,V), Linq, StringBuilder).

4. El manejo de errores debe hacerse exclusivamente con 'On Error GoTo EtiquetaError' o 'On Error Resume Next' (local y justificado).

6. Si necesitas llamadas de bajo nivel o red, utiliza declaraciones Win32 API o componentes COM estandar de VB6 (como WinHttp.WinHttpRequest.5.1 o MSXML2.ServerXMLHTTP60).

'''

# 4. app/core/jobs.py

import time

from pydantic import BaseModel

class Job(BaseModel):

    status: str  # PENDING, RUNNING, COMPLETED, FAILED, CANCELLED

    model: str

    error: Optional[str] = None

    updated_at: float = 0.0



    def full_text(self) -> str:



    def __init__(self):



        job_id = f"job_{uuid.uuid4().hex[:10]}"

        job = Job(

            status="PENDING",

            model=model,

            updated_at=now

        self._jobs[job_id] = job



        return self._jobs.get(job_id)

    def append_chunk(self, job_id: str, chunk: str):

        if job and not job.is_cancelled:

            job.status = "RUNNING"



        job = self._jobs.get(job_id)

            job.status = "COMPLETED"



        job = self._jobs.get(job_id)

            job.status = "FAILED"

            job.updated_at = time.time()

    def cancel_job(self, job_id: str):

        if job:

            job.status = "CANCELLED"



"""

# 5. app/providers/base.py

from typing import Dict, Any, List



    @property

    def name(self) -> str:



    async def check_health(self) -> Dict[str, Any]:



    async def get_models(self) -> List[str]:



    async def generate_stream(self, prompt: str, context: str, model: str, job: Job):

"""

# 6. app/providers/ollama_provider.py

import httpx

from app.providers.base import BaseAIProvider

from app.core.vb6_prompt import VB6_SYSTEM_PROMPT



    @property

        return "ollama"

    async def check_health(self) -> Dict[str, Any]:

            async with httpx.AsyncClient(timeout=3.0) as client:

                if r.status_code == 200:

                    models = [m.get("name") for m in data.get("models", [])]

                        "available": True,

                        "models": models

        except Exception as e:

                "available": False,

                "models": []



        health = await self.check_health()



        full_prompt = ""

            full_prompt += f"CONTEXTO DE VISUAL BASIC 6:\\n```vb\\n{context}\\n```\\n\\n"



            "model": model if model else "codellama",

            "system": VB6_SYSTEM_PROMPT,

        }

        try:

                async with client.stream("POST", f"{settings.OLLAMA_HOST}/api/generate", json=payload) as response:

                        job_manager.fail_job(job.id, f"Ollama respondió con código {response.status_code}")



                        if job.is_cancelled:

                        if not line:

                        try:

                            token = chunk_data.get("response", "")

                                job_manager.append_chunk(job.id, token)

                                break

                            continue

            if not job.is_cancelled:



            job_manager.fail_job(job.id, f"Error durante la generación de Ollama: {str(e)}")



health_routes_content = """from fastapi import APIRouter

from app.providers.ollama_provider import OllamaProvider

router = APIRouter()



async def get_health():

    return {

        "service": "VB6 AI Assistant Local Bridge",

        "providers": {

        }

"""

# 8. app/api/routes/chat.py

from pydantic import BaseModel

from app.core.jobs import job_manager



ollama_provider = OllamaProvider()

class ChatStartRequest(BaseModel):

    context: Optional[str] = ""

    model: Optional[str] = "codellama"

@router.post("/chat/start")

    if not req.prompt:





    if req.provider == "ollama" or not req.provider:

            ollama_provider.generate_stream,

            context=req.context or "",

            job=job



        "success": True,

        "status": "RUNNING",

    }

@router.get("/chat/jobs/{job_id}")

    job = job_manager.get_job(job_id)

        raise HTTPException(status_code=404, detail=f"Job {job_id} no encontrado.")

    return {

        "job_id": job.id,

        "text": job.full_text,

        "error": job.error



async def cancel_job(job_id: str):

    if not job:



    return {

        "job_id": job_id,

    }



main_content = """from fastapi import FastAPI

from app.core.config import settings

from app.api.routes.chat import router as chat_router

app = FastAPI(

    version=settings.SERVICE_VERSION,

)

app.add_middleware(

    allow_origins=["*"],

    allow_methods=["*"],

)

app.include_router(health_router, prefix="/api/v1", tags=["Health"])



async def root():

        "service": "VB6 AI Assistant Local Bridge",

        "docs": "/docs"



    import uvicorn

"""

# 10. run_service.bat

title VB6 AI Assistant - Local Service

echo    INICIANDO SERVICIO LOCAL: VB6 AI Assistant (FastAPI)

echo Puerto: 8765

echo Docs:   http://127.0.0.1:8765/docs

python -m uvicorn app.main:app --host 127.0.0.1 --port 8765 --reload

"""

files = {

    "run_service.bat": run_bat,

    "app/core/__init__.py": "",

    "app/core/vb6_prompt.py": prompt_content,

    "app/providers/__init__.py": "",

    "app/providers/ollama_provider.py": ollama_content,

    "app/api/routes/__init__.py": "",

    "app/api/routes/chat.py": chat_routes_content,

}

for rel_path, content in files.items():

    os.makedirs(os.path.dirname(fpath), exist_ok=True)

        f.write(content)

