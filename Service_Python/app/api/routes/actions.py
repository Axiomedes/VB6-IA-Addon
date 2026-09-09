from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.core.diff_engine import lint_vb6_code, compute_diff, clean_markdown_code
from app.core.database import create_action, update_action_status, get_or_create_project
from app.services.backup_service import create_backup_snapshot

router = APIRouter()

class ProposeActionRequest(BaseModel):
    project_vbp: str
    target_file: Optional[str] = ""
    target_procedure: Optional[str] = ""
    original_code: str
    proposed_code: str
    action_type: Optional[str] = "MODIFY_PROCEDURE"
    description: Optional[str] = ""
    conversation_id: Optional[str] = None

class ExecuteActionRequest(BaseModel):
    action_id: str
    project_vbp: str
    target_file: str
    original_code: str
    action_status: Optional[str] = "EXECUTED"

@router.post("/actions/propose")
def propose_action(req: ProposeActionRequest):
    proj = get_or_create_project(req.project_vbp)
    clean_code = clean_markdown_code(req.proposed_code)
    lint_res = lint_vb6_code(clean_code)
    diff_res = compute_diff(req.original_code, clean_code, from_file=req.target_procedure or req.target_file or "Original", to_file="IA_Propuesto")

    target_file_name = req.target_file or (req.target_procedure + ".bas" if req.target_procedure else "ActiveModule.bas")

    action = create_action(
        project_id=proj["id"],
        action_type=req.action_type or "MODIFY_PROCEDURE",
        target_file=target_file_name,
        target_procedure=req.target_procedure,
        risk_level=lint_res["risk_level"],
        diff_unified=diff_res["diff_unified"],
        original_code=req.original_code,
        proposed_code=clean_code,
        description=req.description or "Modificación propuesta por IA",
        conversation_id=req.conversation_id
    )

    return {
        "success": True,
        "action_id": action["id"],
        "risk_level": lint_res["risk_level"],
        "diff_unified": diff_res["diff_unified"],
        "proposed_code_clean": clean_code,
        "lint_errors": lint_res["errors"],
        "lint_warnings": lint_res["warnings"],
        "stats": diff_res["stats"]
    }

@router.post("/actions/execute")
def execute_action(req: ExecuteActionRequest):
    bkp = create_backup_snapshot(
        project_vbp_path=req.project_vbp,
        target_file_rel=req.target_file,
        content_before=req.original_code,
        action_id=req.action_id,
        reason=f"Snapshot previo a ejecución de {req.action_id}"
    )

    updated = update_action_status(req.action_id, req.action_status or "EXECUTED")
    if not updated:
        raise HTTPException(status_code=404, detail="Acción no encontrada para actualizar estado.")

    return {
        "success": True,
        "action_id": req.action_id,
        "status": req.action_status or "EXECUTED",
        "backup": bkp
    }
