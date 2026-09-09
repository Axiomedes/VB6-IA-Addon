import os

base_dir = r"d:\Programming\Antigravity\VB6 IA Addon\AddIn_VB6"

# 1. modJSON.bas

Option Explicit

' ==============================================================================

' ==============================================================================

' Escapa cadenas para formato JSON estricto (RFC 8259)

    Dim res As String

    q = Chr$(34)

    ' 1. Barra invertida primero

    ' 2. Comilla doble usando Chr$(34)

    ' 3. Saltos de linea y tabulaciones

    res = Replace(res, vbCr, "\\n")

    res = Replace(res, vbTab, "\\t")

    res = Replace(res, Chr$(12), "\\f")

End Function

' Constructor de propiedad String JSON: "clave": "valor"

    Dim q As String

    JsonPropString = q & Key & q & ": " & q & JsonEscape(Value) & q



Public Function JsonPropBool(ByVal Key As String, ByVal Value As Boolean) As String

    q = Chr$(34)

        JsonPropBool = q & Key & q & ": true"

        JsonPropBool = q & Key & q & ": false"

End Function

' Constructor de propiedad Numerica JSON: "clave": 123

    Dim q As String

    JsonPropNumber = q & Key & q & ": " & Trim$(Str$(Value))



Public Function JsonGetString(ByVal json As String, ByVal Key As String) As String

    Dim posKey As Long

    Dim posStart As Long

    Dim charAt As String

    

    JsonGetString = ""

    posKey = InStr(1, json, searchKey, vbTextCompare)

    

    If posColon = 0 Then Exit Function

    ' Buscar comilla inicial del valor

    If posStart = 0 Then Exit Function

    ' Buscar comilla de cierre considerando secuencias de escape

    Do While posEnd <= Len(json)

        If charAt = "\\" Then

        ElseIf charAt = q Then

        Else

        End If

    

        Dim valStr As String

        ' Desescapar caracteres comunes

        valStr = Replace(valStr, "\\r", "")

        valStr = Replace(valStr, "\\" & q, q)

        JsonGetString = valStr

End Function

' Extrae un valor booleano de un JSON

    Dim searchKey As String

    Dim posColon As Long

    Dim q As String

    q = Chr$(34)

    searchKey = q & Key & q

    If posKey = 0 Then Exit Function

    posColon = InStr(posKey + Len(searchKey), json, ":")

    

    If Left$(subStr, 4) = "true" Then

    End If



Public Function JsonGetArrayStrings(ByVal json As String, ByVal arrayKey As String) As Collection

    Dim searchKey As String

    Dim posBracketOpen As Long

    Dim arrayContent As String

    Dim itemStr As String

    

    Set JsonGetArrayStrings = col

    posKey = InStr(1, json, searchKey, vbTextCompare)

    

    If posBracketOpen = 0 Then Exit Function

    posBracketClose = InStr(posBracketOpen + 1, json, "]")

    

    posStart = InStr(1, arrayContent, q)

    Do While posStart > 0

        If posEnd = 0 Then Exit Do

        If Len(Trim$(itemStr)) > 0 Then

        End If

    Loop

    Set JsonGetArrayStrings = col

