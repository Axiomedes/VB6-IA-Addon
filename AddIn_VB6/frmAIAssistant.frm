VERSION 5.00
Begin VB.Form frmAIAssistant 
   Caption         =   "VB6 AI Assistant"
   ClientHeight    =   7800
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   9795
   Icon            =   "frmAIAssistant.frx":0000
   LinkTopic       =   "Form1"
   ScaleHeight     =   7800
   ScaleWidth      =   9795
   StartUpPosition =   2  'CenterScreen
   Begin VB.CommandButton cmdConfig 
      Caption         =   "C"
      Height          =   360
      Left            =   9330
      TabIndex        =   14
      Top             =   585
      Width           =   420
   End
   Begin VB.CommandButton cmdAbout 
      Caption         =   "?"
      Height          =   360
      Left            =   9330
      TabIndex        =   13
      Top             =   150
      Width           =   420
   End
   Begin VB.Timer tmrPolling 
      Enabled         =   0   'False
      Interval        =   100
      Left            =   120
      Top             =   7320
   End
   Begin VB.Frame fraTop 
      Caption         =   " Configuración de Consulta "
      Height          =   855
      Left            =   120
      TabIndex        =   0
      Top             =   120
      Width           =   9120
      Begin VB.ComboBox cboProvider 
         Height          =   315
         Left            =   1080
         Style           =   2  'Dropdown List
         TabIndex        =   1
         Top             =   280
         Width           =   2655
      End
      Begin VB.ComboBox cboModel 
         Height          =   315
         Left            =   4680
         TabIndex        =   2
         Text            =   "qwen3:1.7b"
         Top             =   280
         Width           =   4320
      End
      Begin VB.Label lblProvider 
         Caption         =   "Proveedor:"
         Height          =   255
         Left            =   160
         TabIndex        =   3
         Top             =   320
         Width           =   855
      End
      Begin VB.Label lblModel 
         Caption         =   "Modelo:"
         Height          =   255
         Left            =   3960
         TabIndex        =   4
         Top             =   320
         Width           =   615
      End
   End
   Begin VB6AIAssistant.RichTextBox txtChat 
      Height          =   4500
      Left            =   120
      TabIndex        =   5
      Top             =   1080
      Width           =   9575
      _ExtentX        =   16880
      _ExtentY        =   7938
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "Segoe UI"
         Size            =   9
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      BackColor       =   16777215
      Locked          =   -1  'True
      MultiLine       =   -1  'True
      ScrollBars      =   3
      TextRTF         =   "frmAIAssistant.frx":000C
   End
   Begin VB6AIAssistant.TextBoxW txtPrompt 
      Height          =   1150
      Left            =   120
      TabIndex        =   6
      Top             =   5700
      Width           =   7455
      _ExtentX        =   13150
      _ExtentY        =   2037
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "Tahoma"
         Size            =   9
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      MultiLine       =   -1  'True
      ScrollBars      =   2
      CueBanner       =   "Escriba aquí su consulta o solicitud a la IA... Ej: 'analiza la función CalcularTotal' (Ctrl+Enter para enviar)"
   End
   Begin VB.CommandButton cmdSend 
      Caption         =   "&Enviar"
      Default         =   -1  'True
      BeginProperty Font 
         Name            =   "Tahoma"
         Size            =   8.25
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   340
      Left            =   7680
      TabIndex        =   7
      Top             =   5700
      Width           =   2015
   End
   Begin VB.CommandButton cmdAnalyze 
      Caption         =   "&Analizar Código"
      Height          =   340
      Left            =   7680
      TabIndex        =   8
      Top             =   6080
      Width           =   2015
   End
   Begin VB.CommandButton cmdReviewChanges 
      Caption         =   "&Revisar y Aplicar..."
      BeginProperty Font 
         Name            =   "Tahoma"
         Size            =   8.25
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   340
      Left            =   7680
      TabIndex        =   9
      Top             =   6460
      Width           =   2015
   End
   Begin VB.CommandButton cmdCancel 
      Caption         =   "&Cancelar"
      Enabled         =   0   'False
      Height          =   315
      Left            =   7680
      TabIndex        =   10
      Top             =   6840
      Width           =   975
   End
   Begin VB.CommandButton cmdClear 
      Caption         =   "&Limpiar"
      Height          =   315
      Left            =   8720
      TabIndex        =   11
      Top             =   6840
      Width           =   975
   End
   Begin VB.Label lblStatus 
      Caption         =   "Estado: Listo | Conectando a servicio local..."
      Height          =   255
      Left            =   120
      TabIndex        =   12
      Top             =   6960
      Width           =   7455
   End
