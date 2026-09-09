from fastapi import APIRouter
from typing import Optional
from app.core.database import list_projects, list_conversations, get_messages, get_or_create_project

router = APIRouter()

@router.get("/history/projects")
def get_projects():
    return {"success": True, "projects": list_projects()}

@router.get("/history/conversations")
def get_conversations(project_vbp: Optional[str] = None):
    if project_vbp:
        proj = get_or_create_project(project_vbp)
        return {"success": True, "conversations": list_conversations(proj["id"])}
    return {"success": True, "conversations": []}

@router.get("/history/conversations/{conv_id}/messages")
def get_conv_messages(conv_id: str):
    return {"success": True, "messages": get_messages(conv_id)}
