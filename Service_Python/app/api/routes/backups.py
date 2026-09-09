import os
from fastapi import APIRouter, HTTPException
from typing import Optional
from app.core.database import get_db_connection, get_or_create_project

router = APIRouter()

@router.get("/backups")
def get_backups(project_vbp: Optional[str] = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if project_vbp:
        proj = get_or_create_project(project_vbp)
        cursor.execute("SELECT * FROM backups WHERE project_id = ? ORDER BY created_at DESC", (proj["id"],))
    else:
        cursor.execute("SELECT * FROM backups ORDER BY created_at DESC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return {"success": True, "backups": rows}