End
Attribute VB_Name = "frmAIAssistant"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private Declare Function SendMessage _
                Lib "user32" _
                Alias "SendMessageW" (ByVal hWnd As Long, _
                                      ByVal wMsg As Long, _
                                      ByVal wParam As Long, _
                                      ByRef lParam As Any) As Long

Private Declare Function RedrawWindow _
                Lib "user32" (ByVal hWnd As Long, _
                              ByVal lprcUpdate As Long, _
                              ByVal hrgnUpdate As Long, _
                              ByVal fuRedraw As Long) As Long

Private Const WM_SETREDRAW   As Long = &HB
Private Const RDW_INVALIDATE As Long = &H1
Private Const RDW_UPDATENOW  As Long = &H100
Private Const RDW_NOERASE    As Long = &H20
Private Const vbOrange       As Long = 33023 '&H80FF&
Public VBInstance            As Object
Public Connect               As Object
Private m_CurrentJobID       As String
Private m_IsProcessing       As Boolean
Private m_LastTextLength     As Long
Private m_ServiceOnline      As Boolean
Private m_StreamingStartPos  As Long
Private m_LastRenderedText   As String

Private Sub cmdAbout_Click()
  frmAbout.Show 1
End Sub

Private Sub cmdConfig_Click()
  On Error Resume Next
  Dim frm As frmConfig
  Set frm = New frmConfig
  
  frm.SelectedProviderIndex = cboProvider.ListIndex
  frm.Show 1, Me
  
  If frm.SelectedProviderIndex >= 0 And frm.SelectedProviderIndex < cboProvider.ListCount Then
    cboProvider.ListIndex = frm.SelectedProviderIndex
  End If
  
  Call RefreshModels(frm.SelectedModelName)
  Call ApplyI18N
  Set frm = Nothing
End Sub

Public Sub ApplyI18N()
  On Error Resume Next
  Me.Caption = T("APP_TITLE", "VB6 AI Assistant")
  lblProvider.Caption = T("LBL_PROVIDER", "Proveedor:")
  lblModel.Caption = T("LBL_MODEL", "Modelo:")
  cmdSend.Caption = T("BTN_SEND", "Enviar")
  cmdAnalyze.Caption = T("BTN_ANALYZE", "Analizar Código")
  cmdReviewChanges.Caption = T("BTN_APPLY", "Aplicar Cambios")
  cmdCancel.Caption = T("BTN_CANCEL", "Cancelar")
  cmdClear.Caption = T("BTN_CLEAR", "Limpiar")

End Sub

Private Sub Form_Load()

  On Error Resume Next
  Call InitI18N
  Call ApplyI18N

  ' Inicializar proveedores
  With cboProvider
    .Clear
    .AddItem "Ollama (Local)"
    .AddItem "OpenRouter"
    .AddItem "Google Gemini"
    .AddItem "Groq"
    .AddItem "OpenAI"
    .AddItem "Anthropic Claude"
    .ListIndex = 0 ' Ollama por defecto
  End With

  ' Inicializar modelos por defecto
  With cboModel
    .Clear
    .AddItem "Qwen3:1.7b"
    .AddItem "VB6-IA:latest"
    .AddItem "hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0"
    .AddItem "codellama"
    .AddItem "llama3"
    .AddItem "deepseek-coder:6.7b"
    .AddItem "qwen2.5-coder:7b"
    .ListIndex = 0
  End With

  ' Mensaje inicial con bienvenida y estado
  AppendChatMessage "SISTEMA", "VB6 AI Assistant - David Rojas [AxioUK]+Antigravity" & vbCrLf & "Conectando con el Servicio Local en " & DEFAULT_SERVICE_URL & "..."
  ' Verificar estado del servicio local
  Call CheckServiceHealth
End Sub

