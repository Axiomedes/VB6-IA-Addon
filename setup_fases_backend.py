# -*- coding: utf-8 -*-





db_content = '''import os

import uuid

from typing import Dict, List, Optional, Any

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

DB_PATH = os.path.join(DB_DIR, "VB6AI.db")

def get_db_connection() -> sqlite3.Connection:

    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA journal_mode = WAL;")



    conn = get_db_connection()

    

    CREATE TABLE IF NOT EXISTS projects (

        name TEXT NOT NULL,

        created_at TEXT NOT NULL,

    );

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_projects_vbp_path ON projects(vbp_path);")

    cursor.execute("""

        id TEXT PRIMARY KEY,

        title TEXT NOT NULL,

        model TEXT NOT NULL,

        updated_at TEXT NOT NULL,

    );

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_project ON conversations(project_id);")

    cursor.execute("""

        id TEXT PRIMARY KEY,

        role TEXT NOT NULL CHECK(role IN ('USER', 'ASSISTANT', 'SYSTEM', 'TOOL')),

        raw_payload TEXT,

        created_at TEXT NOT NULL,

    );

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id);")

    cursor.execute("""

        id TEXT PRIMARY KEY,

        project_id TEXT NOT NULL,

        target_file TEXT NOT NULL,

        risk_level TEXT NOT NULL CHECK(risk_level IN ('LOW', 'MEDIUM', 'HIGH')),

        diff_preview TEXT,

        executed_at TEXT,

        FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE SET NULL

    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_actions_status ON actions(status);")

    cursor.execute("""

        id TEXT PRIMARY KEY,

        backup_folder TEXT NOT NULL,

        action_id TEXT,

        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,

    );

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_backups_project ON backups(project_id);")

    cursor.execute("""

        id TEXT PRIMARY KEY,

        project_id TEXT NOT NULL,

        content_before TEXT NOT NULL,

        hash_sha256 TEXT NOT NULL,

        FOREIGN KEY (backup_id) REFERENCES backups(id) ON DELETE CASCADE,

    );

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_file_versions_lookup ON file_versions(project_id, file_path);")

    cursor.execute("""

        key TEXT PRIMARY KEY,

        is_encrypted INTEGER NOT NULL DEFAULT 0,

        updated_at TEXT NOT NULL

    """)

    cursor.execute("""

        id TEXT PRIMARY KEY,

        provider_type TEXT NOT NULL CHECK(provider_type IN ('local', 'cloud')),

        is_enabled INTEGER NOT NULL DEFAULT 1,

        last_ping_ms INTEGER DEFAULT 0

    """)

    conn.commit()



    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def get_or_create_project(vbp_path: str, name: Optional[str] = None) -> Dict[str, Any]:

        vbp_path = "DEFAULT_WORKSPACE"

        name = os.path.splitext(os.path.basename(vbp_path))[0] if vbp_path != "DEFAULT_WORKSPACE" else "Proyecto VB6"

    conn = get_db_connection()

    cursor.execute("SELECT * FROM projects WHERE vbp_path = ?", (vbp_path,))

    

        proj = dict(row)

        return proj

    proj_id = f"proj_{uuid.uuid4().hex[:12]}"

    cursor.execute(

        (proj_id, name, vbp_path, now, now)

    conn.commit()

    return {"id": proj_id, "name": name, "vbp_path": vbp_path, "created_at": now, "updated_at": now}

def list_projects() -> List[Dict[str, Any]]:

    cursor = conn.cursor()

    rows = cursor.fetchall()

    return [dict(r) for r in rows]

def create_conversation(project_id: str, title: str, provider: str, model: str) -> Dict[str, Any]:

    cursor = conn.cursor()

    now = _now()

        "INSERT INTO conversations (id, project_id, title, provider, model, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",

    )

    conn.close()



    conn = get_db_connection()

    cursor.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,))

    conn.close()



    conn = get_db_connection()

    if project_id:

    else:

    rows = cursor.fetchall()

    return [dict(r) for r in rows]

def add_message(conversation_id: str, role: str, content: str, raw_payload: Optional[str] = None, tokens_used: int = 0) -> Dict[str, Any]:

    cursor = conn.cursor()

    now = _now()

        "INSERT INTO messages (id, conversation_id, role, content, raw_payload, tokens_used, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",

    )

    conn.commit()

    return {"id": msg_id, "conversation_id": conversation_id, "role": role.upper(), "content": content, "raw_payload": raw_payload, "tokens_used": tokens_used, "created_at": now}

def get_messages(conversation_id: str) -> List[Dict[str, Any]]:

    cursor = conn.cursor()

    rows = cursor.fetchall()

    return [dict(r) for r in rows]

def create_action(project_id: str, action_type: str, target_file: str, description: str, risk_level: str, diff_preview: str, conversation_id: Optional[str] = None, status: str = "PROPOSED") -> Dict[str, Any]:

    cursor = conn.cursor()

    now = _now()

        """INSERT INTO actions (id, conversation_id, project_id, action_type, target_file, description, risk_level, status, diff_preview, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",

    )

    conn.close()



    conn = get_db_connection()

    now = _now()

    cursor.execute(

        (status.upper(), executed_at, action_id)

    updated = cursor.rowcount > 0

    conn.close()



    conn = get_db_connection()

    cursor.execute("SELECT * FROM actions WHERE id = ?", (action_id,))

    conn.close()



    conn = get_db_connection()

    backup_id = f"bkp_{uuid.uuid4().hex[:12]}"

    cursor.execute(

        (backup_id, project_id, backup_folder, reason, action_id, now)

    conn.commit()

    return {"id": backup_id, "project_id": project_id, "backup_folder": backup_folder, "reason": reason, "action_id": action_id, "created_at": now}

def add_file_version_record(backup_id: str, project_id: str, file_path: str, content_before: str, content_after: Optional[str], hash_sha256: str) -> Dict[str, Any]:

    cursor = conn.cursor()

    now = _now()

        """INSERT INTO file_versions (id, backup_id, project_id, file_path, content_before, content_after, hash_sha256, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",

    )

    conn.close()



    conn = get_db_connection()

    cursor.execute("SELECT * FROM backups WHERE project_id = ? ORDER BY created_at DESC", (project_id,))

    conn.close()



    conn = get_db_connection()

    cursor.execute("SELECT * FROM file_versions WHERE backup_id = ? ORDER BY created_at ASC", (backup_id,))

    conn.close()

'''

