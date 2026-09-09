import os

base_dir = r"d:\Programming\Antigravity\VB6 IA Addon\AddIn_VB6"



    code = f.read()

# Replace cboProvider_Click to include free models

    On Error Resume Next

    Select Case cboProvider.Text

            cboModel.AddItem "codellama"

            cboModel.AddItem "deepseek-coder:6.7b"

            cboModel.ListIndex = 0

            cboModel.AddItem "gpt-4o"

            cboModel.AddItem "o1-preview"

        Case "OpenRouter"

            cboModel.AddItem "meta-llama/llama-3.3-70b-instruct"

            cboModel.ListIndex = 0

            cboModel.AddItem "gemini-2.0-flash"

            cboModel.ListIndex = 0

            cboModel.AddItem "claude-3-5-sonnet-20241022"

            cboModel.ListIndex = 0

            cboModel.AddItem "llama-3.3-70b-versatile"

            cboModel.ListIndex = 0

End Sub"""

new_sub = """Private Sub cboProvider_Click()

    cboModel.Clear

        Case "Ollama (Local)"

            cboModel.AddItem "llama3"

            cboModel.AddItem "qwen2.5-coder:7b"

        Case "OpenRouter"

            cboModel.AddItem "meta-llama/llama-3.3-70b-instruct:free"

            cboModel.AddItem "google/gemini-2.0-flash-exp:free"

            cboModel.ListIndex = 0

            cboModel.AddItem "gemini-2.0-flash"

            cboModel.AddItem "gemini-1.5-pro"

        Case "Groq"

            cboModel.AddItem "llama-3.1-8b-instant"

            cboModel.ListIndex = 0

            cboModel.AddItem "gpt-4o-mini"

            cboModel.ListIndex = 0

            cboModel.AddItem "claude-3-5-sonnet-20241022"

            cboModel.ListIndex = 0

End Sub"""

if old_sub in code:

    lines = code.split("\n")

    if not crlf_content.endswith("\r\n"):

    with open(fpath, "wb") as f:

    print("Updated frmAIAssistant.frm successfully!")

    print("Old sub text not exact match, let's normalize and replace.")

    norm_code = code.replace("\r\n", "\n")

    norm_new = new_sub.replace("\r\n", "\n")

        norm_code = norm_code.replace(norm_old, norm_new)

        with open(fpath, "wb") as f:

        print("Updated frmAIAssistant.frm via normalized replace!")