Private Sub Form_Resize()

  On Error Resume Next

  If Me.WindowState = vbMinimized Then Exit Sub

  Dim w As Single, h As Single

  w = Me.ScaleWidth
  h = Me.ScaleHeight

  If w < 6000 Or h < 5000 Then Exit Sub
  fraTop.Width = w - (cmdAbout.Width + 450)
  cmdAbout.Left = fraTop.Left + fraTop.Width + 230
  cmdConfig.Left = cmdAbout.Left
  cboModel.Width = fraTop.Width - cboModel.Left - 180
  txtChat.Width = w - 240
  txtChat.Height = h - fraTop.Height - txtPrompt.Height - 750
  txtPrompt.Top = txtChat.Top + txtChat.Height + 120
  txtPrompt.Width = w - cmdSend.Width - 360
  cmdSend.Left = txtPrompt.Left + txtPrompt.Width + 120
  cmdSend.Top = txtPrompt.Top
  cmdAnalyze.Left = cmdSend.Left
  cmdAnalyze.Top = cmdSend.Top + cmdSend.Height + 40
  cmdReviewChanges.Left = cmdSend.Left
  cmdReviewChanges.Top = cmdAnalyze.Top + cmdAnalyze.Height + 40
  cmdCancel.Left = cmdSend.Left
  cmdCancel.Top = cmdReviewChanges.Top + cmdReviewChanges.Height + 40
  cmdCancel.Width = (cmdSend.Width - 60) / 2
  cmdClear.Left = cmdCancel.Left + cmdCancel.Width + 60
  cmdClear.Top = cmdCancel.Top
  cmdClear.Width = cmdCancel.Width
  lblStatus.Top = txtPrompt.Top + txtPrompt.Height + 80
  lblStatus.Width = txtPrompt.Width
End Sub

Private Sub Form_Unload(Cancel As Integer)
  On Error Resume Next
  tmrPolling.Enabled = False

  If Not Connect Is Nothing Then
    Connect.FormDisplayed = False
  End If

End Sub

Public Sub CheckServiceHealth()
  On Error Resume Next
  Dim resp    As String
  Dim status  As Long
  Dim success As Boolean

  lblStatus.ForeColor = vbBlack
  lblStatus.Caption = "Estado: Consultando estado del servicio local..."
  success = HttpGet(DEFAULT_SERVICE_URL & "/api/v1/health", resp, status)

  If success And status = 200 Then
    m_ServiceOnline = True

    Dim modelsCol As Collection
    Dim idx       As Long
    Set modelsCol = JsonGetArrayStrings(resp, "models")

    If modelsCol.Count > 0 Then
      cboModel.Clear

      For idx = 1 To modelsCol.Count
        cboModel.AddItem modelsCol(idx)
      Next idx

      cboModel.ListIndex = 0
      lblStatus.ForeColor = vbGreen
      lblStatus.Caption = "Estado: Servicio Conectado | Modelos Ollama detectados: " & modelsCol.Count
      AppendChatMessage "SERVICIO", "Servicio Local conectado. Modelos locales disponibles: " & modelsCol.Count
    Else
      lblStatus.ForeColor = vbGreen
      lblStatus.Caption = "Estado: Servicio Conectado | Ollama no detectó modelos o está apagado"
      AppendChatMessage "SERVICIO", "Servicio Local conectado en " & DEFAULT_SERVICE_URL & "." & vbCrLf & "Aviso: Inicie Ollama en segundo plano para cargar sus modelos locales."
    End If

  Else
    m_ServiceOnline = False
    lblStatus.ForeColor = vbRed
    lblStatus.Caption = "Estado: Servicio Local NO detectado en " & DEFAULT_SERVICE_URL
    AppendChatMessage "AVISO", "No se detecto el Servicio Local en " & DEFAULT_SERVICE_URL & "." & vbCrLf & "Ejecute 'Service_Python\run_service.bat' para activar el puente de IA."
  End If

End Sub

Private Function GetProviderKey(ByVal provText As String) As String
  Select Case provText
    Case "Ollama (Local)": GetProviderKey = "ollama"
    Case "OpenRouter": GetProviderKey = "openrouter"
    Case "Google Gemini": GetProviderKey = "gemini"
    Case "Groq": GetProviderKey = "groq"
    Case "OpenAI": GetProviderKey = "openai"
    Case "Anthropic Claude": GetProviderKey = "claude"
    Case Else: GetProviderKey = "ollama"
  End Select
End Function

