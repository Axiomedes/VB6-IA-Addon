import os



target_dir = r"d:\Programming\Antigravity\VB6 IA Addon\AddIn_VB6"

os.makedirs(controls_dir, exist_ok=True)

# 1. Copy OLEGuids.tlb

dst_tlb = os.path.join(target_dir, "OLEGuids.tlb")

shutil.copy2(src_tlb, os.path.join(controls_dir, "OLEGuids.tlb"))



files_to_copy = [

    (r"Builds\TextBoxW\TextBoxW.ctx", "TextBoxW.ctx", False), # Binary

    (r"Builds\ComCtlsBase.bas", "ComCtlsBase.bas", True),

    (r"Common\Common.bas", "Common.bas", True),

]

for src_rel, dst_name, is_text in files_to_copy:

    dst_full = os.path.join(controls_dir, dst_name)

        with open(src_full, "r", encoding="latin-1") as f:

        # Convert to pure CRLF

        with open(dst_full, "wb") as f:

        print(f"Extracted and converted {dst_name} (CRLF, UTF-8)")

        shutil.copy2(src_full, dst_full)



vbp_content = """Type=OleDll

Reference=*\\G{2DF8D04C-5BFA-101B-BDE5-00AA0044DE52}#2.0#0#..\\..\\..\\..\\..\\..\\Program Files (x86)\\Common Files\\Microsoft Shared\\OFFICE15\\MSO.DLL#Microsoft Office 8.0 Object Library

Reference=*\\G{EF404E00-EDA6-101A-8DAF-00DD010F7EBB}#5.3#0#..\\..\\..\\..\\..\\..\\Program Files (x86)\\Microsoft Visual Studio\\VB98\\VB6EXT.OLB#Microsoft Visual Basic 6.0 Extensibility

Designer=Connect.Dsr

Module=modHttpClient; modHttpClient.bas

Module=ComCtlsBase; Controls\\ComCtlsBase.bas

Module=Common; Controls\\Common.bas

UserControl=Controls\\TextBoxW.ctl

Form=frmAIAssistant.frm

HelpFile=""

ExeName32="VB6AIAssistant.dll"

Name="VB6AIAssistant"

Description="VB6 AI Assistant - Asistente Inteligente con IA para Visual Basic 6.0"

MajorVer=1

RevisionVer=0

ServerSupportFiles=0

CompilationType=0

FavorPentiumPro(tm)=0

NoAliasing=0

OverflowCheck=0

FDIVCheck=0

StartMode=1

Retained=0

MaxNumberOfThreads=1

"""

vbp_path = os.path.join(target_dir, "VB6AIAssistant.vbp")

with open(vbp_path, "wb") as f:

print("Updated VB6AIAssistant.vbp with TextBoxW and OLEGuids.tlb")

# 4. Update frmAIAssistant.frm with TextBoxW control

with open(frm_path, "r", encoding="utf-8") as f:



old_txt_chat = """   Begin VB.TextBox txtChat 

      BeginProperty Font 

         Size            =   9

         Weight          =   400

         Italic          =   0   'False

      EndProperty

      Left            =   120

      MultiLine       =   -1  'True

      TabIndex        =   7

      Width           =   9575



      Height          =   4695

      TabIndex        =   7

      Width           =   9575

      _ExtentY        =   8281

      Locked          =   -1  'True

      ScrollBars      =   3

         Name            =   "Courier New"

         Charset         =   0

         Underline       =   0   'False

         Strikethrough   =   0   'False

   End"""

norm_frm = frm_text.replace("\r\n", "\n")

norm_new = new_txt_chat.replace("\r\n", "\n")

if norm_old in norm_frm:

else:

    import re



with open(frm_path, "wb") as f:

print("Updated frmAIAssistant.frm with TextBoxW control (Unicode & DPI-Aware)")

