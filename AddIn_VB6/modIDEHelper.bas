Attribute VB_Name = "modIDEHelper"
Option Explicit

' ==============================================================================
' VB6 AI Assistant - Manejador de Extensibilidad e Inserción Segura en VBIDE
' ==============================================================================
' Aplica la sustitución de un procedimiento específico en el módulo de código activo
Public Function ApplyProcedureChange(ByVal TargetProcName As String, _
                                     ByVal NewCode As String) As Boolean

  On Error GoTo ErrorHandler

  Dim oMod   As VBIDE.CodeModule

  Dim pStart As Long, pCount As Long

  Dim pKind  As vbext_ProcKind

  ApplyProcedureChange = False
  Set oMod = GetActiveCodeModule()

  If oMod Is Nothing Then
    MsgBox "No hay un módulo de código activo en el editor.", vbExclamation, APP_TITLE

    Exit Function

  End If

  ' Localizar el procedimiento
  pKind = vbext_pk_Proc
  pStart = oMod.ProcStartLine(TargetProcName, pKind)
  pCount = oMod.ProcCountLines(TargetProcName, pKind)

  If pStart > 0 And pCount > 0 Then
    oMod.DeleteLines pStart, pCount
    oMod.InsertLines pStart, NewCode
    ApplyProcedureChange = True
  Else
    oMod.InsertLines oMod.CountOfLines + 1, vbCrLf & NewCode
    ApplyProcedureChange = True
  End If

  Exit Function

ErrorHandler:
  MsgBox "Error aplicando cambios al procedimiento '" & TargetProcName & "': " & Err.Description, vbCritical, APP_TITLE
  ApplyProcedureChange = False
End Function

' Reemplaza todo el contenido del módulo de código activo
Public Function ApplyModuleReplacement(ByVal NewCode As String) As Boolean

  On Error GoTo ErrorHandler

  Dim oMod As VBIDE.CodeModule

  ApplyModuleReplacement = False
  Set oMod = GetActiveCodeModule()

  If oMod Is Nothing Then
    MsgBox "No hay un módulo activo en el editor.", vbExclamation, APP_TITLE

    Exit Function

  End If

  If oMod.CountOfLines > 0 Then
    oMod.DeleteLines 1, oMod.CountOfLines
  End If

  oMod.InsertLines 1, NewCode
  ApplyModuleReplacement = True

  Exit Function

ErrorHandler:
  MsgBox "Error reemplazando contenido del módulo: " & Err.Description, vbCritical, APP_TITLE
  ApplyModuleReplacement = False
End Function

' Crea un nuevo componente (.bas, .cls o .frm) y lo añade al proyecto activo
Public Function CreateNewVBComponent(ByVal CompType As Long, _
                                     ByVal CompName As String, _
                                     ByVal InitialCode As String) As Boolean

  On Error GoTo ErrorHandler

  Dim oProj As VBIDE.VBProject

  Dim oComp As VBIDE.VBComponent

  CreateNewVBComponent = False

  If g_VBInstance Is Nothing Then Exit Function
  Set oProj = g_VBInstance.ActiveVBProject

  If oProj Is Nothing Then
    MsgBox "No hay un proyecto activo abierto en VB6.", vbExclamation, APP_TITLE

    Exit Function

  End If

  Set oComp = oProj.VBComponents.Add(CompType)

  If oComp Is Nothing Then Exit Function
  If Len(Trim$(CompName)) > 0 Then

    On Error Resume Next

    oComp.Name = CompName

    On Error GoTo ErrorHandler

  End If

  If Len(InitialCode) > 0 Then
    If oComp.CodeModule.CountOfLines > 0 Then
      oComp.CodeModule.DeleteLines 1, oComp.CodeModule.CountOfLines
    End If

    oComp.CodeModule.InsertLines 1, InitialCode
  End If

  CreateNewVBComponent = True

  Exit Function

ErrorHandler:
  MsgBox "Error creando nuevo componente en el proyecto: " & Err.Description, vbCritical, APP_TITLE
  CreateNewVBComponent = False
End Function

' Busca el código de un procedimiento por su nombre en todo el proyecto activo
Public Function FindProcedureCodeInProject(ByVal ProcName As String, _
                                           ByRef OutModuleName As String) As String

  On Error Resume Next

  Dim oProj         As VBIDE.VBProject

  Dim oComp         As VBIDE.VBComponent

  Dim oMod          As VBIDE.CodeModule

  Dim i             As Long

  Dim pStart        As Long, pCount As Long

  Dim pKind         As vbext_ProcKind

  Dim cleanProcName As String

  OutModuleName = ""
  FindProcedureCodeInProject = ""
  cleanProcName = Trim$(ProcName)

  If Len(cleanProcName) = 0 Then Exit Function
  If g_VBInstance Is Nothing Then Exit Function
  Set oProj = g_VBInstance.ActiveVBProject

  If oProj Is Nothing Then Exit Function
  ' 1. Buscar primero en el módulo activo
  Set oMod = GetActiveCodeModule()

  If Not oMod Is Nothing Then
    pKind = vbext_pk_Proc
    pStart = oMod.ProcStartLine(cleanProcName, pKind)
    pCount = oMod.ProcCountLines(cleanProcName, pKind)

    If pStart > 0 And pCount > 0 Then
      If Not g_VBInstance.SelectedVBComponent Is Nothing Then
        OutModuleName = g_VBInstance.SelectedVBComponent.Name
      End If

      FindProcedureCodeInProject = oMod.Lines(pStart, pCount)

      Exit Function

    End If
  End If

  ' 2. Buscar en todos los componentes del proyecto
  For i = 1 To oProj.VBComponents.Count
    Set oComp = oProj.VBComponents(i)
    Set oMod = oComp.CodeModule

    If Not oMod Is Nothing Then
      pKind = vbext_pk_Proc
      pStart = oMod.ProcStartLine(cleanProcName, pKind)
      pCount = oMod.ProcCountLines(cleanProcName, pKind)

      If pStart > 0 And pCount > 0 Then
        OutModuleName = oComp.Name
        FindProcedureCodeInProject = oMod.Lines(pStart, pCount)

        Exit Function

      End If
    End If

  Next i