Private Sub LoadFallbackModels(ByVal provKey As String)
  cboModel.Clear
  Select Case provKey
    Case "ollama"
      cboModel.AddItem "qwen3:1.7b"
      cboModel.AddItem "VB6-IA:latest"
      cboModel.AddItem "hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0"
      cboModel.AddItem "codellama"
      cboModel.AddItem "llama3"
      cboModel.AddItem "deepseek-coder:6.7b"
      cboModel.AddItem "qwen2.5-coder:7b"
      cboModel.ListIndex = 0
    Case "openrouter"
      cboModel.AddItem "openrouter/free"
      cboModel.AddItem "nvidia/nemotron-3.5-lightning:free"
      cboModel.AddItem "google/gemma-4-31b-it:free"
      cboModel.AddItem "google/gemma-4-26b-a4b-it:free"
      cboModel.AddItem "cohere/north-mini-code:free"
      cboModel.AddItem "poolside/laguna-s-2.1:free"
      cboModel.AddItem "thinkingmachines/inkling:free"
      cboModel.ListIndex = 0
    Case "gemini"
      cboModel.AddItem "gemini-flash-latest"
      cboModel.AddItem "gemini-pro-latest"
      cboModel.AddItem "gemini-3.6-flash"
      cboModel.AddItem "gemini-3.5-flash"
      cboModel.AddItem "gemini-2.5-flash-lite"
      cboModel.ListIndex = 0
    Case "groq"
      cboModel.AddItem "llama-3.3-70b-versatile"
      cboModel.AddItem "llama-3.1-8b-instant"
      cboModel.AddItem "deepseek-r1-distill-llama-70b"
      cboModel.ListIndex = 0
    Case "openai"
      cboModel.AddItem "gpt-4o-mini"
      cboModel.AddItem "gpt-4o"
      cboModel.AddItem "o3-mini"
      cboModel.ListIndex = 0
    Case "claude"
      cboModel.AddItem "claude-3-5-sonnet-20241022"
      cboModel.AddItem "claude-3-5-haiku-20241022"
      cboModel.ListIndex = 0
  End Select
End Sub

Public Sub RefreshModels(Optional ByVal preferredModel As String = "")
  On Error Resume Next
  Dim provKey   As String
  Dim resp      As String
  Dim status    As Long
  Dim success   As Boolean
  Dim modelsCol As Collection
  Dim idx       As Long
  Dim foundPref As Boolean

  provKey = GetProviderKey(cboProvider.Text)
  cboModel.Clear

  ' 1. Consultar modelos dinámicos en tiempo real desde el servicio local
  If m_ServiceOnline Then
    success = HttpGet(DEFAULT_SERVICE_URL & "/api/v1/providers/" & provKey & "/models", resp, status)
    If success And status = 200 Then
      Set modelsCol = JsonGetArrayStrings(resp, "models")
      If Not modelsCol Is Nothing Then
        If modelsCol.Count > 0 Then
          For idx = 1 To modelsCol.Count
            cboModel.AddItem modelsCol(idx)
            If Len(preferredModel) > 0 And modelsCol(idx) = preferredModel Then
              cboModel.ListIndex = cboModel.NewIndex
              foundPref = True
            End If
          Next idx

          If Not foundPref Then
            If Len(preferredModel) > 0 Then
              cboModel.Text = preferredModel
            Else
              cboModel.ListIndex = 0
            End If
          End If
          lblStatus.ForeColor = vbGreen
          lblStatus.Caption = "Estado: " & cboProvider.Text & " listo (" & modelsCol.Count & " modelos disponibles)"
          Exit Sub
        End If
      End If
    End If
  End If

  ' 2. Fallback a lista predeterminada
  Call LoadFallbackModels(provKey)
  If Len(preferredModel) > 0 Then
    cboModel.Text = preferredModel
  End If
End Sub

Private Sub cboProvider_Click()
  Call RefreshModels("")
End Sub

Private Sub txtPrompt_KeyDown(KeyCode As Integer, Shift As Integer)

  If KeyCode = vbKeyReturn And (Shift And vbCtrlMask) <> 0 Then
    KeyCode = 0
    Call cmdSend_Click
  End If

End Sub

