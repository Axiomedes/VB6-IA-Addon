import os

base_dir = r"d:\Programming\Antigravity\VB6 IA Addon\AddIn_VB6"



dsr_content = """VERSION 5.00

   ClientHeight    =   9000

   ClientTop       =   0

   _ExtentX        =   15875

   _Version        =   393216

   DisplayName     =   "VB6 AI Assistant"

   AppVer          =   "Visual Basic 98 (ver 6.0)"

   LoadBehavior    =   5

   CmdLineSupport  =   -1  'True

Attribute VB_Name = "Connect"

Attribute VB_Creatable = True

Attribute VB_Exposed = True



' VB6 AI Assistant - Add-In Designer (Connect.Dsr)

' ==============================================================================

Private m_VBE                   As VBIDE.VBE

Private m_AIMenuItem            As CommandBarControl

Private WithEvents ctlAssistant As CommandBarEvents





Private Sub AddinInstance_OnConnection(ByVal Application As Object, ByVal ConnectMode As AddInDesignerObjects.ext_ConnectMode, ByVal AddInInst As Object, custom() As Variant)

    

    Set m_VBE = Application

    Set g_VBInstance = Application

    ' Crear el comando de menu en la barra del IDE

    Exit Sub

ErrorHandler:

End Sub

' Evento de desconexion

    On Error Resume Next

    ' Cerrar formulario si esta abierto

        If Not mfrmAIAssistant Is Nothing Then

            Set mfrmAIAssistant = Nothing

        FormDisplayed = False

    

    Set ctlAssistant = Nothing

        m_AIMenuItem.Delete

    End If

    Set m_AddInInst = Nothing

    Set g_VBInstance = Nothing



    On Error GoTo ErrorHandler

    Dim cmdNew As CommandBarControl

    ' Localizar barra de menu (compatible con versiones en ingles, espanol e internacional)

    Set cbMenu = m_VBE.CommandBars("Add-Ins")

    If cbMenu Is Nothing Then Set cbMenu = m_VBE.CommandBars(1) ' MenuBar principal

    

    

    Set cmdNew = cbMenu.Controls.Add(msoControlButton)

    cmdNew.BeginGroup = True

    ' Enlazar eventos de clic

    Set m_AIMenuItem = cmdNew

    

    Debug.Print "Error creando menu de VB6 AI Assistant: " & Err.Description



    On Error GoTo ErrorHandler

    handled = True

ErrorHandler:

End Sub

Public Sub ShowAssistant()

    If mfrmAIAssistant Is Nothing Then

        Set mfrmAIAssistant.VBInstance = m_VBE

    End If

    FormDisplayed = True

    Exit Sub

    MsgBox "Error al mostrar la interfaz: " & Err.Description, vbCritical, "VB6 AI Assistant"



    On Error Resume Next

        Unload mfrmAIAssistant

    End If

End Sub

Public Property Get VBE() As VBIDE.VBE

End Property

Public Property Get AddInInst() As Object

End Property



vbp_content = """Type=OleDll

Reference=*\\G{2DF8D04C-5BFA-101B-BDE5-00AA0044DE52}#2.0#0#..\\..\\..\\..\\..\\..\\Program Files (x86)\\Common Files\\Microsoft Shared\\OFFICE15\\MSO.DLL#Microsoft Office 8.0 Object Library

Reference=*\\G{EF404E00-EDA6-101A-8DAF-00DD010F7EBB}#5.3#0#..\\..\\..\\..\\..\\..\\Program Files (x86)\\Microsoft Visual Studio\\VB98\\VB6EXT.OLB#Microsoft Visual Basic 6.0 Extensibility

Module=modMain; modMain.bas

Startup="(None)"

Title="VB6AIAssistant"

Command32=""

HelpContextID="0"

CompatibleMode="0"

MinorVer=0

AutoIncrementVer=0

VersionCompanyName="Antigravity"

OptimizationType=0

CodeViewDebugInfo=0

BoundsCheck=0

FlPointCheck=0

UnroundedFP=0

Unattended=0

ThreadPerObject=0

ThreadingModel=1