End Function

' Busca el código completo de un módulo por su nombre
Public Function FindModuleCodeInProject(ByVal ModName As String) As String

  On Error Resume Next

  Dim oProj        As VBIDE.VBProject

  Dim oComp        As VBIDE.VBComponent

  Dim cleanModName As String

  Dim i            As Long

  FindModuleCodeInProject = ""
  cleanModName = LCase$(Trim$(ModName))
  cleanModName = Replace(cleanModName, ".bas", "")
  cleanModName = Replace(cleanModName, ".cls", "")
  cleanModName = Replace(cleanModName, ".frm", "")

  If Len(cleanModName) = 0 Then Exit Function
  If g_VBInstance Is Nothing Then Exit Function
  Set oProj = g_VBInstance.ActiveVBProject

  If oProj Is Nothing Then Exit Function

  For i = 1 To oProj.VBComponents.Count
    Set oComp = oProj.VBComponents(i)

    If LCase$(oComp.Name) = cleanModName Then
      If Not oComp.CodeModule Is Nothing Then
        If oComp.CodeModule.CountOfLines > 0 Then
          FindModuleCodeInProject = oComp.CodeModule.Lines(1, oComp.CodeModule.CountOfLines)

          Exit Function

        End If
      End If
    End If

  Next i

End Function

' Resuelve inteligentemente el contexto según el texto de la solicitud o el estado del editor
Public Function SmartResolveContext(ByVal PromptText As String, _
                                    ByRef OutContextType As String) As String

  On Error Resume Next

  Dim promptLower As String

  Dim words()     As String

  Dim i           As Long

  Dim keyword     As String

  Dim targetName  As String

  Dim foundCode   As String

  Dim modFound    As String

  Dim pName       As String, pKind As Long

  SmartResolveContext = ""
  OutContextType = ""
  promptLower = LCase$(PromptText)
  ' 1. Intentar resolver por mención explícita en el prompt ("función CalcularTotal", "sub MiRutina", "módulo modMain")
  words = Split(PromptText, " ")

  For i = 0 To UBound(words)
    keyword = LCase$(Trim$(words(i)))
    keyword = Replace(keyword, "¿", "")
    keyword = Replace(keyword, "¡", "")
    keyword = Replace(keyword, ":", "")

    Select Case keyword

      Case "función", "funcion", "function", "sub", "procedimiento", "procedure", "metodo", "método", "method", "rutina"

        If i + 1 <= UBound(words) Then
          targetName = CleanIdentifier(words(i + 1))

          If Len(targetName) > 0 Then
            foundCode = FindProcedureCodeInProject(targetName, modFound)

            If Len(foundCode) > 0 Then
              OutContextType = "Procedimiento '" & targetName & "'" & IIf(Len(modFound) > 0, " en " & modFound, "")
              SmartResolveContext = foundCode

              Exit Function

            End If
          End If
        End If

      Case "módulo", "modulo", "module", "clase", "class", "formulario", "form"

        If i + 1 <= UBound(words) Then
          targetName = CleanIdentifier(words(i + 1))

          If Len(targetName) > 0 Then
            foundCode = FindModuleCodeInProject(targetName)

            If Len(foundCode) > 0 Then
              OutContextType = "Módulo '" & targetName & "'"
              SmartResolveContext = foundCode

              Exit Function

            End If
          End If
        End If

    End Select

  Next i

  ' 2. Si no se especificó por nombre, verificar si hay selección real de texto en el editor
  foundCode = GetSelectedCode()

  If Len(foundCode) > 0 Then
    OutContextType = "Código Seleccionado"
    SmartResolveContext = foundCode

    Exit Function

  End If

  ' 3. Verificar si el cursor est dentro de un procedimiento
  foundCode = GetActiveProcedure(pName, pKind)

  If Len(foundCode) > 0 Then
    OutContextType = "Procedimiento Actual (" & pName & ")"
    SmartResolveContext = foundCode

    Exit Function

  End If

  ' 4. Si el prompt pide análisis/revisión general y hay un módulo abierto
  If InStr(promptLower, "analiza") > 0 Or InStr(promptLower, "revisa") > 0 Or InStr(promptLower, "explica") > 0 Or InStr(promptLower, "optimiza") > 0 Or InStr(promptLower, "modulo") > 0 Or InStr(promptLower, "código") > 0 Then
    foundCode = GetActiveModuleCode()

    If Len(foundCode) > 0 Then
      OutContextType = "Módulo Activo"
      SmartResolveContext = foundCode

      Exit Function

    End If
  End If

End Function

Private Function CleanIdentifier(ByVal RawWord As String) As String

  Dim s As String

  s = Trim$(RawWord)
  s = Replace(s, """", "")
  s = Replace(s, "'", "")
  s = Replace(s, "(", "")
  s = Replace(s, ")", "")
  s = Replace(s, ",", "")
  s = Replace(s, ";", "")
  s = Replace(s, ".", "")
  s = Replace(s, "?", "")
  s = Replace(s, "¿", "")
  CleanIdentifier = s
End Function