Private Sub cmdSend_Click()
  On Error GoTo ErrorHandler
  Dim Prompt      As String
  Dim contextCode As String
  Dim ContextType As String
  Dim projName    As String, projPath As String
  Dim jsonPayload As String
  Dim resp        As String
  Dim status      As Long
  Dim success     As Boolean

  If m_IsProcessing Then
    MsgBox T("MSG_REQUEST_IN_PROGRESS", "Ya hay una solicitud en curso. Presione 'Cancelar' si desea interrumpirla."), vbExclamation, APP_TITLE
    Exit Sub
  End If

  Prompt = Trim$(txtPrompt.Text)

  If Len(Prompt) = 0 Then
    MsgBox T("MSG_WRITE_REQUEST", "Por favor escriba una solicitud."), vbInformation, APP_TITLE
    txtPrompt.SetFocus
    Exit Sub
  End If

  ' Resolucion inteligente de contexto segun prompt o estado del editor
  contextCode = SmartResolveContext(Prompt, ContextType)
  Call GetActiveProjectInfo(projName, projPath)
  ' Registrar en pantalla el mensaje del usuario
  AppendChatMessage "USUARIO", Prompt

  If Len(contextCode) > 0 Then
    AppendChatMessage T("PROMPT_AUTO_CTX_FOUND", "CONTEXTO DETECTADO") & " (" & ContextType & ")", contextCode
  End If

  ' Construir JSON seguro utilizando los helpers de modJSON
  jsonPayload = "{" & JsonPropString("prompt", Prompt) & ", " & JsonPropString("context", contextCode) & ", " & JsonPropString("provider", LCase$(cboProvider.Text)) & ", " & JsonPropString("model", cboModel.Text) & ", " & JsonPropString("project_vbp", projPath) & ", " & JsonPropString("language", GetLanguage()) & "}"
  lblStatus.ForeColor = vbBlack
  lblStatus.Caption = T("LBL_STATUS", "Estado:") & " " & T("STATUS_QUERYING", "Conectando con IA en background...")
  txtPrompt.Text = ""
  ' Iniciar peticion asincrona al servicio local
  success = HttpPost(DEFAULT_SERVICE_URL & "/api/v1/chat/start", jsonPayload, resp, status)

  If success And status = 200 Then
    m_CurrentJobID = JsonGetString(resp, "job_id")

    If Len(m_CurrentJobID) > 0 Then
      m_IsProcessing = True
      m_LastTextLength = 0
      cmdSend.Enabled = False
      cmdAnalyze.Enabled = False
      cmdCancel.Enabled = True
      AppendChatMessage "ASISTENTE (" & cboModel.Text & ")", "Generando respuesta..."
      m_StreamingStartPos = Len(txtChat.Text) - Len("Generando respuesta...")

      If m_StreamingStartPos < 0 Then m_StreamingStartPos = 0
      m_LastRenderedText = "Generando respuesta..."
      ' Iniciar temporizador de polling no bloqueante
      tmrPolling.Enabled = True
      lblStatus.ForeColor = vbYellow
      lblStatus.Caption = T("LBL_STATUS", "Estado:") & " " & T("STATUS_STREAMING", "Generando respuesta...") & " (" & cboModel.Text & ")..."
      Exit Sub

    End If
  End If

  lblStatus.ForeColor = vbRed
  lblStatus.Caption = T("LBL_STATUS", "Estado:") & " " & T("STATUS_ERROR", "Error al iniciar solicitud en el servicio local")
  AppendChatMessage "ERROR", "No fue posible conectar con el servicio local en " & DEFAULT_SERVICE_URL & "." & vbCrLf & "Respuesta: " & resp & vbCrLf & "Asegúrese de que 'Service_Python\run_service.bat' esté en ejecución."

  Exit Sub

ErrorHandler:
  lblStatus.ForeColor = vbRed
  lblStatus.Caption = "Estado: Error"
  MsgBox "Error al enviar mensaje: " & Err.Description, vbCritical, APP_TITLE
End Sub

Private Sub tmrPolling_Timer()
  On Error Resume Next
  Dim resp          As String
  Dim status        As Long
  Dim success       As Boolean
  Dim jobStatus     As String
  Dim generatedText As String
  Dim isCompleted   As Boolean
  Dim errDesc       As String

  If Len(m_CurrentJobID) = 0 Then
    tmrPolling.Enabled = False
    Exit Sub
  End If

  success = HttpGet(DEFAULT_SERVICE_URL & "/api/v1/chat/jobs/" & m_CurrentJobID, resp, status)

  If success And status = 200 Then
    jobStatus = JsonGetString(resp, "status")
    generatedText = JsonGetString(resp, "text")
    isCompleted = JsonGetBool(resp, "is_completed")
    errDesc = JsonGetString(resp, "error")

    ' Actualizar texto acumulado
    If Len(generatedText) > 0 Then
      Call UpdateStreamingText(generatedText)
    End If

    If isCompleted Then
      tmrPolling.Enabled = False
      m_IsProcessing = False
      m_LastRenderedText = ""
      cmdSend.Enabled = True
      cmdAnalyze.Enabled = True
      cmdCancel.Enabled = False

      If jobStatus = "COMPLETED" Then
        lblStatus.ForeColor = vbGreen
        lblStatus.Caption = "Estado: Respuesta completada con éxito."
      ElseIf jobStatus = "FAILED" Then
        lblStatus.ForeColor = vbRed
        lblStatus.Caption = "Estado: Error en la generación."
        AppendChatMessage "ERROR IA", "Falló la generación: " & errDesc
      ElseIf jobStatus = "CANCELLED" Then
        lblStatus.ForeColor = vbOrange
        lblStatus.Caption = "Estado: Tarea cancelada por el usuario."
        AppendChatMessage "SISTEMA", "Generación cancelada."
      End If
    End If

  Else
    lblStatus.ForeColor = vbBlack
    lblStatus.Caption = "Estado: Consultando avance..."
  End If

