import os
import shutil
import hashlib
import datetime
from typing import Dict, Any, Optional
from app.core.database import record_backup, get_or_create_project

BACKUP_ROOT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "backups")

def compute_sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8", "ignore")).hexdigest()

def create_backup_snapshot(
    project_vbp_path: str,
    target_file_rel: str,
    content_before: str,
    action_id: Optional[str] = None,
    reason: str = "Pre-modification snapshot"
) -> Dict[str, Any]:
    proj = get_or_create_project(project_vbp_path)
    proj_id = proj["id"]

    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = os.path.join(BACKUP_ROOT_DIR, proj_id, now_str)
    os.makedirs(backup_folder, exist_ok=True)

    safe_filename = os.path.basename(target_file_rel)
    backup_file_path = os.path.join(backup_folder, safe_filename)

    with open(backup_file_path, "w", encoding="utf-8") as f:
        f.write(content_before)

    sha256_hash = compute_sha256(content_before)
    bkp_id = record_backup(
        project_id=proj_id,
        backup_file_path=backup_file_path,
        sha256_hash=sha256_hash,
        reason=reason,
        action_id=action_id
    )

    return {
        "success": True,
        "backup_id": bkp_id,
        "backup_file": backup_file_path,
        "sha256": sha256_hash,
        "created_at": now_str
    }
