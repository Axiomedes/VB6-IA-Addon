import os

frm_path = r"d:\Programming\Antigravity\VB6 IA Addon\AddIn_VB6\frmAIAssistant.frm"

    frm_text = f.read()

# Replace txtPrompt definition

      BeginProperty Font 

         Size            =   9

         Weight          =   400

         Italic          =   0   'False

      EndProperty

      Left            =   120

      ScrollBars      =   2  'Vertical

      Top             =   5880

   End"""

new_prompt = """   Begin VB6AIAssistant.TextBoxW txtPrompt 

      Left            =   120

      Top             =   5880

      _ExtentX        =   13150

      MultiLine       =   -1  'True

      CueBanner       =   "Escriba aquíí su consulta o solicitud a la IA... (Ctrl+Enter para enviar)"

         Name            =   "Tahoma"

         Charset         =   0

         Underline       =   0   'False

         Strikethrough   =   0   'False

   End"""

norm_frm = frm_text.replace("\r\n", "\n")

norm_new = new_prompt.replace("\r\n", "\n")

if norm_old in norm_frm:

else:

    norm_frm = re.sub(r'Begin\s+VB6AIAssistant\.TextBoxW\s+txtPrompt\b.*?End', norm_new, norm_frm, flags=re.DOTALL)

# Add txtPrompt_KeyDown handler if not present

    key_event_code = """

    ' Enviar mensaje con Ctrl+Enter

        KeyCode = 0

    End If

"""



with open(frm_path, "wb") as f:



