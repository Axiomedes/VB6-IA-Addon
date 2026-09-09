import os

base_dir = r"d:\Programming\Antigravity\VB6 IA Addon\AddIn_VB6"

# 1. modHttpClient.bas

Option Explicit

' ==============================================================================

' Utiliza WinHttp.WinHttpRequest.5.1 / MSXML2.ServerXMLHTTP60



    On Error GoTo ErrorHandler

    

    OutStatusCode = 0

    

    On Error Resume Next

    If http Is Nothing Then

    End If

        Set http = CreateObject("MSXML2.ServerXMLHTTP")

    On Error GoTo ErrorHandler

    If http Is Nothing Then

        Exit Function

    

    ' Configurar timeouts (Resolve, Connect, Send, Receive en milisegundos)

    http.SetTimeouts 3000, 3000, 5000, 5000

    

    

    OutResponse = StrConv(http.ResponseBody, vbUnicode)

    

    Exit Function

ErrorHandler:

    OutStatusCode = -1

    Set http = Nothing



    On Error GoTo ErrorHandler

    

    OutStatusCode = 0

    

    Set http = CreateObject("WinHttp.WinHttpRequest.5.1")

        Set http = CreateObject("MSXML2.ServerXMLHTTP.6.0")

    If http Is Nothing Then

    End If

    

        OutResponse = "No se pudo instanciar el cliente HTTP COM en Win32."

    End If

    http.Open "POST", Url, False

    http.setRequestHeader "Accept", "application/json"

    On Error Resume Next

    On Error GoTo ErrorHandler

    http.Send JsonBody

    OutStatusCode = http.Status

    HttpPost = (OutStatusCode >= 200 And OutStatusCode < 300)

    Set http = Nothing

    

    OutResponse = "Error HTTP POST: " & Err.Description

    HttpPost = False

End Function



json_content = """Attribute VB_Name = "modJSON"



' VB6 AI Assistant - Parser y Formateador JSON Ultraligero y Seguro para VB6



Public Function JsonEscape(ByVal Text As String) As String

    res = Replace(Text, "\\", "\\\\")

    res = Replace(res, vbCrLf, "\\n")

    res = Replace(res, vbLf, "\\n")

    JsonEscape = res



Public Function JsonGetString(ByVal json As String, ByVal Key As String) As String

    Dim posKey As Long

    Dim posStart As Long

    Dim charAt As String

    

    searchKey = "\"" & Key & "\""

    If posKey = 0 Then Exit Function

    posColon = InStr(posKey + Len(searchKey), json, ":")

    

    posStart = InStr(posColon + 1, json, "\"")

    

    posEnd = posStart + 1

        charAt = Mid$(json, posEnd, 1)

            posEnd = posEnd + 2

            Exit Do

            posEnd = posEnd + 1

    Loop

    If posEnd <= Len(json) Then

        valStr = Mid$(json, posStart + 1, posEnd - posStart - 1)

        valStr = Replace(valStr, "\\n", vbCrLf)

        valStr = Replace(valStr, "\\t", vbTab)

        valStr = Replace(valStr, "\\\\", "\\")

    End If



Public Function JsonGetBool(ByVal json As String, ByVal Key As String) As Boolean

    Dim posKey As Long

    Dim subStr As String

    JsonGetBool = False

    posKey = InStr(1, json, searchKey, vbTextCompare)

    

    If posColon = 0 Then Exit Function

    subStr = LCase$(Trim$(Mid$(json, posColon + 1, 15)))

        JsonGetBool = True

End Function

' Extrae una coleccion de cadenas de un array JSON de strings: ["item1", "item2"]

    Dim col As New Collection

    Dim posKey As Long

    Dim posBracketClose As Long

    Dim posStart As Long, posEnd As Long

    

    searchKey = "\"" & arrayKey & "\""

    If posKey = 0 Then Exit Function

    posBracketOpen = InStr(posKey + Len(searchKey), json, "[")

    

    If posBracketClose = 0 Then Exit Function

    arrayContent = Mid$(json, posBracketOpen + 1, posBracketClose - posBracketOpen - 1)

    

        posEnd = InStr(posStart + 1, arrayContent, "\"")

        itemStr = Mid$(arrayContent, posStart + 1, posEnd - posStart - 1)

            col.Add Trim$(itemStr)

        posStart = InStr(posEnd + 1, arrayContent, "\"")

    

End Function



frm_content = """VERSION 5.00

   Caption         =   "VB6 AI Assistant"

   ClientLeft      =   60

   ClientWidth     =   9800

   LinkTopic       =   "Form1"

   ScaleWidth      =   9800

   Begin VB.Timer tmrPolling 

      Interval        =   200

      Top             =   7320

   Begin VB.Frame fraTop 

      Height          =   855

      TabIndex        =   0

      Width           =   9575

         Height          =   315

         Style           =   2  'Dropdown List

         Top             =   280

      End

         Height          =   315

         TabIndex        =   2

         Top             =   280

      End

         Height          =   315

         Style           =   2  'Dropdown List

         Top             =   280

      End

         Caption         =   "Proveedor:"

         Left            =   120

         Top             =   320

      End

         Caption         =   "Modelo:"

         Left            =   2880

         Top             =   320

      End

         Caption         =   "Contexto:"

         Left            =   6000

         Top             =   320

      End

   Begin VB.TextBox txtChat 

      BeginProperty Font 

         Size            =   9

         Weight          =   400

         Italic          =   0   'False

      EndProperty

      Left            =   120

      MultiLine       =   -1  'True

      TabIndex        =   7

      Width           =   9575

   Begin VB.TextBox txtPrompt 

         Name            =   "Tahoma"

         Charset         =   0

         Underline       =   0   'False

         Strikethrough   =   0   'False

      Height          =   975

      MultiLine       =   -1  'True

      TabIndex        =   8

      Width           =   7455

   Begin VB.CommandButton cmdSend 

      Default         =   -1  'True

         Name            =   "Tahoma"

         Charset         =   0

         Underline       =   0   'False

         Strikethrough   =   0   'False

      Height          =   375

      TabIndex        =   9

      Width           =   2015

   Begin VB.CommandButton cmdAnalyze 

      Height          =   375

      TabIndex        =   10

      Width           =   2015

   Begin VB.CommandButton cmdCancel 

      Enabled         =   0   'False

      Left            =   7680

      Top             =   6720

   End

      Caption         =   "&Limpiar"

      Left            =   8720

      Top             =   6720

   End

      Caption         =   "Estado: Listo | Conectando a servicio local..."

      Left            =   120

      Top             =   6960

   End

