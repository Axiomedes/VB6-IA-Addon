import asyncio
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.core.jobs import job_manager
from app.core.database import get_or_create_project, create_conversation, add_message
from app.providers.ollama_provider import OllamaProvider
from app.providers.openrouter_provider import OpenRouterProvider
from app.providers.groq_provider import GroqProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.openai_provider import OpenAIProvider
from app.providers.claude_provider import ClaudeProvider

router = APIRouter()
ollama_p = OllamaProvider()
openrouter_p = OpenRouterProvider()
groq_p = GroqProvider()
gemini_p = GeminiProvider()
openai_p = OpenAIProvider()
claude_p = ClaudeProvider()

class ChatStartRequest(BaseModel):
    prompt: str
    context: Optional[str] = ""
    provider: Optional[str] = "ollama"
    model: Optional[str] = ""
    project_vbp: Optional[str] = ""
    conversation_id: Optional[str] = None
    language: Optional[str] = "es"

async def _stream_and_persist(provider_instance, prompt: str, context: str, model: str, job, conversation_id: str, language: str = 'es'):
    await provider_instance.generate_stream(prompt=prompt, context=context, model=model, job=job, language=language)
    try:
        if job.status == "COMPLETED" and conversation_id:
            add_message(conversation_id, "ASSISTANT", job.full_text)
    except Exception as ex:
        print(f"[DB ERROR] Error persistiendo respuesta del asistente: {ex}")

@router.post("/chat/start")
async def start_chat(req: ChatStartRequest, background_tasks: BackgroundTasks):
    if not req.prompt:
        raise HTTPException(status_code=400, detail="El prompt no puede estar vacío.")

    prov = (req.provider or "ollama").lower()
    model = req.model or ""
    
    # 1. Obtener o crear conversación en SQLite
    conv_id = req.conversation_id
    if not conv_id:
        proj = get_or_create_project(req.project_vbp)
        title = req.prompt[:40] + "..." if len(req.prompt) > 40 else req.prompt
        conv = create_conversation(proj["id"], title, prov, model)
        conv_id = conv["id"]
        
    # 2. Registrar mensaje del usuario
    try:
        user_msg = req.prompt
        if req.context:
            user_msg = f"{req.prompt}\n\n[Contexto]\n{req.context}"
        add_message(conv_id, "USER", user_msg)
    except Exception as ex:
        print(f"[DB ERROR] Error persistiendo mensaje del usuario: {ex}")
    
    # 3. Crear Job
    job = job_manager.create_job(provider=prov, model=model)

    # 4. Seleccionar proveedor e iniciar streaming con persistencia
    p_inst = ollama_p
    if "openrouter" in prov:
        p_inst = openrouter_p
    elif "groq" in prov:
        p_inst = groq_p
    elif "gemini" in prov:
        p_inst = gemini_p
    elif "openai" in prov:
        p_inst = openai_p
    elif "claude" in prov or "anthropic" in prov:
        p_inst = claude_p

    asyncio.create_task(_stream_and_persist(p_inst, req.prompt, req.context or "", model, job, conv_id, req.language or "es"))

    return {
        "success": True,
        "job_id": job.id,
        "conversation_id": conv_id,
        "status": "RUNNING",
        "message": f"Tarea de generación iniciada con {prov}."
    }

@router.get("/chat/jobs/{job_id}")
async def get_job_status(job_id: str):
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} no encontrado.")

    return {
        "success": True,
        "job_id": job.id,
        "status": job.status,
        "text": job.full_text,
        "is_completed": (job.status in ["COMPLETED", "FAILED", "CANCELLED"]),
        "error": job.error
    }

@router.post("/chat/jobs/{job_id}/cancel")
async def cancel_job(job_id: str):
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} no encontrado.")

    job_manager.cancel_job(job_id)
    return {
        "success": True,
        "job_id": job_id,
        "status": "CANCELLED"
    }