End Sub

Private Sub cmdCancel_Click()
  On Error Resume Next
  Dim resp   As String
  Dim status As Long

  If Len(m_CurrentJobID) > 0 Then
    lblStatus.ForeColor = vbRed
    lblStatus.Caption = "Estado: Cancelando tarea..."
    Call HttpPost(DEFAULT_SERVICE_URL & "/api/v1/chat/jobs/" & m_CurrentJobID & "/cancel", "{}", resp, status)
  End If

  tmrPolling.Enabled = False
  m_IsProcessing = False
  m_LastRenderedText = ""
  cmdSend.Enabled = True
  cmdAnalyze.Enabled = True
  cmdCancel.Enabled = False
  lblStatus.ForeColor = vbGreen
  lblStatus.Caption = "Estado: Listo"
End Sub

Private Sub cmdAnalyze_Click()
  On Error GoTo ErrorHandler
  Dim Prompt As String
  Prompt = Trim$(txtPrompt.Text)

  If Len(Prompt) = 0 Then
    txtPrompt.Text = T("PROMPT_ANALYZE_DEFAULT", "Analiza el siguiente código de VB6, explica su funcionamiento, posibles bugs y sugiere optimizaciones:")
  End If

  Call cmdSend_Click
  Exit Sub

ErrorHandler:
  MsgBox "Error en Analizar Código: " & Err.Description, vbCritical, APP_TITLE
End Sub

Private Sub cmdReviewChanges_Click()
  On Error GoTo ErrorHandler
  Dim generatedText As String
  Dim origCode      As String
  Dim pName         As String, pKind As Long
  Dim projName      As String, projPath As String
  Dim ActionType    As String
  Dim jsonPayload   As String
  Dim resp          As String
  Dim status        As Long
  Dim success       As Boolean

  generatedText = ExtractLastAssistantResponse()

  If Len(Trim$(generatedText)) = 0 Then
    MsgBox T("MSG_NO_CODE_TO_APPLY", "No hay código generado por la IA en el chat para revisar."), vbInformation, APP_TITLE
    Exit Sub
  End If

  origCode = GetSelectedCode()

  If Len(origCode) > 0 Then
    ActionType = "MODIFY_PROCEDURE"
  Else
    origCode = GetActiveProcedure(pName, pKind)

    If Len(origCode) > 0 Then
      ActionType = "MODIFY_PROCEDURE"
    Else
      origCode = GetActiveModuleCode()

      If Len(origCode) > 0 Then
        ActionType = "REPLACE_MODULE"
      Else
        ActionType = "CREATE_COMPONENT"
      End If
    End If
  End If

  Call GetActiveProjectInfo(projName, projPath)
  jsonPayload = "{" & JsonPropString("project_vbp", projPath) & ", " & JsonPropString("target_procedure", pName) & ", " & JsonPropString("original_code", origCode) & ", " & JsonPropString("proposed_code", generatedText) & ", " & JsonPropString("action_type", ActionType) & ", " & JsonPropString("description", "Cambio sugerido por IA para " & IIf(Len(pName) > 0, pName, "módulo activo")) & "}"
  lblStatus.ForeColor = vbYellow
  lblStatus.Caption = "Estado: Analizando diferencias con el servicio local..."
  success = HttpPost(DEFAULT_SERVICE_URL & "/api/v1/actions/propose", jsonPayload, resp, status)

  If success And status = 200 Then

    Dim ActionID As String, RiskLevel As String, DiffUnified As String, cleanCode As String

    ActionID = JsonGetString(resp, "action_id")
    RiskLevel = JsonGetString(resp, "risk_level")
    DiffUnified = JsonGetString(resp, "diff_unified")
    cleanCode = JsonGetString(resp, "proposed_code_clean")

    If Len(cleanCode) = 0 Then cleanCode = generatedText

    Dim frm As frmChanges

    Set frm = New frmChanges
    Call frm.ShowProposal(ActionID, IIf(Len(pName) > 0, pName, "MóduloActivo"), pName, origCode, cleanCode, DiffUnified, RiskLevel, "Revisión previa obligatoria", ActionType)
    Set frm = Nothing
    lblStatus.ForeColor = vbGreen
    lblStatus.Caption = "Estado: Listo"
  Else
    MsgBox "Error analizando propuesta de cambios: " & resp, vbCritical, APP_TITLE
    lblStatus.ForeColor = vbRed
    lblStatus.Caption = "Estado: Error al proponer cambios"
  End If

  Exit Sub