# 2. app/core/diff_engine.py

import re



    (r"\\bDim\\s+\\w+\\s+As\\s+New\\s+List\\s*\\(Of\\b", "Colección genérica 'List(Of ...)' no existe en VB6. Use Collection o Arrays."),

    (r"\\bImports\\s+\\w+", "Instrucción 'Imports' es de VB.NET. En VB6 las referencias se configuran en el .vbp."),

    (r"\\bConsole\\.(Write|WriteLine|ReadLine)", "'Console' no existe en VB6 Win32. Use Debug.Print o MsgBox."),

    (r"\\b(OrElse|AndAlso)\\b", "Operadores de cortocircuito 'OrElse' y 'AndAlso' no existen en VB6. Use 'Or' / 'And'."),

    (r"\\bUsing\\s+\\w+\\s+As\\b", "Estructura 'Using' no existe en VB6. Instancie y destruya objetos con 'Set obj = Nothing'."),

    (r"\\.ToString\\s*\\(", "Método '.ToString()' es de .NET. En VB6 use 'CStr()', 'Format$()', o 'Str$()'."),

]

def clean_markdown_code(raw_text: str) -> str:

    if not raw_text:

    

    

    matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

        return max(matches, key=len).strip()

    if text.startswith("```") and text.endswith("```"):

        if len(lines) >= 2:

            



    \"\"\"Analiza el código generado en busca de construcciones incompatibles con VB6.\"\"\"

    errors = []

    for pattern, msg in ANTI_VBDOTNET_PATTERNS:

            errors.append(msg)

    if "Option Explicit" not in code and len(code.splitlines()) > 10:

        

    

        risk_level = "HIGH"

        risk_level = "MEDIUM"

        risk_level = "LOW"

    return {

        "risk_level": risk_level,

        "warnings": warnings



    \"\"\"Calcula diferencias unificadas y estructuradas línea por línea.\"\"\"

    prop_lines = (proposed_code or "").splitlines(keepends=True)

    unified_diff = "".join(difflib.unified_diff(

        prop_lines,

        tofile="Propuesto_IA.cls",

    ))

    matcher = difflib.SequenceMatcher(None, orig_lines, prop_lines)

    added = 0

    modified = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():

            for line in orig_lines[i1:i2]:

        elif tag == 'insert':

                diff_lines.append({"status": "ADDED", "text": line.rstrip("\\r\\n")})

        elif tag == 'delete':

                diff_lines.append({"status": "DELETED", "text": line.rstrip("\\r\\n")})

        elif tag == 'replace':

                diff_lines.append({"status": "DELETED", "text": line.rstrip("\\r\\n")})

            for line in prop_lines[j1:j2]:

                added += 1

            

        "unified_diff": unified_diff,

        "stats": {

            "total_proposed_lines": len(prop_lines),

            "deleted_lines": deleted,

        }

'''

# 3. app/services/__init__.py y app/services/backup_service.py

os.makedirs(services_dir, exist_ok=True)



import hashlib

from typing import Dict, Any, Optional



    return hashlib.sha256(content.encode("utf-8", errors="ignore")).hexdigest()

def create_backup(

    target_file_path: str,

    reason: str,

) -> Dict[str, Any]:

    proj = get_or_create_project(project_vbp_path)

    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    if project_vbp_path and project_vbp_path != "DEFAULT_WORKSPACE" and os.path.exists(os.path.dirname(project_vbp_path)):

        backup_base = os.path.join(proj_dir, ".vb6ai", "backups")

        backup_base = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "backups", proj["id"])

    backup_folder = os.path.join(backup_base, now_str)

    

    backup_file_path = os.path.join(backup_folder, file_name)

    with open(backup_file_path, "w", encoding="utf-8", errors="ignore") as f:

        

    bkp = create_backup_record(proj["id"], backup_folder, reason, action_id)

    

        "success": True,

        "backup_folder": backup_folder,

        "sha256": sha,

    }



actions_route_content = '''from fastapi import APIRouter, HTTPException

from typing import Optional, List, Dict, Any

from app.core.diff_engine import compute_diff, lint_vb6_code, clean_markdown_code





    project_vbp: Optional[str] = ""

    target_procedure: Optional[str] = ""

    proposed_code: str

    description: Optional[str] = "Propuesta de cambio de codigo IA"



    action_id: str

    file_path: Optional[str] = ""

    create_backup: Optional[bool] = True

@router.post("/actions/propose")

    if not req.proposed_code:

        

    validation = lint_vb6_code(clean_code)

    

    action = create_action(

        action_type=req.action_type or "MODIFY_PROCEDURE",

        description=req.description or "Modificacion sugerida por IA",

        diff_preview=diff_data["unified_diff"],

        status="PROPOSED"

    

        "success": True,

        "risk_level": validation["risk_level"],

        "diff_unified": diff_data["unified_diff"],

        "stats": diff_data["stats"],

    }

@router.post("/actions/execute")

    action = get_action(req.action_id)

        raise HTTPException(status_code=404, detail="Accion no encontrada.")

    backup_result = None

        backup_result = create_backup(

            target_file_path=req.file_path or action["target_file"],

            reason=f"Backup automatico previo a ejecucion de accion {req.action_id}",

        )

    update_action_status(req.action_id, "EXECUTED")

    return {

        "action_id": req.action_id,

        "backup": backup_result

'''

# 5. app/api/routes/backups.py

from typing import Optional, List, Dict, Any





async def get_project_backups(vbp_path: str = Query(..., description="Ruta del archivo .vbp del proyecto")):

    backups = list_backups_for_project(proj["id"])

    result = []

        versions = get_file_versions_for_backup(b["id"])

            "backup_id": b["id"],

            "reason": b["reason"],

            "files": [dict(v) for v in versions]

        

        "success": True,

        "backups": result

'''

# 6. app/api/routes/history.py

from pydantic import BaseModel

from app.core.database import (

    list_projects,

    list_conversations,

    get_messages





    project_vbp: Optional[str] = ""

    provider: str



async def get_projects():

    return {"success": True, "projects": projs}

@router.get("/history/conversations")

    project_id = None

        proj = get_or_create_project(vbp_path)

        

    return {"success": True, "conversations": convs}

@router.post("/history/conversations")

    proj = get_or_create_project(req.project_vbp)

    return {"success": True, "conversation": conv}

@router.get("/history/conversations/{conv_id}/messages")

    conv = get_conversation(conv_id)

        raise HTTPException(status_code=404, detail="Conversacion no encontrada.")

    msgs = get_messages(conv_id)

'''

# 7. app/api/routes/chat.py

from fastapi import APIRouter, BackgroundTasks, HTTPException

from typing import Optional

from app.core.database import get_or_create_project, create_conversation, add_message

from app.providers.openrouter_provider import OpenRouterProvider

from app.providers.gemini_provider import GeminiProvider

router = APIRouter()

openrouter_p = OpenRouterProvider()

gemini_p = GeminiProvider()

class ChatStartRequest(BaseModel):

    context: Optional[str] = ""

    model: Optional[str] = ""

    conversation_id: Optional[str] = None

async def _stream_and_persist(provider_instance, prompt: str, context: str, model: str, job, conversation_id: str):

    try:

            add_message(conversation_id, "ASSISTANT", job.full_text)

        print(f"[DB ERROR] Error persistiendo respuesta del asistente: {ex}")

@router.post("/chat/start")

    if not req.prompt:



    model = req.model or ""

    conv_id = req.conversation_id

        proj = get_or_create_project(req.project_vbp)

        conv = create_conversation(proj["id"], title, prov, model)

        

        user_msg = req.prompt

            user_msg = f"{req.prompt}\\n\\n[Contexto]\\n{req.context}"

    except Exception as ex:

    



    if "openrouter" in prov:

    elif "groq" in prov:

    elif "gemini" in prov:





        "success": True,

        "conversation_id": conv_id,

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

'''

# 8. app/main.py

from fastapi.middleware.cors import CORSMiddleware

from app.core.database import init_db

from app.api.routes.chat import router as chat_router

from app.api.routes.backups import router as backups_router





    title="VB6 AI Assistant Local Bridge",

    description="Servicio Local REST para asistencia de IA en Microsoft Visual Basic 6.0"



    CORSMiddleware,

    allow_credentials=True,

    allow_headers=["*"],



app.include_router(chat_router, prefix="/api/v1", tags=["Chat"])

app.include_router(backups_router, prefix="/api/v1", tags=["Backups"])



async def root():

        "service": "VB6 AI Assistant Local Bridge",

        "status": "running",

    }

if __name__ == "__main__":

    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)



    os.path.join(base_dir, "app", "core", "database.py"): db_content,

    os.path.join(base_dir, "app", "services", "__init__.py"): services_init_content,

    os.path.join(base_dir, "app", "api", "routes", "actions.py"): actions_route_content,

    os.path.join(base_dir, "app", "api", "routes", "history.py"): history_route_content,

    os.path.join(base_dir, "app", "main.py"): main_route_content



    with open(path, "w", encoding="utf-8") as f:

    print(f"Created/Updated: {path}")

print("All backend files created successfully!")



    import sys

