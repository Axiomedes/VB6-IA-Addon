import difflib
import re
from typing import Dict, Any, List

VBNET_FORBIDDEN_PATTERNS = [
    (r"\bTry\b[\s\S]*?\bCatch\b", "Uso de 'Try...Catch' (exclusivo de VB.NET/C#). En VB6 use 'On Error GoTo / Resume Next'."),
    (r"\bDim\s+\w+(?:\s+As\s+\w+)?\s*=", "Inicialización directa en declaración 'Dim x = v' o 'Dim x As T = v'. En VB6 declare y luego asigne."),
    (r"(\+=|-=|\*=|/=|\\=)", "Operadores compuestos '+=', '-=', etc. no existen en VB6. Use 'x = x + 1'."),
    (r"\bReturn\s+", "Sentencia 'Return valor' (VB.NET). En VB6 asigne el retorno al nombre de la función."),
    (r"\bStringBuilder\b", "Clase .NET 'StringBuilder' no existe en VB6. Use concatenación de Strings o StringBuffers."),
    (r"\bConsole\.(Write|WriteLine)\b", "'Console.WriteLine' es de .NET. En VB6 use 'Debug.Print' o 'MsgBox'."),
    (r"\bImports\s+\w+", "Instrucción 'Imports' de .NET no existe en VB6."),
    (r"\bInherits\s+\w+", "Herencia de implementación 'Inherits' no existe en VB6. Use 'Implements' para interfaces."),
    (r"\bDim\s+\w+\s+As\s+New\s+List\s*\(Of\b", "Colección genérica 'List(Of ...)' no existe en VB6. Use Collection o Arrays."),
]

def lint_vb6_code(code: str) -> Dict[str, Any]:
    errors = []
    warnings = []

    for pattern, message in VBNET_FORBIDDEN_PATTERNS:
        matches = list(re.finditer(pattern, code, re.IGNORECASE))
        for m in matches:
            errors.append({
                "type": "ANTI_VBNET_LINT",
                "message": message,
                "match": m.group(0),
                "start": m.start(),
                "end": m.end()
            })

    if "On Error " not in code and ("Sub " in code or "Function " in code):
        warnings.append({
            "type": "MISSING_ERROR_HANDLING",
            "message": "Se recomienda incluir bloque 'On Error GoTo ErrorHandler' para robustez en VB6."
        })

    is_valid = len(errors) == 0
    risk_level = "LOW"
    if len(errors) > 0:
        risk_level = "HIGH"
    elif len(warnings) > 1:
        risk_level = "MEDIUM"

    return {
        "valid": is_valid,
        "risk_level": risk_level,
        "errors": errors,
        "warnings": warnings
    }

def clean_markdown_code(text: str) -> str:
    cleaned = text.strip()
    if "```" in cleaned:
        pattern = r"```[a-zA-Z0-9_-]*\s*([\s\S]*?)```"
        matches = re.findall(pattern, cleaned, re.IGNORECASE)
        if matches:
            cleaned = "\n\n".join(m.strip() for m in matches)
        else:
            cleaned = re.sub(r"```[a-zA-Z0-9_-]*\n?", "", cleaned)
            cleaned = cleaned.replace("```", "")
    return cleaned.strip()

def compute_diff(original_code: str, proposed_code: str, from_file: str = "Original", to_file: str = "Propuesto") -> Dict[str, Any]:
    orig_lines = original_code.splitlines(keepends=True)
    prop_lines = proposed_code.splitlines(keepends=True)

    diff = list(difflib.unified_diff(
        orig_lines,
        prop_lines,
        fromfile=from_file,
        tofile=to_file,
        n=3
    ))

    unified_text = "".join(diff)

    added_lines = sum(1 for line in diff if line.startswith("+") and not line.startswith("+++"))
    removed_lines = sum(1 for line in diff if line.startswith("-") and not line.startswith("---"))
    modified_blocks = sum(1 for line in diff if line.startswith("@@"))

    return {
        "diff_unified": unified_text,
        "stats": {
            "added_lines": added_lines,
            "removed_lines": removed_lines,
            "modified_blocks": modified_blocks
        }
    }