ErrorHandler:
  MsgBox "Error en Revisar Cambios: " & Err.Description, vbCritical, APP_TITLE
End Sub

Private Function ExtractLastAssistantResponse() As String
  On Error Resume Next
  Dim fullTxt As String
  Dim Pos     As Long, endHeader As Long
  fullTxt = txtChat.Text
  Pos = InStrRev(fullTxt, "=== [")

  If Pos > 0 Then
    If InStr(Pos, fullTxt, "ASISTENTE") > 0 Then
      endHeader = InStr(Pos, fullTxt, vbCrLf)

      If endHeader > 0 Then
        ExtractLastAssistantResponse = Mid$(fullTxt, endHeader + 2)
      End If
    End If
  End If

  If Len(Trim$(ExtractLastAssistantResponse)) = 0 Then
    ExtractLastAssistantResponse = fullTxt
  End If

End Function

Private Sub cmdClear_Click()
  Dim wasLocked As Boolean

  If MsgBox("¿Desea limpiar el historial de conversación actual?", vbQuestion + vbYesNo, APP_TITLE) = vbYes Then
    wasLocked = txtChat.Locked

    If wasLocked Then txtChat.Locked = False
    txtChat.Text = ""

    If wasLocked Then txtChat.Locked = True
    AppendChatMessage "SISTEMA", "Historial limpiado. Listo para una nueva consulta."
  End If

End Sub

Public Sub AppendChatMessage(ByVal Sender As String, ByVal Message As String)
  On Error Resume Next
  Dim timeStr     As String
  Dim headerText  As String
  Dim headerColor As Long
  Dim bodyColor   As Long
  Dim sUpper      As String
  Dim wasLocked   As Boolean
  Dim hWndChat    As Long
  hWndChat = txtChat.hWnd

  If hWndChat <> 0 Then SendMessage hWndChat, WM_SETREDRAW, 0, ByVal 0&
  wasLocked = txtChat.Locked

  If wasLocked Then txtChat.Locked = False
  timeStr = Format$(Now, "hh:nn:ss")
  headerText = "=== [" & timeStr & "] " & UCase$(Sender) & " ===" & vbCrLf
  sUpper = UCase$(Sender)

  ' Asignar colores segun la naturaleza del mensaje
  Select Case sUpper

    Case "ERROR", "ERROR IA"
      headerColor = &HFF&       ' Rojo brillante
      bodyColor = &H2020C0       ' Rojo oscuro

    Case "AVISO", "ADVERTENCIA", "SERVICIO"
      headerColor = &H80FF&     ' Naranja (&H000080FF&)
      bodyColor = &H303030      ' Gris oscuro

    Case "PROPUESTA", "DIFF", "CAMBIOS"
      headerColor = &HFF0000    ' Azul
      bodyColor = &H800000      ' Azul marino

    Case "EXITO", "SISTEMA"
      headerColor = &H8000&     ' Verde oscuro
      bodyColor = &H0&

    Case "USUARIO"
      headerColor = &H800000    ' Azul marino
      bodyColor = &H0&

    Case Else

      If InStr(sUpper, "CONTEXTO") > 0 Then
        headerColor = &HC04000 ' Azul acero
        bodyColor = &H404040
      ElseIf InStr(sUpper, "ASISTENTE") > 0 Then
        headerColor = &H404040 ' Gris grafito
        bodyColor = &H0&
      Else
        headerColor = &H0&
        bodyColor = &H0&
      End If

  End Select

  ' Si ya hay texto, agregar doble salto previo
  If Len(txtChat.Text) > 0 Then
    txtChat.SelStart = Len(txtChat.Text)
    txtChat.SelLength = 0
    txtChat.SelText = vbCrLf & vbCrLf
  End If

  ' 1. Insertar Cabecera en Negrita (Bold) y con Color Especifico
  txtChat.SelStart = Len(txtChat.Text)
  txtChat.SelLength = 0
  txtChat.SelBold = True
  txtChat.SelColor = headerColor
  txtChat.SelFontName = "Segoe UI"
  txtChat.SelFontSize = 9
  txtChat.SelText = headerText
  ' 2. Insertar Cuerpo del Mensaje
  txtChat.SelStart = Len(txtChat.Text)
  txtChat.SelLength = 0
  txtChat.SelBold = False
  txtChat.SelColor = bodyColor

  If InStr(Message, "Sub ") > 0 Or InStr(Message, "Function ") > 0 Or InStr(Message, "Dim ") > 0 Or InStr(Message, "Private ") > 0 Then
    txtChat.SelFontName = "Consolas"
  Else
    txtChat.SelFontName = "Segoe UI"
  End If

  txtChat.SelFontSize = 9
  txtChat.SelText = Message
  ' Desplazar automaticamente al final del chat
  txtChat.SelStart = Len(txtChat.Text)

  If wasLocked Then txtChat.Locked = True
  If hWndChat <> 0 Then
    SendMessage hWndChat, WM_SETREDRAW, 1, ByVal 0&
    RedrawWindow hWndChat, 0&, 0&, RDW_INVALIDATE Or RDW_UPDATENOW Or RDW_NOERASE
  End If

