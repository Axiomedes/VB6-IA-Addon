import os
import sys

# Asegurar importación de Service_Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Service_Python"))

from app.core.database import (
    init_db,
    get_or_create_project,
    create_conversation,
    add_message,
    get_messages,
    create_action,
    update_action_status,
    list_projects
)
from app.core.diff_engine import compute_diff, lint_vb6_code, clean_markdown_code
from app.services.backup_service import create_backup_snapshot

def test_full_suite():
    print("=== INICIANDO TEST SUITE DEL BACKEND ===")
    
    # 1. Base de datos SQLite
    print("\n[1/4] Verificando inicialización de SQLite (VB6AI.db)...")
    init_db()
    
    proj = get_or_create_project(r"C:\TestProject\MiApp.vbp", "MiApp")
    assert proj["id"].startswith("proj_"), "Error creando proyecto"
    print(f" -> Proyecto registrado: {proj['name']} ({proj['id']})")
    
    conv = create_conversation(proj["id"], "Consulta de prueba", "ollama", "qwen3:1.7b")
    assert conv["id"].startswith("conv_"), "Error creando conversación"
    print(f" -> Conversación creada: {conv['title']} ({conv['id']})")
    
    msg_u = add_message(conv["id"], "USER", "Hola, refactoriza mi función de ordenamiento.")
    msg_a = add_message(conv["id"], "ASSISTANT", "Entendido, aquí está la optimización en VB6 puro.")
    msgs = get_messages(conv["id"])
    assert len(msgs) >= 2, "Error persistiendo mensajes"
    print(f" -> Mensajes persistidos correctamente: {len(msgs)}")
    
    # 2. Diff Engine y Linter Anti-VB.NET
    print("\n[2/4] Verificando Diff Engine y Linter Anti-VB.NET...")
    orig_code = "Public Sub Sumar(a As Long, b As Long)\n    Dim res As Long\n    res = a + b\nEnd Sub"
    
    # Prueba de código VB.NET inválido
    vbnet_code = "Public Sub Sumar(a As Integer, b As Integer)\n    Dim res = a + b\n    Console.WriteLine(res)\nEnd Sub"
    lint_fail = lint_vb6_code(vbnet_code)
    assert not lint_fail["valid"], "Linter falló al detectar código VB.NET"
    assert len(lint_fail["errors"]) >= 2, "Deben detectarse al menos 2 errores de VB.NET"
    assert lint_fail["risk_level"] == "HIGH", "Riesgo debe ser HIGH para VB.NET"
    print(f" -> Detección Anti-VB.NET OK (Errores detectados: {len(lint_fail['errors'])}, Riesgo: {lint_fail['risk_level']})")
    
    # Prueba de código VB6 válido
    vb6_clean = "Public Sub Sumar(a As Long, b As Long)\n    Dim res As Long\n    res = a + b\n    Debug.Print res\nEnd Sub"
    lint_ok = lint_vb6_code(vb6_clean)
    assert lint_ok["valid"], "El código VB6 válido debe ser aceptado"
    print(f" -> Validación VB6 válida OK (Riesgo: {lint_ok['risk_level']})")
    
    # Cálculo de Diff
    diff_res = compute_diff(orig_code, vb6_clean)
    assert diff_res["stats"]["added_lines"] == 1, "Debe reportar 1 línea agregada"
    print(f" -> Cálculo de Myers Diff OK (Líneas agregadas: {diff_res['stats']['added_lines']})")
    
    # Extractor de Markdown
    md_code = "Aquí está tu código:\n```vba\nPublic Sub Test()\n    MsgBox \"Hola\"\nEnd Sub\n```\nSaludos!"
    extracted = clean_markdown_code(md_code)
    assert extracted.startswith("Public Sub Test()"), "Error extrayendo código markdown"
    print(" -> Extractor Markdown a VB6 puro OK")
    
    # 3. Action Engine
    print("\n[3/4] Verificando Action Engine...")
    act = create_action(
        project_id=proj["id"],
        action_type="MODIFY_PROCEDURE",
        target_file="Module1.bas",
        target_procedure="Sumar",
        diff_unified=diff_res["diff_unified"],
        original_code=orig_code,
        proposed_code=vb6_clean,
        risk_level=lint_ok["risk_level"],
        description="Refactorización para pruebas",
        conversation_id=conv["id"]
    )
    assert act["id"].startswith("act_"), "Error creando acción"
    print(f" -> Acción registrada: {act['id']} (Estado: {act['status']})")
    
    update_res = update_action_status(act["id"], "EXECUTED")
    assert update_res, "Error actualizando estado de acción"
    print(" -> Estado de acción actualizado a EXECUTED OK")
    
    # 4. Motor de Snapshots y Backups
    print("\n[4/4] Verificando Motor de Snapshots y Backups...")
    bkp = create_backup_snapshot(
        project_vbp_path=proj["vbp_path"],
        target_file_rel="Module1.bas",
        content_before=orig_code,
        action_id=act["id"]
    )
    assert bkp["success"], "Error creando snapshot de backup"
    print(f" -> Snapshot de backup creado OK: {bkp['backup_file']} (SHA256: {bkp['sha256'][:10]}...)")
    
    print("\n=== TODAS LAS PRUEBAS DEL BACKEND PASARON EXITOSAMENTE! ===")

if __name__ == "__main__":
    test_full_suite()
