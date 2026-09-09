VERSION 5.00
Begin VB.Form frmConfig 
   BorderStyle     =   3  'Fixed Dialog
   Caption         =   "Configuración de Proveedores de IA"
   ClientHeight    =   6600
   ClientLeft      =   45
   ClientTop       =   375
   ClientWidth     =   6855
   BeginProperty Font 
      Name            =   "Segoe UI"
      Size            =   9
      Charset         =   0
      Weight          =   400
      Underline       =   0   'False
      Italic          =   0   'False
      Strikethrough   =   0   'False
   EndProperty
   Icon            =   "frmConfig.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   6600
   ScaleWidth      =   6855
   ShowInTaskbar   =   0   'False
   StartUpPosition =   1  'CenterOwner
   Begin VB.Frame fraProvider 
      Caption         =   " Seleccionar Proveedor de Inteligencia Artificial "
      Height          =   855
      Left            =   120
      TabIndex        =   0
      Top             =   120
      Width           =   6615
      Begin VB.ComboBox cboProvider 
         Height          =   315
         Left            =   240
         Style           =   2  'Dropdown List
         TabIndex        =   1
         Top             =   340
         Width           =   6135
      End
   End
   Begin VB.Frame fraDetails 
      Caption         =   " Parámetros de Conexión y Autenticación "
      Height          =   4725
      Left            =   120
      TabIndex        =   2
      Top             =   1080
      Width           =   6615
      Begin VB.TextBox txtHost 
         Height          =   315
         Left            =   240
         TabIndex        =   4
         Text            =   "http://127.0.0.1:11434"
         Top             =   600
         Width           =   6135
      End
      Begin VB.TextBox txtApiKey 
         Height          =   315
         Left            =   240
         TabIndex        =   6
         Top             =   1260
         Width           =   6135
      End
      Begin VB.ComboBox cboModel 
         Height          =   315
         Left            =   240
         TabIndex        =   8
         Top             =   1950
         Width           =   4215
      End
      Begin VB.CommandButton cmdFetchModels 
         Caption         =   "&Obtener Modelos"
         Height          =   345
         Left            =   4560
         TabIndex        =   9
         Top             =   1930
         Width           =   1815
      End
      Begin VB.ComboBox cboLanguage 
         Height          =   345
         Left            =   180
         Style           =   2  'Dropdown List
         TabIndex        =   11
         Top             =   4125
         Width           =   4215
      End
      Begin VB.CommandButton cmdTest 
         Caption         =   "&Probar Conexión"
         Height          =   375
         Left            =   240
         TabIndex        =   12
         Top             =   2445
         Width           =   2055
      End
      Begin VB.Label lblLanguage 
         Caption         =   "Idioma de Interfaz / Language:"
         Height          =   255
         Left            =   180
         TabIndex        =   10
         Top             =   3870
         Width           =   4005
      End
      Begin VB.Label lblHost 
         Caption         =   "URL del Servidor Ollama (Local):"
         Height          =   255
         Left            =   240
         TabIndex        =   3
         Top             =   340
         Width           =   4000
      End
      Begin VB.Label lblApiKey 
         Caption         =   "Clave API (API Key del Proveedor):"
         Height          =   255
         Left            =   240
         TabIndex        =   5
         Top             =   1020
         Width           =   4000
      End
      Begin VB.Label lblModel 
         Caption         =   "Modelo por Defecto / Personalizado:"
         Height          =   255
         Left            =   240
         TabIndex        =   7
         Top             =   1710
         Width           =   4000
      End
      Begin VB.Label lblTestResult 
         BackStyle       =   0  'Transparent
         Caption         =   "Estado: Listo para probar conexión."
         Height          =   855
         Left            =   240
         TabIndex        =   14
         Top             =   2940
         Width           =   6135
         WordWrap        =   -1  'True
      End
   End
   Begin VB.CommandButton cmdSave 
      Caption         =   "&Guardar Configuración"
      Default         =   -1  'True
      BeginProperty Font 
         Name            =   "Segoe UI"
         Size            =   9
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   450
      Left            =   4500
      TabIndex        =   15
      Top             =   6000
      Width           =   2175
   End
   Begin VB.CommandButton cmdClose 
      Cancel          =   -1  'True
      Caption         =   "&Cerrar"
      Height          =   450
      Left            =   5640
      TabIndex        =   13
      Top             =   5250
      Width           =   1095
   End
End
Attribute VB_Name = "frmConfig"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Public SelectedProviderIndex As Long
Public SelectedModelName     As String

Private m_OllamaHost              As String

Private m_OpenRouterKey           As String

Private m_GroqKey                 As String

Private m_GeminiKey               As String

Private m_OpenAIKey               As String

Private m_ClaudeKey               As String

