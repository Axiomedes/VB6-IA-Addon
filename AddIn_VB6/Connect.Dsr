VERSION 5.00
Begin {AC0714F6-3D04-11D1-AE7D-00A0C90F26F4} Connect 
   ClientHeight    =   9000
   ClientLeft      =   0
   ClientTop       =   0
   ClientWidth     =   9000
   _ExtentX        =   15875
   _ExtentY        =   15875
   _Version        =   393216
   Description     =   "VB6 AI Assistant - Asistente Inteligente con IA para Visual Basic 6.0"
   DisplayName     =   "VB6 AI Assistant"
   AppName         =   "Visual Basic"
   AppVer          =   "Visual Basic 98 (ver 6.0)"
   LoadName        =   "Command Line / Startup"
   LoadBehavior    =   5
   RegLocation     =   "HKEY_CURRENT_USER\Software\Microsoft\Visual Basic\6.0"
   CmdLineSupport  =   -1  'True
End
Attribute VB_Name = "Connect"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = True
Option Explicit

' ==============================================================================
' VB6 AI Assistant - Add-In Designer (Connect.Dsr)
' Arquitectura oficial de inicio y gestion de ciclo de vida en VBIDE
' ==============================================================================
Private m_VBE                   As VBIDE.VBE

Private m_AddInInst             As Object

Private m_AIMenuItem            As CommandBarControl

Private mfrmAIAssistant         As frmAIAssistant

Private WithEvents ctlAssistant As CommandBarEvents
Attribute ctlAssistant.VB_VarHelpID = -1

Public FormDisplayed            As Boolean

' Evento de conexion invocado por el Add-In Designer
Private Sub AddinInstance_OnConnection(ByVal Application As Object, _
                                       ByVal ConnectMode As AddInDesignerObjects.ext_ConnectMode, _
                                       ByVal AddInInst As Object, _
                                       custom() As Variant)

  On Error GoTo ErrorHandler

  ' Guardar instancias VBE
  Set m_VBE = Application
  Set m_AddInInst = AddInInst
  Set g_VBInstance = Application
  ' Inicializar internacionalizacion
  Call InitI18N
  ' Crear el comando de menu en la barra del IDE
  Call CreateMenu

  Exit Sub

ErrorHandler:
  MsgBox "Error al iniciar VB6 AI Assistant: " & Err.Description, vbCritical, "VB6 AI Assistant"
End Sub

' Evento de desconexion
Private Sub AddinInstance_OnDisconnection(ByVal RemoveMode As AddInDesignerObjects.ext_DisconnectMode, _
                                          custom() As Variant)

  On Error Resume Next

  ' Cerrar formulario si esta abierto
  If FormDisplayed Then
    If Not mfrmAIAssistant Is Nothing Then
      Unload mfrmAIAssistant
      Set mfrmAIAssistant = Nothing
    End If

    FormDisplayed = False
  End If

  ' Limpiar eventos y controles de menu
  Set ctlAssistant = Nothing

  If Not m_AIMenuItem Is Nothing Then
    m_AIMenuItem.Delete
    Set m_AIMenuItem = Nothing
  End If

  Set m_AddInInst = Nothing
  Set m_VBE = Nothing
  Set g_VBInstance = Nothing
End Sub

Private Sub CreateMenu()

  On Error GoTo ErrorHandler

  Dim cbMenu As CommandBar

  Dim cmdNew As CommandBarControl

  ' Localizar barra de menu (compatible con versiones en ingles, espanol e internacional)
  On Error Resume Next

  Set cbMenu = m_VBE.CommandBars("Add-Ins")

  If cbMenu Is Nothing Then Set cbMenu = m_VBE.CommandBars("Complementos")
  If cbMenu Is Nothing Then Set cbMenu = m_VBE.CommandBars(1) ' MenuBar principal

  On Error GoTo ErrorHandler

  If cbMenu Is Nothing Then Exit Sub
  ' Agregar elemento de menu
  Set cmdNew = cbMenu.Controls.Add(msoControlButton)
  cmdNew.Caption = T("MENU_MAIN", "&VB6 AI Assistant...")
  cmdNew.BeginGroup = True
  ' Enlazar eventos de clic
  Set ctlAssistant = m_VBE.Events.CommandBarEvents(cmdNew)
  Set m_AIMenuItem = cmdNew

  Exit Sub

ErrorHandler:
  Debug.Print "Error creando menu de VB6 AI Assistant: " & Err.Description
End Sub

Private Sub ctlAssistant_Click(ByVal CommandBarControl As Object, _
                               Handled As Boolean, _
                               CancelDefault As Boolean)

  On Error GoTo ErrorHandler

  Call ShowAssistant
  Handled = True

  Exit Sub

ErrorHandler:
  MsgBox "Error al abrir la ventana del asistente: " & Err.Description, vbExclamation, "VB6 AI Assistant"
End Sub

Public Sub ShowAssistant()

  On Error GoTo ErrorHandler

  If mfrmAIAssistant Is Nothing Then
    Set mfrmAIAssistant = New frmAIAssistant
    Set mfrmAIAssistant.VBInstance = m_VBE
    Set mfrmAIAssistant.Connect = Me
  End If

  FormDisplayed = True
  mfrmAIAssistant.Show vbModeless

  Exit Sub

ErrorHandler:
  MsgBox "Error al mostrar la interfaz: " & Err.Description, vbCritical, "VB6 AI Assistant"
End Sub

Public Sub HideAssistant()

  On Error Resume Next

  If Not mfrmAIAssistant Is Nothing Then
    Unload mfrmAIAssistant
    Set mfrmAIAssistant = Nothing
  End If

  FormDisplayed = False
End Sub

Public Property Get VBE() As VBIDE.VBE
  Set VBE = m_VBE
End Property

Public Property Get AddInInst() As Object
  Set AddInInst = m_AddInInst
End Property
