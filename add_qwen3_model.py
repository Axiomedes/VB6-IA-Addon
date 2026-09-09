import os

# 1. Update OllamaProvider in Service_Python

provider_code = """import json

from typing import Dict, Any, List

from app.core.config import settings

from app.core.jobs import Job, job_manager

class OllamaProvider(BaseAIProvider):

    def name(self) -> str:



        "qwen3:1.7b",

        "hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0",

        "llama3",

        "qwen2.5-coder:7b"



        try:

                r = await client.get(f"{settings.OLLAMA_HOST}/api/tags")

                    data = r.json()

                    # Asegurar que los modelos clave esten en la lista si no estan ya

                    if "qwen3:1.7b" not in models:

                    return {

                        "message": f"Ollama conectado correctamente ({len(installed)} modelos locales detectados).",

                    }

            return {

                "message": f"No se pudo conectar a Ollama en {settings.OLLAMA_HOST}. Asegúrese de que Ollama esté iniciado.",

            }

    async def get_models(self) -> List[str]:

        return health.get("models", self.DEFAULT_FALLBACK_MODELS)

    async def generate_stream(self, prompt: str, context: str, model: str, job: Job):

        if context:

        full_prompt += f"SOLICITUD DEL USUARIO:\\n{prompt}"

        # Resolver modelo objetivo

        

        try:

                r = await client.get(f"{settings.OLLAMA_HOST}/api/tags")

                    tags = [m.get("name") for m in r.json().get("models", [])]

                        # Buscar coincidencias como VB6-IA:latest o Qwen3

                            if "qwen3" in t.lower() or "vb6-ia" in t.lower():

                                break

            pass

        payload = {

            "prompt": full_prompt,

            "stream": True



            async with httpx.AsyncClient(timeout=120.0) as client:

                    if response.status_code != 200:

                        job_manager.fail_job(job.id, f"Ollama respondió con código {response.status_code}: {err_text.decode('utf-8', 'ignore')}")



                        if job.is_cancelled:

                        if not line:

                        try:

                            token = chunk_data.get("response", "")

                                job_manager.append_chunk(job.id, token)

                                break

                            continue

            if not job.is_cancelled:



            job_manager.fail_job(job.id, f"Error durante la generación de Ollama: {str(e)}")



    f.write(provider_code)



config_path = r"d:\Programming\Antigravity\VB6 IA Addon\Service_Python\app\core\config.py"

    cfg = f.read()

with open(config_path, "w", encoding="utf-8") as f:

print("Updated config.py successfully!")

# 3. Update frmAIAssistant.frm with Qwen3:1.7b as the top local model

with open(frm_path, "r", encoding="utf-8") as f:



old_ollama_load = '''    With cboModel

        .AddItem "codellama"

        .AddItem "deepseek-coder:6.7b"

        .ListIndex = 0



        .Clear

        .AddItem "VB6-IA:latest"

        .AddItem "codellama"

        .AddItem "deepseek-coder:6.7b"

        .ListIndex = 0



            cboModel.AddItem "codellama"

            cboModel.AddItem "deepseek-coder:6.7b"

            cboModel.ListIndex = 0'''

new_ollama_click = '''        Case "Ollama (Local)"

            cboModel.AddItem "VB6-IA:latest"

            cboModel.AddItem "codellama"

            cboModel.AddItem "deepseek-coder:6.7b"

            cboModel.ListIndex = 0'''

frm_norm = frm.replace("\r\n", "\n")

frm_norm = frm_norm.replace(old_ollama_click.replace("\r\n", "\n"), new_ollama_click.replace("\r\n", "\n"))

if not frm_crlf.endswith("\r\n"):



    f.write(frm_crlf.encode("utf-8"))