Attribute VB_Name = "frmAIAssistant"

Attribute VB_Creatable = False

Attribute VB_Exposed = False



Public Connect As Object

Private m_CurrentJobID As String

Private m_LastTextLength As Long



    On Error Resume Next

    ' Inicializar proveedores

        .Clear

        .AddItem "OpenAI"

        .AddItem "Google Gemini"

        .AddItem "Groq"

    End With

    ' Inicializar modelos por defecto

        .Clear

        .AddItem "llama3"

        .AddItem "qwen2.5-coder:7b"

    End With

    ' Inicializar opciones de contexto

        .Clear

        .AddItem "2. Procedimiento Actual"

        .AddItem "4. Proyecto Completo"

    End With

    ' Mensaje inicial

                                "Conectando con el Servicio Local en " & DEFAULT_SERVICE_URL & "..."

    ' Verificar estado del servicio local

End Sub

Private Sub Form_Resize()

    If Me.WindowState = vbMinimized Then Exit Sub

    Dim w As Single, h As Single

    h = Me.ScaleHeight

    If w < 6000 Or h < 5000 Then Exit Sub

    fraTop.Width = w - 240

    txtChat.Height = h - fraTop.Height - txtPrompt.Height - 650

    txtPrompt.Top = txtChat.Top + txtChat.Height + 120

    

    cmdSend.Top = txtPrompt.Top

    cmdAnalyze.Left = cmdSend.Left

    

    cmdCancel.Top = cmdAnalyze.Top + cmdAnalyze.Height + 45

    

    cmdClear.Top = cmdCancel.Top

    

    lblStatus.Width = txtPrompt.Width



    On Error Resume Next

    If Not Connect Is Nothing Then

    End If



    On Error Resume Next

    Dim status As Long

    

    success = HttpGet(DEFAULT_SERVICE_URL & "/api/v1/health", resp, status)

    If success And status = 200 Then

        Dim modelsCol As Collection

        

        If modelsCol.Count > 0 Then

            For idx = 1 To modelsCol.Count

            Next idx

            lblStatus.Caption = "Estado: Servicio Conectado | Modelos Ollama detectados: " & modelsCol.Count

        Else

            AppendChatMessage "SERVICIO", "Servicio Local conectado en " & DEFAULT_SERVICE_URL & "." & vbCrLf & _

        End If

        m_ServiceOnline = False

        AppendChatMessage "AVISO", "No se detecto el Servicio Local en " & DEFAULT_SERVICE_URL & "." & vbCrLf & _

    End If



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

End Sub

Private Sub cmdSend_Click()

    Dim prompt As String

    Dim contextType As String

    Dim resp As String

    Dim success As Boolean

    If m_IsProcessing Then

        Exit Sub

    

    If Len(prompt) = 0 Then

        txtPrompt.SetFocus

    End If

    ' Obtener contexto del IDE segun combo

    

    AppendChatMessage "USUARIO", prompt

        AppendChatMessage "CONTEXTO (" & contextType & ")", contextCode

    

    jsonPayload = "{" & _

        "\"context\": \"" & JsonEscape(contextCode) & "\"," & _

        "\"model\": \"" & JsonEscape(cboModel.Text) & "\"" & _

        

    txtPrompt.Text = ""

    ' Iniciar peticion asincrona al servicio local

    

        m_CurrentJobID = JsonGetString(resp, "job_id")

            m_IsProcessing = True

            cmdSend.Enabled = False

            cmdCancel.Enabled = True

            AppendChatMessage "ASISTENTE (" & cboModel.Text & ")", "Generando respuesta..."

            ' Iniciar temporizador de polling no bloqueante

            lblStatus.Caption = "Estado: Generando respuesta (" & cboModel.Text & ")..."

        End If

    

    lblStatus.Caption = "Estado: Error al iniciar solicitud en el servicio local"

                              "Respuesta: " & resp & vbCrLf & _

    Exit Sub

