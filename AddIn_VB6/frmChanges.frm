VERSION 5.00
Begin VB.Form frmChanges 
   Caption         =   "Revisión de Cambios de Código por VB6 AI Assistant"
   ClientHeight    =   7605
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   10605
   Icon            =   "frmChanges.frx":0000
   LinkTopic       =   "Form1"
   ScaleHeight     =   7605
   ScaleWidth      =   10605
   StartUpPosition =   2  'CenterScreen
   Begin VB.Frame fraHeader 
      Caption         =   " Información de la Propuesta "
      Height          =   975
      Left            =   120
      TabIndex        =   0
      Top             =   120
      Width           =   10335
      Begin VB.Label lblTarget 
         Caption         =   "Destino: Procedimiento activo"
         BeginProperty Font 
            Name            =   "Tahoma"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   160
         TabIndex        =   1
         Top             =   280
         Width           =   6200
      End
      Begin VB.Label lblRisk 
         Alignment       =   1  'Right Justify
         Caption         =   "Riesgo: [BAJO]"
         BeginProperty Font 
            Name            =   "Tahoma"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00008000&
         Height          =   255
         Left            =   6500
         TabIndex        =   2
         Top             =   280
         Width           =   3600
      End
      Begin VB.Label lblDescription 
         Caption         =   "Descripcion de la modificacion sugerida por el asistente de IA."
         ForeColor       =   &H00404040&
         Height          =   375
         Left            =   160
         TabIndex        =   3
         Top             =   540
         Width           =   9900
      End
   End
   Begin VB6AIAssistant.TextBoxW txtOriginal 
      Height          =   5100
      Left            =   120
      TabIndex        =   6
      Top             =   1500
      Width           =   5050
      _ExtentX        =   8916
      _ExtentY        =   8996
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "Courier New"
         Size            =   9
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      BackColor       =   15790320
      Locked          =   -1  'True
      MultiLine       =   -1  'True
      ScrollBars      =   3
   End
   Begin VB6AIAssistant.TextBoxW txtProposed 
      Height          =   5100
      Left            =   5300
      TabIndex        =   7
      Top             =   1500
      Width           =   5150
      _ExtentX        =   9075
      _ExtentY        =   8996
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "Courier New"
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
   End
   Begin VB.CommandButton cmdApprove 
      Caption         =   "&Aprobar y Aplicar al IDE"
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
      Height          =   420
      Left            =   7800
      TabIndex        =   8
      Top             =   6900
      Width           =   2655
   End
   Begin VB.CommandButton cmdReject 
      Cancel          =   -1  'True
      Caption         =   "&Rechazar"
      Height          =   420
      Left            =   6360
      TabIndex        =   9
      Top             =   6900
      Width           =   1335
   End
   Begin VB.CommandButton cmdCopy 
      Caption         =   "&Copiar Codigo"
      Height          =   420
      Left            =   120
      TabIndex        =   10
      Top             =   6900
      Width           =   1695
   End
   Begin VB.CommandButton cmdUnified 
      Caption         =   "Ver &Diff Unificado"
      Height          =   420
      Left            =   1920
      TabIndex        =   11
      Top             =   6900
      Width           =   1815
   End
   Begin VB.Label lblOriginal 
      Caption         =   "Codigo Original (Actual en el Editor):"
      BeginProperty Font 
         Name            =   "Tahoma"
         Size            =   8.25
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   255
      Left            =   120
      TabIndex        =   4
      Top             =   1200
      Width           =   5000
   End
   Begin VB.Label lblProposed 
      Caption         =   "Codigo Sugerido por IA:"
      BeginProperty Font 
         Name            =   "Tahoma"
         Size            =   8.25
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00800000&
      Height          =   255
      Left            =   5300
      TabIndex        =   5
      Top             =   1200
      Width           =   5000
   End
End
Attribute VB_Name = "frmChanges"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private m_ActionID       As String

Private m_TargetFile     As String

Private m_TargetProc     As String

Private m_ActionType     As String

Private m_OriginalCode   As String

Private m_ProposedCode   As String

Private m_DiffUnified    As String

Private m_RiskLevel      As String

Private m_Approved       As Boolean

Private m_ShowingUnified As Boolean
Public Function ShowProposal(ByVal ActionID As String, _
   ByVal TargetFile As String, _
   ByVal TargetProc As String, _
   ByVal OriginalCode As String, _
   ByVal ProposedCode As String, _
   ByVal DiffUnified As String, _
   ByVal RiskLevel As String, _
   ByVal Description As String, _
   ByVal ActionType As String) As Boolean
  On Error GoTo ErrorHandler
  m_ActionID = ActionID
  m_TargetFile = TargetFile
  m_TargetProc = TargetProc
  m_OriginalCode = OriginalCode
  m_ProposedCode = ProposedCode
  m_DiffUnified = DiffUnified
  m_RiskLevel = UCase$(RiskLevel)
  m_ActionType = ActionType
  m_Approved = False
  m_ShowingUnified = False
  ' Configurar etiquetas informativas
  If Len(TargetProc) > 0 Then
    lblTarget.Caption = "Destino: Procedimiento '" & TargetProc & "' en " & TargetFile
  Else
    lblTarget.Caption = "Destino: " & TargetFile
  End If
  lblDescription.Caption = Description
  ' Badge de nivel de riesgo
  Select Case m_RiskLevel
    Case "LOW"
      lblRisk.Caption = "Nivel de Riesgo: [BAJO]"
      lblRisk.ForeColor = &H8000& ' Verde
    Case "MEDIUM"
      lblRisk.Caption = "Nivel de Riesgo: [MEDIO]"
      lblRisk.ForeColor = &H808000 ' Amarillo/Naranja
    Case "HIGH"
      lblRisk.Caption = "Nivel de Riesgo: [ALTO]"
      lblRisk.ForeColor = &HFF& ' Rojo
    Case Else
      lblRisk.Caption = "Nivel de Riesgo: [INFO]"
      lblRisk.ForeColor = &H800000
  End Select
  ' Llenar cuadros de texto
  txtOriginal.Text = OriginalCode
  txtProposed.Text = ProposedCode
  ' Mostrar modalmente
  Me.Show vbModal
  ShowProposal = m_Approved
  Exit Function