Private m_LastSelectedProviderIdx As Long


Public Sub ApplyI18N()
  On Error Resume Next
  Me.Caption = T("TITLE_CONFIG", "Configuración de Proveedores de IA")
  fraProvider.Caption = " " & T("LBL_PROVIDER_FRAME", "Seleccionar Proveedor de Inteligencia Artificial") & " "
  fraDetails.Caption = " " & T("LBL_CONFIG_DETAILS", "Parámetros de Conexión y Autenticación") & " "
  cmdFetchModels.Caption = "&" & T("BTN_FETCH_MODELS", "Obtener Modelos")
  cmdTest.Caption = "&" & T("BTN_TEST", "Probar Conexión")
  cmdSave.Caption = "&" & T("BTN_SAVE", "Guardar Configuración")
  cmdClose.Caption = "&" & T("BTN_CLOSE", "Cerrar")
  lblModel.Caption = T("LBL_MODEL", "Modelo por Defecto / Personalizado:")
  lblLanguage.Caption = T("LBL_LANGUAGE", "Idioma de Interfaz / Language:")
  
  If cboProvider.ListIndex = 0 Then
    lblHost.Caption = T("LBL_OLLAMA_HOST", "URL del Servidor Ollama (Local):")
  Else
    lblApiKey.Caption = T("LBL_API_KEY", "Clave API (API Key del Proveedor):")
  End If
End Sub

Private Sub cboLanguage_Click()
  On Error Resume Next
  Select Case cboLanguage.ListIndex
    Case 1: Call SetLanguage("es")
    Case 2: Call SetLanguage("en")
    Case Else: Call SetLanguage("auto")
  End Select
  Call ApplyI18N
End Sub

Private Sub Form_Load()

  On Error Resume Next
  ' Inicializar idiomas
  With cboLanguage
    .Clear
    .AddItem T("LANG_OPT_AUTO", "Auto (Detectar Sistema)")
    .AddItem "Español"
    .AddItem "English"
    If g_LanguageMode = "es" Then
      .ListIndex = 1
    ElseIf g_LanguageMode = "en" Then
      .ListIndex = 2
    Else
      .ListIndex = 0
    End If
  End With

  Call ApplyI18N


  m_LastSelectedProviderIdx = -1

  With cboProvider
    .Clear
    .AddItem "Ollama (100% Local y Gratuito)"
    .AddItem "OpenRouter (Modelos Libres y Comerciales)"
    .AddItem "Google Gemini (Google AI Studio)"
    .AddItem "Groq (Ultra-Rápido)"
    .AddItem "OpenAI (GPT-4o / o3-mini)"
    .AddItem "Anthropic Claude (Sonnet / Haiku)"
  End With

  Call LoadCurrentConfig
  cboProvider.ListIndex = 0
End Sub

Private Sub LoadCurrentConfig()

  On Error Resume Next

  Dim resp    As String

  Dim status  As Long

  Dim success As Boolean

  m_OllamaHost = "http://127.0.0.1:11434"
  m_OpenRouterKey = ""
  m_GroqKey = ""
  m_GeminiKey = ""
  m_OpenAIKey = ""
  m_ClaudeKey = ""
  success = HttpGet(DEFAULT_SERVICE_URL & "/api/v1/config", resp, status)

  If success And status = 200 Then
    m_OllamaHost = JsonGetString(resp, "ollama_host")

    If Len(m_OllamaHost) = 0 Then m_OllamaHost = "http://127.0.0.1:11434"
    m_OpenRouterKey = JsonGetString(resp, "openrouter_api_key")
    m_GroqKey = JsonGetString(resp, "groq_api_key")
    m_GeminiKey = JsonGetString(resp, "gemini_api_key")
    m_OpenAIKey = JsonGetString(resp, "openai_api_key")
    m_ClaudeKey = JsonGetString(resp, "anthropic_api_key")
  End If

End Sub

Private Sub SaveCurrentProviderToMemory()

  On Error Resume Next

  Select Case m_LastSelectedProviderIdx

    Case 0 ' Ollama
      m_OllamaHost = Trim$(txtHost.Text)

    Case 1 ' OpenRouter
      m_OpenRouterKey = Trim$(txtApiKey.Text)

    Case 2 ' Gemini
      m_GeminiKey = Trim$(txtApiKey.Text)

    Case 3 ' Groq
      m_GroqKey = Trim$(txtApiKey.Text)

    Case 4 ' OpenAI
      m_OpenAIKey = Trim$(txtApiKey.Text)

    Case 5 ' Claude
      m_ClaudeKey = Trim$(txtApiKey.Text)
  End Select

End Sub