"""

# 2. frmAIAssistant.frm

Begin VB.Form frmAIAssistant 

   ClientHeight    =   7800

   ClientTop       =   345

   Icon            =   0

   ScaleHeight     =   7800

   StartUpPosition =   2  'CenterScreen

      Enabled         =   0   'False

      Left            =   120

   End

      Caption         =   " Configuracion de Consulta "

      Left            =   120

      Top             =   120

      Begin VB.ComboBox cboProvider 

         Left            =   960

         TabIndex        =   1

         Width           =   1815

      Begin VB.ComboBox cboModel 

         Left            =   3600

         Text            =   "codellama"

         Width           =   2295

      Begin VB.ComboBox cboContext 

         Left            =   6840

         TabIndex        =   3

         Width           =   2535

      Begin VB.Label lblProvider 

         Height          =   255

         TabIndex        =   4

         Width           =   855

      Begin VB.Label lblModel 

         Height          =   255

         TabIndex        =   5

         Width           =   615

      Begin VB.Label lblContext 

         Height          =   255

         TabIndex        =   6

         Width           =   735

   End

      BackColor       =   &H00FFFFFF&

         Name            =   "Courier New"

         Charset         =   0

         Underline       =   0   'False

         Strikethrough   =   0   'False

      Height          =   4695

      Locked          =   -1  'True

      ScrollBars      =   3  'Both

      Top             =   1080

   End

      BeginProperty Font 

         Size            =   9

         Weight          =   400

         Italic          =   0   'False

      EndProperty

      Left            =   120

      ScrollBars      =   2  'Vertical

      Top             =   5880

   End

      Caption         =   "&Enviar"

      BeginProperty Font 

         Size            =   8.25

         Weight          =   700

         Italic          =   0   'False

      EndProperty

      Left            =   7680

      Top             =   5880

   End

      Caption         =   "&Analizar Codigo"

      Left            =   7680

      Top             =   6300

   End

      Caption         =   "&Cancelar"

      Height          =   315

      TabIndex        =   11

      Width           =   975

   Begin VB.CommandButton cmdClear 

      Height          =   315

      TabIndex        =   12

      Width           =   975

   Begin VB.Label lblStatus 

      Height          =   255

      TabIndex        =   13

      Width           =   7455

End

Attribute VB_GlobalNameSpace = False

Attribute VB_PredeclaredId = True

Option Explicit

Public VBInstance As Object



Private m_IsProcessing As Boolean

Private m_ServiceOnline As Boolean

Private Sub Form_Load()

    

    With cboProvider

        .AddItem "Ollama (Local)"

        .AddItem "OpenRouter"

        .AddItem "Anthropic Claude"

        .ListIndex = 0 ' Ollama por defecto (Prioridad 1)

    

    With cboModel

        .AddItem "codellama"

        .AddItem "deepseek-coder:6.7b"

        .ListIndex = 0

    

    With cboContext

        .AddItem "1. Codigo Seleccionado"

        .AddItem "3. Modulo Actual"

        .ListIndex = 0

    

    AppendChatMessage "SISTEMA", "VB6 AI Assistant v1.0 listo." & vbCrLf & _

                                

    Call CheckServiceHealth



    On Error Resume Next

    

    w = Me.ScaleWidth

    

    

    txtChat.Width = w - 240

    

    txtPrompt.Width = w - cmdSend.Width - 360

    cmdSend.Left = txtPrompt.Left + txtPrompt.Width + 120

    

    cmdAnalyze.Top = cmdSend.Top + cmdSend.Height + 45

    cmdCancel.Left = cmdSend.Left

    cmdCancel.Width = (cmdSend.Width - 60) / 2

    cmdClear.Left = cmdCancel.Left + cmdCancel.Width + 60

    cmdClear.Width = cmdCancel.Width

    lblStatus.Top = txtPrompt.Top + txtPrompt.Height + 120

End Sub

Private Sub Form_Unload(Cancel As Integer)

    tmrPolling.Enabled = False

        Connect.FormDisplayed = False

End Sub

Public Sub CheckServiceHealth()

    Dim resp As String

    Dim success As Boolean

    lblStatus.Caption = "Estado: Consultando estado del servicio local..."

    

        m_ServiceOnline = True

        Dim idx As Long

        Set modelsCol = JsonGetArrayStrings(resp, "models")

            cboModel.Clear

                cboModel.AddItem modelsCol(idx)

            cboModel.ListIndex = 0

            AppendChatMessage "SERVICIO", "Servicio Local conectado. Modelos locales disponibles: " & modelsCol.Count

            lblStatus.Caption = "Estado: Servicio Conectado | Ollama no detecto modelos o esta apagado"

                                         "Aviso: Inicie Ollama en segundo plano para cargar sus modelos locales."

    Else

        lblStatus.Caption = "Estado: Servicio Local NO detectado en " & DEFAULT_SERVICE_URL

                                   "Ejecute 'Service_Python\\run_service.bat' para activar el puente de IA."

End Sub

Private Sub cboProvider_Click()

    cboModel.Clear

        Case "Ollama (Local)"

            cboModel.AddItem "llama3"

            cboModel.AddItem "qwen2.5-coder:7b"

        Case "OpenAI"

            cboModel.AddItem "gpt-4o-mini"

            cboModel.ListIndex = 0

            cboModel.AddItem "anthropic/claude-3.5-sonnet"

            cboModel.AddItem "qwen/qwen-2.5-coder-32b-instruct"

        Case "Google Gemini"

            cboModel.AddItem "gemini-1.5-pro"

        Case "Anthropic Claude"

            cboModel.AddItem "claude-3-haiku-20240307"

        Case "Groq"

            cboModel.AddItem "deepseek-r1-distill-llama-70b"

    End Select



    On Error GoTo ErrorHandler

    Dim contextCode As String

    Dim jsonPayload As String

    Dim status As Long

    

        MsgBox "Ya hay una solicitud en curso. Presione 'Cancelar' si desea interrumpirla.", vbExclamation, APP_TITLE

    End If

    prompt = Trim$(txtPrompt.Text)

        MsgBox "Por favor escriba una solicitud.", vbInformation, APP_TITLE

        Exit Sub

    

    contextCode = ExtractSelectedContext(contextType)

    ' Registrar en pantalla el mensaje del usuario

    If Len(contextCode) > 0 Then

    End If

    ' Construir JSON seguro utilizando los helpers de modJSON

        JsonPropString("prompt", prompt) & ", " & _

        JsonPropString("provider", LCase$(cboProvider.Text)) & ", " & _

        "}"

    lblStatus.Caption = "Estado: Conectando con IA en background..."

    

    success = HttpPost(DEFAULT_SERVICE_URL & "/api/v1/chat/start", jsonPayload, resp, status)

    If success And status = 200 Then

        If Len(m_CurrentJobID) > 0 Then

            m_LastTextLength = 0

            cmdAnalyze.Enabled = False

            

            

            tmrPolling.Enabled = True

            Exit Sub

    End If

    ' Si fallo la conexion

    AppendChatMessage "ERROR", "No fue posible conectar con el servicio local en " & DEFAULT_SERVICE_URL & "." & vbCrLf & _

                              "Asegurese de que 'Service_Python\\run_service.bat' este en ejecucion."

    

    lblStatus.Caption = "Estado: Error"

End Sub

Private Sub tmrPolling_Timer()

    Dim resp As String

    Dim success As Boolean

    Dim generatedText As String

    Dim errDesc As String

    If Len(m_CurrentJobID) = 0 Then

        Exit Sub

    

    

        jobStatus = JsonGetString(resp, "status")

        isCompleted = JsonGetBool(resp, "is_completed")

        

        If Len(generatedText) > 0 Then

        End If

        If isCompleted Then

            m_IsProcessing = False

            cmdAnalyze.Enabled = True

            

                lblStatus.Caption = "Estado: Respuesta completada con exito."

                lblStatus.Caption = "Estado: Error en la generacion."

            ElseIf jobStatus = "CANCELLED" Then

                AppendChatMessage "SISTEMA", "Generacion cancelada."

        End If

        ' Error temporal de polling

    End If



    On Error Resume Next

    Dim status As Long

    If Len(m_CurrentJobID) > 0 Then

        Call HttpPost(DEFAULT_SERVICE_URL & "/api/v1/chat/jobs/" & m_CurrentJobID & "/cancel", "{}", resp, status)

    

    m_IsProcessing = False

    cmdAnalyze.Enabled = True

    lblStatus.Caption = "Estado: Listo"



    On Error GoTo ErrorHandler

    Dim pName As String, pKind As Long

    ' Prioridad: 1. Codigo seleccionado, 2. Procedimiento actual, 3. Modulo actual

    If Len(code) > 0 Then

        cboContext.ListIndex = 0

        code = GetActiveProcedure(pName, pKind)

            txtPrompt.Text = "Analiza el procedimiento '" & pName & "' de VB6, busca posibles bugs, fugas de recursos y mejoras de rendimiento:"

        Else

            If Len(code) > 0 Then

                cboContext.ListIndex = 2

                MsgBox "No hay ningun modulo o codigo activo en el editor de VB6.", vbExclamation, APP_TITLE

            End If

    End If

    Call cmdSend_Click

ErrorHandler:

End Sub

Private Sub cmdClear_Click()

        txtChat.Text = ""

    End If



    On Error Resume Next

    

        Case 0 ' Codigo seleccionado

            ExtractSelectedContext = GetSelectedCode()

                ExtractSelectedContext = GetActiveProcedure(pName, pKind)

                    OutContextType = "Procedimiento Actual (" & pName & ")"

                    ExtractSelectedContext = GetActiveModuleCode()

                End If

        Case 1 ' Procedimiento actual

            OutContextType = "Procedimiento Actual (" & pName & ")"

            OutContextType = "Modulo Actual"

        Case 3 ' Proyecto completo

            ExtractSelectedContext = "[Indice de proyecto solicitado]"

End Function

Public Sub AppendChatMessage(ByVal Sender As String, ByVal Message As String)

    Dim header As String

    

    header = "=== [" & timeStr & "] " & UCase$(Sender) & " ===" & vbCrLf

    If Len(txtChat.Text) > 0 Then

    Else

    End If

    txtChat.SelStart = Len(txtChat.Text)



    On Error Resume Next

    Dim lastHeaderPos As Long

    If lastHeaderPos > 0 Then

        endHeaderPos = InStr(lastHeaderPos, txtChat.Text, vbCrLf)

            Dim headerPart As String

            txtChat.Text = headerPart & FullGeneratedText

        End If

End Sub



    "modJSON.bas": json_content,

}

for fname, content in files.items():

    # Ensure CRLF line endings on all lines

    crlf_content = "\r\n".join([line.rstrip("\r") for line in lines])

        crlf_content += "\r\n"

        f.write(crlf_content.encode("utf-8"))

