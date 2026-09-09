import os



sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Service_Python"))

from fastapi.testclient import TestClient

from app.core.database import init_db

def run_api_tests():

    

    client = TestClient(app)

    # 1. Health check

    resp = client.get("/api/v1/health")

    print(f" -> OK: {resp.json().get('status')}")

    # 2. History Projects

    resp = client.get("/api/v1/history/projects")

    print(f" -> OK: Proyectos encontrados: {len(resp.json().get('projects', []))}")

    # 3. Action Propose (Diff & Anti-VB.NET Linter)

    prop_payload = {

        "file_path": r"C:\TestProject\Module1.bas",

        "original_code": "Public Function CalcularTotal(precio As Currency, cant As Long) As Currency\n    CalcularTotal = precio * cant\nEnd Function",

        "action_type": "MODIFY_PROCEDURE",

    }

    assert resp.status_code == 200, f"Error en propose: {resp.text}"

    action_id = data["action_id"]

    diff_unif = data["diff_unified"]

    assert risk == "LOW", f"Se esperaba riesgo LOW, se obtuvo {risk}"

    print(f" -> OK: Acción propuesta {action_id} | Riesgo: {risk} | Líneas Diff: {len(data['diff_lines'])}")

    # 4. Action Execute (Snapshot & Backup preventivo)

    exec_payload = {

        "project_vbp": r"C:\TestProject\MyProject.vbp",

        "original_code": prop_payload["original_code"],

    }

    assert resp.status_code == 200, f"Error en execute: {resp.text}"

    assert exec_data["status"] == "EXECUTED"

    print(f" -> OK: Acción ejecutada con backup {exec_data['backup']['backup_id']}")

    # 5. List Backups

    resp = client.get("/api/v1/backups/project", params={"vbp_path": r"C:\TestProject\MyProject.vbp"})

    backups = resp.json().get("backups", [])

    print(f" -> OK: {len(backups)} backups registrados para el proyecto")

    # 6. Conversation & Messages History

    resp = client.get("/api/v1/history/conversations")

    convs = resp.json().get("conversations", [])

    



    run_api_tests()