Private Sub cboProvider_Click()

  On Error Resume Next

  If m_LastSelectedProviderIdx >= 0 Then
    Call SaveCurrentProviderToMemory
  End If

  m_LastSelectedProviderIdx = cboProvider.ListIndex
  lblTestResult.Caption = "Listo para probar conexión con " & cboProvider.Text
  lblTestResult.ForeColor = &H0&
  cboModel.Clear

  Select Case cboProvider.ListIndex

    Case 0 ' Ollama
      lblHost.Visible = True
      txtHost.Visible = True
      lblApiKey.Visible = False
      txtApiKey.Visible = False
      txtHost.Text = m_OllamaHost
      txtApiKey.Text = ""
      cboModel.AddItem "qwen3:1.7b"
      cboModel.AddItem "VB6-IA:latest"
      cboModel.AddItem "hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0"
      cboModel.AddItem "codellama"
      cboModel.AddItem "llama3"
      cboModel.ListIndex = 0

    Case 1 ' OpenRouter
      lblHost.Visible = False
      txtHost.Visible = False
      lblApiKey.Visible = True
      txtApiKey.Visible = True
      lblApiKey.Caption = "Clave API de OpenRouter (sk-or-v1-...):"
      txtApiKey.Text = m_OpenRouterKey
      cboModel.AddItem "openrouter/free"
      cboModel.AddItem "nvidia/nemotron-3.5-lightning:free"
      cboModel.AddItem "google/gemma-4-31b-it:free"
      cboModel.AddItem "google/gemma-4-26b-a4b-it:free"
      cboModel.AddItem "cohere/north-mini-code:free"
      cboModel.AddItem "poolside/laguna-s-2.1:free"
      cboModel.AddItem "thinkingmachines/inkling:free"
      cboModel.ListIndex = 0

    Case 2 ' Gemini
      lblHost.Visible = False
      txtHost.Visible = False
      lblApiKey.Visible = True
      txtApiKey.Visible = True
      lblApiKey.Caption = "Clave API de Google AI Studio (AIzaSy...):"
      txtApiKey.Text = m_GeminiKey
      cboModel.AddItem "gemini-flash-latest"
      cboModel.AddItem "gemini-pro-latest"
      cboModel.AddItem "gemini-3.6-flash"
      cboModel.AddItem "gemini-3.5-flash"
      cboModel.AddItem "gemini-2.5-flash-lite"
      cboModel.ListIndex = 0

    Case 3 ' Groq
      lblHost.Visible = False
      txtHost.Visible = False
      lblApiKey.Visible = True
      txtApiKey.Visible = True
      lblApiKey.Caption = "Clave API de Groq (gsk_...):"
      txtApiKey.Text = m_GroqKey
      cboModel.AddItem "llama-3.3-70b-versatile"
      cboModel.AddItem "llama-3.1-8b-instant"
      cboModel.AddItem "deepseek-r1-distill-llama-70b"
      cboModel.ListIndex = 0

    Case 4 ' OpenAI
      lblHost.Visible = False
      txtHost.Visible = False
      lblApiKey.Visible = True
      txtApiKey.Visible = True
      lblApiKey.Caption = "Clave API de OpenAI (sk-...):"
      txtApiKey.Text = m_OpenAIKey
      cboModel.AddItem "gpt-4o-mini"
      cboModel.AddItem "gpt-4o"
      cboModel.AddItem "o3-mini"
      cboModel.ListIndex = 0

    Case 5 ' Claude
      lblHost.Visible = False
      txtHost.Visible = False
      lblApiKey.Visible = True
      txtApiKey.Visible = True
      lblApiKey.Caption = "Clave API de Anthropic Claude (sk-ant-...):"
      txtApiKey.Text = m_ClaudeKey
      cboModel.AddItem "claude-3-5-sonnet-20241022"
      cboModel.AddItem "claude-3-5-haiku-20241022"
      cboModel.ListIndex = 0
  End Select

End Sub

Private Function GetProviderKey() As String

  Select Case cboProvider.ListIndex

    Case 0: GetProviderKey = "ollama"

    Case 1: GetProviderKey = "openrouter"

    Case 2: GetProviderKey = "gemini"

    Case 3: GetProviderKey = "groq"

    Case 4: GetProviderKey = "openai"

    Case 5: GetProviderKey = "claude"

    Case Else: GetProviderKey = "ollama"
  End Select

End Function