ErrorHandler:
  MsgBox "Error mostrando propuesta de cambios: " & Err.Description, vbCritical, APP_TITLE
  ShowProposal = False
End Function

Private Sub Form_Resize()

  On Error Resume Next

  Dim w As Single, h As Single, halfW As Single

  w = Me.ScaleWidth
  h = Me.ScaleHeight

  If w < 6000 Or h < 4000 Then Exit Sub
  fraHeader.Width = w - 240
  lblDescription.Width = fraHeader.Width - 300
  lblRisk.Left = fraHeader.Width - lblRisk.Width - 200
  halfW = (w - 360) / 2
  lblOriginal.Left = 120
  lblOriginal.Width = halfW
  lblProposed.Left = 120 + halfW + 120
  lblProposed.Width = halfW
  txtOriginal.Left = 120
  txtOriginal.Width = halfW
  txtOriginal.Height = h - txtOriginal.Top - 800
  txtProposed.Left = lblProposed.Left
  txtProposed.Width = halfW
  txtProposed.Height = txtOriginal.Height
  cmdCopy.Top = h - 600
  cmdUnified.Top = cmdCopy.Top
  cmdReject.Top = cmdCopy.Top
  cmdApprove.Top = cmdCopy.Top
  cmdApprove.Left = w - cmdApprove.Width - 120
  cmdReject.Left = cmdApprove.Left - cmdReject.Width - 120
End Sub

Private Sub cmdApprove_Click()

  On Error GoTo ErrorHandler

  Dim projName    As String, projPath As String

  Dim jsonPayload As String

  Dim resp        As String

  Dim status      As Long

  Dim success     As Boolean

  Dim applyOk     As Boolean

  Call GetActiveProjectInfo(projName, projPath)
  ' 1. Solicitar ejecucion y backup al servicio local
  jsonPayload = "{" & JsonPropString("action_id", m_ActionID) & ", " & JsonPropString("project_vbp", projPath) & ", " & JsonPropString("file_path", m_TargetFile) & ", " & JsonPropString("original_code", m_OriginalCode) & ", " & JsonPropBool("create_backup", True) & "}"
  success = HttpPost(DEFAULT_SERVICE_URL & "/api/v1/actions/execute", jsonPayload, resp, status)

  If Not success Or status <> 200 Then
    MsgBox "Advertencia: No fue posible registrar el backup en el servicio local." & vbCrLf & "Respuesta: " & resp, vbExclamation, APP_TITLE
  End If

  ' 2. Aplicar las modificaciones al IDE segun el tipo de accion
  Select Case m_ActionType

    Case "MODIFY_PROCEDURE"

      If Len(m_TargetProc) > 0 Then
        applyOk = ApplyProcedureChange(m_TargetProc, m_ProposedCode)
      Else
        applyOk = ApplyModuleReplacement(m_ProposedCode)
      End If

    Case "REPLACE_MODULE"
      applyOk = ApplyModuleReplacement(m_ProposedCode)

    Case "CREATE_COMPONENT"
      applyOk = CreateNewVBComponent(1, m_TargetFile, m_ProposedCode)

    Case Else

      If Len(m_TargetProc) > 0 Then
        applyOk = ApplyProcedureChange(m_TargetProc, m_ProposedCode)
      Else
        applyOk = ApplyModuleReplacement(m_ProposedCode)
      End If

  End Select

  If applyOk Then
    MsgBox "Los cambios han sido aplicados con exito en el editor de VB6.", vbInformation, APP_TITLE
    m_Approved = True
    Unload Me
  Else
    MsgBox "Ocurrio un error al aplicar los cambios en el editor de VB6.", vbCritical, APP_TITLE
  End If

  Exit Sub

ErrorHandler:
  MsgBox "Error al aprobar cambios: " & Err.Description, vbCritical, APP_TITLE
End Sub

Private Sub cmdReject_Click()
  m_Approved = False
  Unload Me
End Sub

Private Sub cmdCopy_Click()

  On Error Resume Next

  Clipboard.Clear
  Clipboard.SetText m_ProposedCode
  MsgBox "Codigo propuesto copiado al portapapeles.", vbInformation, APP_TITLE
End Sub

Private Sub cmdUnified_Click()

  On Error Resume Next

  If Not m_ShowingUnified Then
    ' Cambiar a vista de Diff Unificado
    txtOriginal.Text = m_DiffUnified
    lblOriginal.Caption = "Diff Unificado (Formato Patch):"
    cmdUnified.Caption = "Ver &Lado a Lado"
    m_ShowingUnified = True
  Else
    ' Restaurar vista lado a lado
    txtOriginal.Text = m_OriginalCode
    lblOriginal.Caption = "Codigo Original (Actual en el Editor):"
    cmdUnified.Caption = "Ver &Diff Unificado"
    m_ShowingUnified = False
  End If

End Sub