End Sub

Private Sub UpdateStreamingText(ByVal FullGeneratedText As String)
  On Error Resume Next
  Dim wasLocked       As Boolean
  Dim currentTotalLen As Long
  Dim hWndChat        As Long
  Dim newChunk        As String

  If m_StreamingStartPos < 0 Then Exit Sub
  If FullGeneratedText = m_LastRenderedText Then Exit Sub
  hWndChat = txtChat.hWnd

  If hWndChat <> 0 Then SendMessage hWndChat, WM_SETREDRAW, 0, ByVal 0&
  wasLocked = txtChat.Locked

  If wasLocked Then txtChat.Locked = False

  ' Caso 1: Primera actualizacion (reemplazar placeholder 'Generando respuesta...')
  If m_LastRenderedText = "Generando respuesta..." Or Len(m_LastRenderedText) = 0 Then
    currentTotalLen = Len(txtChat.Text)

    If currentTotalLen >= m_StreamingStartPos Then
      txtChat.SelStart = m_StreamingStartPos
      txtChat.SelLength = currentTotalLen - m_StreamingStartPos
      txtChat.SelBold = False
      txtChat.SelColor = &H0&

      If InStr(FullGeneratedText, "Sub ") > 0 Or InStr(FullGeneratedText, "Function ") > 0 Then
        txtChat.SelFontName = "Consolas"
      Else
        txtChat.SelFontName = "Segoe UI"
      End If

      txtChat.SelFontSize = 9
      txtChat.SelText = FullGeneratedText
      txtChat.SelStart = Len(txtChat.Text)
      m_LastRenderedText = FullGeneratedText
    End If

    ' Caso 2: Streaming incremental O(1) appending sin tocar el texto previo
  ElseIf Len(FullGeneratedText) > Len(m_LastRenderedText) And Left$(FullGeneratedText, Len(m_LastRenderedText)) = m_LastRenderedText Then
    newChunk = Mid$(FullGeneratedText, Len(m_LastRenderedText) + 1)

    If Len(newChunk) > 0 Then
      txtChat.SelStart = Len(txtChat.Text)
      txtChat.SelLength = 0
      txtChat.SelText = newChunk
      txtChat.SelStart = Len(txtChat.Text)
      m_LastRenderedText = FullGeneratedText
    End If

    ' Caso 3: Modificacion completa
  Else
    currentTotalLen = Len(txtChat.Text)

    If currentTotalLen >= m_StreamingStartPos Then
      txtChat.SelStart = m_StreamingStartPos
      txtChat.SelLength = currentTotalLen - m_StreamingStartPos
      txtChat.SelText = FullGeneratedText
      txtChat.SelStart = Len(txtChat.Text)
      m_LastRenderedText = FullGeneratedText
    End If
  End If

  If wasLocked Then txtChat.Locked = True
  If hWndChat <> 0 Then
    SendMessage hWndChat, WM_SETREDRAW, 1, ByVal 0&
    RedrawWindow hWndChat, 0&, 0&, RDW_INVALIDATE Or RDW_UPDATENOW Or RDW_NOERASE
  End If

End Sub