Private Sub cmdFetchModels_Click()

  On Error GoTo ErrorHandler

  Dim pKey      As String

  Dim resp      As String

  Dim status    As Long

  Dim success   As Boolean

  Dim modelsCol As Collection

  Dim idx       As Long

  pKey = GetProviderKey()
  lblTestResult.ForeColor = &H800000 ' Azul marino
  lblTestResult.Caption = "Consultando lista dinámica de modelos para " & pKey & "..."
  DoEvents
  success = HttpGet(DEFAULT_SERVICE_URL & "/api/v1/providers/" & pKey & "/models", resp, status)

  If success And status = 200 Then
    Set modelsCol = JsonGetArrayStrings(resp, "models")

    If Not modelsCol Is Nothing Then
      If modelsCol.Count > 0 Then
        cboModel.Clear

        For idx = 1 To modelsCol.Count
          cboModel.AddItem modelsCol(idx)
        Next idx

        cboModel.ListIndex = 0
        lblTestResult.ForeColor = &H8000& ' Verde
        lblTestResult.Caption = "[OK] Se cargaron " & modelsCol.Count & " modelos disponibles en vivo."

        Exit Sub

      End If
    End If
  End If

  lblTestResult.ForeColor = &H80FF& ' Naranja
  lblTestResult.Caption = "Aviso: No se pudo obtener la lista remota de modelos. Verifique su clave o conexión."

  Exit Sub

ErrorHandler:
  lblTestResult.ForeColor = &HFF&
  lblTestResult.Caption = "Error al consultar modelos: " & Err.Description
End Sub

Private Sub cmdTest_Click()

  On Error GoTo ErrorHandler

  Dim pKey        As String

  Dim jsonPayload As String

  Dim resp        As String

  Dim status      As Long

  Dim success     As Boolean

  Dim testMsg     As String

  Dim isOk        As Boolean

  Call SaveCurrentProviderToMemory
  pKey = GetProviderKey()
  lblTestResult.ForeColor = &H800000
  lblTestResult.Caption = "Probando conexión con " & cboProvider.Text & "..."
  DoEvents
  jsonPayload = "{" & JsonPropString("api_key", txtApiKey.Text) & ", " & JsonPropString("host", txtHost.Text) & "}"
  success = HttpPost(DEFAULT_SERVICE_URL & "/api/v1/providers/" & pKey & "/test", jsonPayload, resp, status)

  If success And status = 200 Then
    isOk = JsonGetBool(resp, "success")
    testMsg = JsonGetString(resp, "message")

    If isOk Then
      lblTestResult.ForeColor = &H8000& ' Verde
      lblTestResult.Caption = "[OK] " & testMsg

      Dim modelsCol As Collection

      Dim idx       As Long

      Set modelsCol = JsonGetArrayStrings(resp, "models")

      If Not modelsCol Is Nothing Then
        If modelsCol.Count > 0 Then
          cboModel.Clear

          For idx = 1 To modelsCol.Count
            cboModel.AddItem modelsCol(idx)
          Next idx

          cboModel.ListIndex = 0
        End If
      End If

    Else
      lblTestResult.ForeColor = &HFF& ' Rojo
      lblTestResult.Caption = "[X] " & testMsg
    End If

  Else
    lblTestResult.ForeColor = &HFF& ' Rojo
    lblTestResult.Caption = "[X] Error de conexión HTTP con el servicio local (Status " & status & "): " & resp
  End If

  Exit Sub

ErrorHandler:
  lblTestResult.ForeColor = &HFF&
  lblTestResult.Caption = "Error al probar conexión: " & Err.Description
End Sub

Private Sub cmdSave_Click()

  On Error GoTo ErrorHandler

  Dim jsonPayload As String

  Dim resp        As String

  Dim status      As Long

  Dim success     As Boolean

  Call SaveCurrentProviderToMemory
  jsonPayload = "{" & JsonPropString("ollama_host", m_OllamaHost) & ", " & JsonPropString("openrouter_api_key", m_OpenRouterKey) & ", " & JsonPropString("gemini_api_key", m_GeminiKey) & ", " & JsonPropString("groq_api_key", m_GroqKey) & ", " & JsonPropString("openai_api_key", m_OpenAIKey) & ", " & JsonPropString("anthropic_api_key", m_ClaudeKey) & "}"
  success = HttpPost(DEFAULT_SERVICE_URL & "/api/v1/config", jsonPayload, resp, status)

  If success And status = 200 Then
    If cboLanguage.ListIndex = 1 Then
      Call SetLanguage("es")
    ElseIf cboLanguage.ListIndex = 2 Then
      Call SetLanguage("en")
    Else
      Call SetLanguage("auto")
    End If
    MsgBox T("MSG_CONFIG_SAVED", "Configuración guardada y recargada exitosamente."), vbInformation, T("TITLE_CONFIG", "Configuración")
    Unload Me
  Else
    MsgBox "No fue posible guardar la configuración: " & resp, vbCritical, "Error"
  End If

  Exit Sub

ErrorHandler:
  MsgBox "Error al guardar configuración: " & Err.Description, vbCritical, "Error"
End Sub

Private Sub cmdClose_Click()
  Unload Me
End Sub