ErrorHandler:

    MsgBox "Error al enviar mensaje: " & Err.Description, vbCritical, APP_TITLE



    On Error Resume Next

    Dim status As Long

    Dim jobStatus As String

    Dim isCompleted As Boolean

    

        tmrPolling.Enabled = False

    End If

    success = HttpGet(DEFAULT_SERVICE_URL & "/api/v1/chat/jobs/" & m_CurrentJobID, resp, status)

    If success And status = 200 Then

        generatedText = JsonGetString(resp, "text")

        errDesc = JsonGetString(resp, "error")

        ' Actualizar texto acumulado

            Call UpdateStreamingText(generatedText)

        

            tmrPolling.Enabled = False

            cmdSend.Enabled = True

            cmdCancel.Enabled = False

            If jobStatus = "COMPLETED" Then

            ElseIf jobStatus = "FAILED" Then

                AppendChatMessage "ERROR IA", "Fallo la generacion: " & errDesc

                lblStatus.Caption = "Estado: Tarea cancelada por el usuario."

            End If

    Else

        lblStatus.Caption = "Estado: Consultando avance..."

End Sub

Private Sub cmdCancel_Click()

    Dim resp As String

    

        lblStatus.Caption = "Estado: Cancelando tarea..."

    End If

    tmrPolling.Enabled = False

    cmdSend.Enabled = True

    cmdCancel.Enabled = False

End Sub

Private Sub cmdAnalyze_Click()

    Dim code As String

    

    code = GetSelectedCode()

        txtPrompt.Text = "Analiza el siguiente codigo seleccionado de VB6, explica su funcionamiento y sugiere optimizaciones:"

    Else

        If Len(code) > 0 Then

            cboContext.ListIndex = 1

            code = GetActiveModuleCode()

                txtPrompt.Text = "Realiza una revision completa del modulo activo de VB6 y resume su estructura:"

            Else

                Exit Sub

        End If

    

    Exit Sub

    MsgBox "Error en Analizar Codigo: " & Err.Description, vbCritical, APP_TITLE



    If MsgBox("Desea limpiar el historial de conversacion actual?", vbQuestion + vbYesNo, APP_TITLE) = vbYes Then

        AppendChatMessage "SISTEMA", "Historial limpiado. Listo para una nueva consulta."

End Sub

Private Function ExtractSelectedContext(ByRef OutContextType As String) As String

    Dim pName As String, pKind As Long

    Select Case cboContext.ListIndex

            OutContextType = "Codigo Seleccionado"

            If Len(ExtractSelectedContext) = 0 Then

                If Len(ExtractSelectedContext) > 0 Then

                Else

                    OutContextType = "Modulo Actual"

            End If

            ExtractSelectedContext = GetActiveProcedure(pName, pKind)

        Case 2 ' Modulo actual

            ExtractSelectedContext = GetActiveModuleCode()

            OutContextType = "Proyecto Completo"

    End Select



    On Error Resume Next

    Dim timeStr As String

    timeStr = Format$(Now, "hh:nn:ss")

    

        txtChat.Text = txtChat.Text & vbCrLf & vbCrLf & header & Message

        txtChat.Text = header & Message

    

End Sub

Private Sub UpdateStreamingText(ByVal FullGeneratedText As String)

    ' Reemplazar el ultimo mensaje de generacion por el texto actualizado

    lastHeaderPos = InStrRev(txtChat.Text, "=== [")

        Dim endHeaderPos As Long

        If endHeaderPos > 0 Then

            headerPart = Left$(txtChat.Text, endHeaderPos + 1)

            txtChat.SelStart = Len(txtChat.Text)

    End If

"""

# 4. VB6AIAssistant.vbp

Reference=*\\G{00020430-0000-0000-C000-000000000046}#2.0#0#..\\..\\..\\..\\..\\..\\Windows\\SysWOW64\\stdole2.tlb#OLE Automation

Reference=*\\G{AC0714F2-3D04-11D1-AE7D-00A0C90F26F4}#1.0#0#..\\..\\..\\..\\..\\..\\Program Files (x86)\\Common Files\\Designer\\MSADDNDR.DLL#Add-In Designer/Instance Control Library

Designer=Connect.Dsr

Module=modHttpClient; modHttpClient.bas

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

files = {

    "modJSON.bas": json_content,

    "VB6AIAssistant.vbp": vbp_content,



    fpath = os.path.join(base_dir, fname)

    lines = content.split("\n")

    if not crlf_content.endswith("\r\n"):

    with open(fpath, "wb") as f:

    print(f"Successfully wrote {fname} ({len(crlf_content)} bytes, CRLF, UTF-8)")

