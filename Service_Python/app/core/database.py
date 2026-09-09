import os
import sqlite3
import uuid
import datetime
from typing import Optional, List, Dict, Any

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "VB6AI.db")

def get_db_connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Proyectos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        vbp_path TEXT UNIQUE NOT NULL,
        root_dir TEXT NOT NULL,
        created_at TEXT NOT NULL,
        last_accessed_at TEXT
    );
    """)

    try:
        cursor.execute("ALTER TABLE projects ADD COLUMN last_accessed_at TEXT;")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE projects ADD COLUMN root_dir TEXT;")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE projects ADD COLUMN updated_at TEXT;")
    except Exception:
        pass

    # 2. Conversaciones
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        title TEXT NOT NULL,
        provider TEXT NOT NULL,
        model TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
    );
    """)

    # 3. Mensajes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id TEXT PRIMARY KEY,
        conversation_id TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('USER', 'ASSISTANT', 'SYSTEM')),
        content TEXT NOT NULL,
        tokens_estimated INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
    );
    """)

    try:
        cursor.execute("ALTER TABLE messages ADD COLUMN tokens_estimated INTEGER DEFAULT 0;")
    except Exception:
        pass

    # 4. Acciones y Modificaciones de Código
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS actions (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        conversation_id TEXT,
        action_type TEXT NOT NULL CHECK(action_type IN ('MODIFY_PROCEDURE', 'CREATE_COMPONENT', 'REPLACE_MODULE', 'REMOVE_DEAD_CODE')),
        target_file TEXT NOT NULL,
        target_procedure TEXT,
        risk_level TEXT NOT NULL CHECK(risk_level IN ('LOW', 'MEDIUM', 'HIGH')),
        diff_preview TEXT,
        original_code TEXT,
        proposed_code TEXT,
        status TEXT NOT NULL CHECK(status IN ('PROPOSED', 'EXECUTED', 'REJECTED', 'ROLLED_BACK')),
        description TEXT,
        created_at TEXT NOT NULL,
        executed_at TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
        FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE SET NULL
    );
    """)

    for col, ctype in [("target_procedure", "TEXT"), ("original_code", "TEXT"), ("proposed_code", "TEXT"), ("diff_preview", "TEXT")]:
        try:
            cursor.execute(f"ALTER TABLE actions ADD COLUMN {col} {ctype};")
        except Exception:
            pass

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_actions_status ON actions(status);")

    # 5. Backups y Snapshots
    try:
        cursor.execute("ALTER TABLE backups ADD COLUMN backup_file_path TEXT;")
    except Exception:
        pass
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS backups (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        action_id TEXT,
        backup_file_path TEXT NOT NULL,
        sha256 TEXT NOT NULL,
        reason TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
        FOREIGN KEY (action_id) REFERENCES actions(id) ON DELETE SET NULL
    );
    """)

    # 6. Versiones de archivo
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS file_versions (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        file_path TEXT NOT NULL,
        content_before TEXT NOT NULL,
        content_after TEXT NOT NULL,
        hash_sha256 TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()

def get_or_create_project(vbp_path: str, name: Optional[str] = None) -> Dict[str, Any]:
    if not vbp_path:
        vbp_path = "DEFAULT_WORKSPACE.vbp"
    vbp_path = os.path.abspath(vbp_path)
    root_dir = os.path.dirname(vbp_path)
    if not name:
        name = os.path.splitext(os.path.basename(vbp_path))[0]

    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM projects WHERE vbp_path = ?", (vbp_path,))
    row = cursor.fetchone()
    if row:
        cursor.execute("UPDATE projects SET last_accessed_at = ? WHERE id = ?", (now_iso, row["id"]))
        conn.commit()
        cursor.execute("SELECT * FROM projects WHERE id = ?", (row["id"],))
        proj = dict(cursor.fetchone())
        conn.close()
        return proj

    proj_id = f"proj_{uuid.uuid4().hex[:12]}"
    cursor.execute("""
        INSERT INTO projects (id, name, vbp_path, root_dir, created_at, updated_at, last_accessed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (proj_id, name, vbp_path, root_dir, now_iso, now_iso, now_iso))
    conn.commit()
    cursor.execute("SELECT * FROM projects WHERE id = ?", (proj_id,))
    new_proj = dict(cursor.fetchone())
    conn.close()
    return new_proj

def list_projects() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def create_conversation(project_id: str, title: str, provider: str, model: str) -> Dict[str, Any]:
    conv_id = f"conv_{uuid.uuid4().hex[:12]}"
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conversations (id, project_id, title, provider, model, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (conv_id, project_id, title, provider, model, now_iso, now_iso))
    conn.commit()
    cursor.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,))
    res = dict(cursor.fetchone())
    conn.close()
    return res

def list_conversations(project_id: str) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conversations WHERE project_id = ? ORDER BY updated_at DESC", (project_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def add_message(conversation_id: str, role: str, content: str) -> Dict[str, Any]:
    msg_id = f"msg_{uuid.uuid4().hex[:12]}"
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    tokens_est = len(content) // 4
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (id, conversation_id, role, content, tokens_estimated, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (msg_id, conversation_id, role, content, tokens_est, now_iso))
    cursor.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (now_iso, conversation_id))
    conn.commit()
    cursor.execute("SELECT * FROM messages WHERE id = ?", (msg_id,))
    res = dict(cursor.fetchone())
    conn.close()
    return res

def get_messages(conversation_id: str) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC", (conversation_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def create_action(
    project_id: str,
    action_type: str,
    target_file: str,
    risk_level: str,
    diff_unified: str,
    original_code: str,
    proposed_code: str,
    description: str,
    conversation_id: Optional[str] = None,
    target_procedure: Optional[str] = None
) -> Dict[str, Any]:
    action_id = f"act_{uuid.uuid4().hex[:12]}"
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO actions (
            id, project_id, conversation_id, action_type, target_file,
            target_procedure, risk_level, diff_preview, original_code,
            proposed_code, status, description, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PROPOSED', ?, ?)
    """, (
        action_id, project_id, conversation_id, action_type, target_file,
        target_procedure, risk_level, diff_unified, original_code,
        proposed_code, description, now_iso
    ))
    conn.commit()
    cursor.execute("SELECT * FROM actions WHERE id = ?", (action_id,))
    res = dict(cursor.fetchone())
    conn.close()
    return res

def update_action_status(action_id: str, status: str) -> bool:
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE actions 
        SET status = ?, executed_at = CASE WHEN ? = 'EXECUTED' THEN ? ELSE executed_at END
        WHERE id = ?
    """, (status, status, now_iso, action_id))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated

def record_backup(project_id: str, backup_file_path: str, sha256_hash: str, reason: str, action_id: Optional[str] = None) -> str:
    bkp_id = f"bkp_{uuid.uuid4().hex[:12]}"
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO backups (id, project_id, action_id, backup_file_path, backup_folder, reason, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (bkp_id, project_id, action_id, backup_file_path, os.path.dirname(backup_file_path), reason, now_iso))
    conn.commit()
    conn.close()
    return bkp_id