bas_content = """Attribute VB_Name = "modMain"



' VB6 AI Assistant - Modulo Principal de Utilidades e Integracion con VBIDE



Public g_ServiceURL As String

Public Const DEFAULT_SERVICE_URL As String = "http://127.0.0.1:8765"



Public Sub Main()

    g_ServiceURL = DEFAULT_SERVICE_URL



Public Function GetActiveCodeModule() As VBIDE.CodeModule

    If g_VBInstance Is Nothing Then Exit Function

    If Not g_VBInstance.ActiveCodePane Is Nothing Then

    ElseIf Not g_VBInstance.SelectedVBComponent Is Nothing Then

    End If



Public Function GetSelectedCode() As String

    Dim oPane As VBIDE.CodePane

    Dim sLine As Long, sCol As Long, eLine As Long, eCol As Long

    If g_VBInstance Is Nothing Then Exit Function

    If oPane Is Nothing Then Exit Function

    Set oMod = oPane.CodeModule

    

    If sLine > 0 And eLine >= sLine Then

    End If



Public Function GetActiveProcedure(ByRef OutProcName As String, ByRef OutProcKind As Long) As String

    Dim oPane As VBIDE.CodePane

    Dim sLine As Long, sCol As Long, eLine As Long, eCol As Long

    Dim pName As String

    

    OutProcKind = 0

    

    Set oPane = g_VBInstance.ActiveCodePane

    

    If oMod Is Nothing Then Exit Function

    oPane.GetSelection sLine, sCol, eLine, eCol

    

    If Len(Trim$(pName)) > 0 Then

        OutProcKind = pKind

        pCount = oMod.ProcCountLines(pName, pKind)

            GetActiveProcedure = oMod.Lines(pStart, pCount)

    End If



Public Function GetActiveModuleCode() As String

    Dim oMod As VBIDE.CodeModule

    

    If oMod Is Nothing Then Exit Function

    count = oMod.CountOfLines

        GetActiveModuleCode = oMod.Lines(1, count)

End Function

' Obtiene el nombre y ruta del proyecto activo

    On Error Resume Next

    OutProjPath = ""

    

    If g_VBInstance.ActiveVBProject Is Nothing Then Exit Function

    OutProjName = g_VBInstance.ActiveVBProject.Name

    GetActiveProjectInfo = True

"""

# 4. frmAIAssistant.frm

Begin VB.Form frmAIAssistant 

   ClientHeight    =   7680

   ClientTop       =   345

   Icon            =   0

   ScaleHeight     =   7680

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

         Text            =   "llama3:latest"

         Width           =   2175

      Begin VB.ComboBox cboContext 

         Left            =   6720

         TabIndex        =   3

         Width           =   2415

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

      Height          =   4575

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

      Top             =   5760

   End

      Caption         =   "&Enviar"

      BeginProperty Font 

         Size            =   8.25

         Weight          =   700

         Italic          =   0   'False

      EndProperty

      Left            =   7560

      Top             =   5760

   End

      Caption         =   "&Analizar Codigo"

      Left            =   7560

      Top             =   6280

   End

      Caption         =   "&Limpiar Chat"

      Left            =   7560

      Top             =   6800

   End

      Caption         =   "Estado: Listo | Conectado a VBIDE"

      Left            =   120

      Top             =   6840

   End

Attribute VB_Name = "frmAIAssistant"

Attribute VB_Creatable = False

Attribute VB_Exposed = False



Public Connect As Object

Private m_CurrentJobID As String



    On Error Resume Next

    ' Inicializar proveedores

        .Clear

        .AddItem "OpenAI"

        .AddItem "Google Gemini"

        .AddItem "Groq"

    End With

    ' Inicializar modelos para Ollama

        .Clear

        .AddItem "llama3:latest"

        .AddItem "qwen2.5-coder:7b"

    End With

    ' Inicializar opciones de contexto

        .Clear

        .AddItem "2. Procedimiento Actual"

        .AddItem "4. Proyecto Completo"

    End With

    ' Mensaje de bienvenida

                                "Integracion con VBIDE activa mediante AddIn Designer." & vbCrLf & _

                                "Escriba una solicitud o use 'Analizar Codigo' para comenzar."



    On Error Resume Next

    

    w = Me.ScaleWidth

    

    

    txtChat.Width = w - 240

    

    txtPrompt.Width = w - cmdSend.Width - 360

    cmdSend.Left = txtPrompt.Left + txtPrompt.Width + 120

    

    cmdAnalyze.Top = cmdSend.Top + cmdSend.Height + 60

    cmdClear.Left = cmdSend.Left

    

    lblStatus.Width = txtPrompt.Width



    On Error Resume Next

        Connect.FormDisplayed = False

End Sub

Private Sub cboProvider_Click()

    ' Actualizar lista sugerida de modelos segun el proveedor

    Select Case cboProvider.Text

            cboModel.AddItem "codellama:latest"

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

    prompt = Trim$(txtPrompt.Text)

        MsgBox "Por favor escriba una solicitud.", vbInformation, APP_TITLE

        Exit Sub

    

    contextCode = ExtractSelectedContext(contextType)

    ' Registrar mensaje del usuario en el chat

    If Len(contextCode) > 0 Then

    End If

    txtPrompt.Text = ""

    

    AppendChatMessage "ASISTENTE [Prototipo Fase 2]", _

        "Contexto capturado: " & contextType & " (" & Len(contextCode) & " caracteres)." & vbCrLf & _

        

    Exit Sub

    MsgBox "Error al enviar mensaje: " & Err.Description, vbCritical, APP_TITLE



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

                ' Fallback automatico a procedimiento o modulo si no selecciono texto

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

    

    txtChat.SelStart = Len(txtChat.Text)

"""

files = {

    "VB6AIAssistant.vbp": vbp_content,

    "frmAIAssistant.frm": frm_content,



    fpath = os.path.join(base_dir, fname)

    lines = content.split("\n")

    if not crlf_content.endswith("\r\n"):

    with open(fpath, "wb") as f:

    print(f"Successfully wrote {fname} ({len(crlf_content)} bytes, CRLF, UTF-8)")

# Remove old Connect.cls if exists

if os.path.exists(old_cls):

    print("Removed old Connect.cls")

