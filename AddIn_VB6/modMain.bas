Attribute VB_Name = "modMain"
Option Explicit

' ==============================================================================
' VB6 AI Assistant - Modulo Principal de Utilidades e Integracion con VBIDE
' ==============================================================================
Public g_VBInstance              As VBIDE.VBE

Public g_ServiceURL              As String

Public Const DEFAULT_SERVICE_URL As String = "http://127.0.0.1:8765"

Public Const APP_TITLE           As String = "VB6 AI Assistant"

' Punto de entrada opcional
Public Sub Main()

  On Error Resume Next

  g_ServiceURL = DEFAULT_SERVICE_URL
End Sub

' Obtiene el objeto CodeModule activo actualmente en el editor
Public Function GetActiveCodeModule() As VBIDE.CodeModule

  On Error Resume Next

  If g_VBInstance Is Nothing Then Exit Function
  If Not g_VBInstance.ActiveCodePane Is Nothing Then
    Set GetActiveCodeModule = g_VBInstance.ActiveCodePane.CodeModule
  ElseIf Not g_VBInstance.SelectedVBComponent Is Nothing Then
    Set GetActiveCodeModule = g_VBInstance.SelectedVBComponent.CodeModule
  End If

End Function

' Obtiene el texto del codigo REALMENTE seleccionado por el usuario en el editor
Public Function GetSelectedCode() As String

  On Error Resume Next

  Dim oPane As VBIDE.CodePane

  Dim oMod  As VBIDE.CodeModule

  Dim sLine As Long, sCol As Long, eLine As Long, eCol As Long

  GetSelectedCode = ""

  If g_VBInstance Is Nothing Then Exit Function
  Set oPane = g_VBInstance.ActiveCodePane

  If oPane Is Nothing Then Exit Function
  Set oMod = oPane.CodeModule

  If oMod Is Nothing Then Exit Function
  oPane.GetSelection sLine, sCol, eLine, eCol

  If sLine > 0 And eLine >= sLine Then

    ' Solo considerar selección si abarca ms de una línea o caracteres entre columnas
    If (sLine < eLine) Or (sLine = eLine And eCol > sCol) Then
      GetSelectedCode = oMod.Lines(sLine, (eLine - sLine + 1))
    End If
  End If

End Function

' Obtiene el nombre y cuerpo del procedimiento bajo el cursor activo
Public Function GetActiveProcedure(ByRef OutProcName As String, _
                                   ByRef OutProcKind As Long) As String

  On Error Resume Next

  Dim oPane  As VBIDE.CodePane

  Dim oMod   As VBIDE.CodeModule

  Dim sLine  As Long, sCol As Long, eLine As Long, eCol As Long

  Dim pKind  As vbext_ProcKind

  Dim pName  As String

  Dim pStart As Long, pCount As Long

  OutProcName = ""
  OutProcKind = 0
  GetActiveProcedure = ""

  If g_VBInstance Is Nothing Then Exit Function
  Set oPane = g_VBInstance.ActiveCodePane

  If oPane Is Nothing Then Exit Function
  Set oMod = oPane.CodeModule

  If oMod Is Nothing Then Exit Function
  oPane.GetSelection sLine, sCol, eLine, eCol

  If sLine <= 0 Then Exit Function
  pName = oMod.ProcOfLine(sLine, pKind)

  If Len(Trim$(pName)) > 0 Then
    OutProcName = pName
    OutProcKind = pKind
    pStart = oMod.ProcStartLine(pName, pKind)
    pCount = oMod.ProcCountLines(pName, pKind)

    If pStart > 0 And pCount > 0 Then
      GetActiveProcedure = oMod.Lines(pStart, pCount)
    End If
  End If

End Function

' Obtiene todo el codigo del modulo activo
Public Function GetActiveModuleCode() As String

  On Error Resume Next

  Dim oMod  As VBIDE.CodeModule

  Dim Count As Long

  Set oMod = GetActiveCodeModule()

  If oMod Is Nothing Then Exit Function
  Count = oMod.CountOfLines

  If Count > 0 Then
    GetActiveModuleCode = oMod.Lines(1, Count)
  End If

End Function

' Obtiene el nombre y ruta del proyecto activo
Public Function GetActiveProjectInfo(ByRef OutProjName As String, _
                                     ByRef OutProjPath As String) As Boolean

  On Error Resume Next

  OutProjName = ""
  OutProjPath = ""
  GetActiveProjectInfo = False

  If g_VBInstance Is Nothing Then Exit Function
  If g_VBInstance.ActiveVBProject Is Nothing Then Exit Function
  OutProjName = g_VBInstance.ActiveVBProject.Name
  OutProjPath = g_VBInstance.ActiveVBProject.FileName
  GetActiveProjectInfo = True
End Function
