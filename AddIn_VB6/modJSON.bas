Attribute VB_Name = "modJSON"
Option Explicit

' ==============================================================================
' VB6 AI Assistant - Parser y Formateador JSON Ultraligero y Seguro para VB6
' ==============================================================================
' Escapa cadenas para formato JSON estricto (RFC 8259)
Public Function JsonEscape(ByVal Text As String) As String

  Dim res As String

  Dim q   As String

  q = Chr$(34)
  ' 1. Barra invertida primero
  res = Replace(Text, "\", "\\")
  ' 2. Comilla doble usando Chr$(34)
  res = Replace(res, q, "\" & q)
  ' 3. Saltos de linea y tabulaciones
  res = Replace(res, vbCrLf, "\n")
  res = Replace(res, vbCr, "\n")
  res = Replace(res, vbLf, "\n")
  res = Replace(res, vbTab, "\t")
  res = Replace(res, Chr$(8), "\b")
  res = Replace(res, Chr$(12), "\f")
  JsonEscape = res
End Function

' Constructor de propiedad String JSON: "clave": "valor"
Public Function JsonPropString(ByVal Key As String, ByVal Value As String) As String

  Dim q As String

  q = Chr$(34)
  JsonPropString = q & Key & q & ": " & q & JsonEscape(Value) & q
End Function

' Constructor de propiedad Booleana JSON: "clave": true / false
Public Function JsonPropBool(ByVal Key As String, ByVal Value As Boolean) As String

  Dim q As String

  q = Chr$(34)

  If Value Then
    JsonPropBool = q & Key & q & ": true"
  Else
    JsonPropBool = q & Key & q & ": false"
  End If

End Function

' Constructor de propiedad Numerica JSON: "clave": 123
Public Function JsonPropNumber(ByVal Key As String, ByVal Value As Double) As String

  Dim q As String

  q = Chr$(34)
  JsonPropNumber = q & Key & q & ": " & Trim$(Str$(Value))
End Function

' Extrae un valor de tipo String de un objeto JSON plano
Public Function JsonGetString(ByVal json As String, ByVal Key As String) As String

  Dim searchKey As String

  Dim posKey    As Long

  Dim posColon  As Long

  Dim posStart  As Long

  Dim posEnd    As Long

  Dim charAt    As String

  Dim q         As String

  q = Chr$(34)
  JsonGetString = ""
  searchKey = q & Key & q
  posKey = InStr(1, json, searchKey, vbTextCompare)

  If posKey = 0 Then Exit Function
  posColon = InStr(posKey + Len(searchKey), json, ":")

  If posColon = 0 Then Exit Function
  ' Buscar comilla inicial del valor
  posStart = InStr(posColon + 1, json, q)

  If posStart = 0 Then Exit Function
  ' Buscar comilla de cierre considerando secuencias de escape
  posEnd = posStart + 1

  Do While posEnd <= Len(json)
    charAt = Mid$(json, posEnd, 1)

    If charAt = "\" Then
      posEnd = posEnd + 2
    ElseIf charAt = q Then

      Exit Do

    Else
      posEnd = posEnd + 1
    End If

  Loop

  Dim valStr As String

  valStr = Mid$(json, posStart + 1, posEnd - posStart - 1)
  ' Desescapar caracteres comunes y Unicode
  valStr = UnescapeUnicode(valStr)
  valStr = Replace(valStr, "\n", vbCrLf)
  valStr = Replace(valStr, "\r", "")
  valStr = Replace(valStr, "\t", vbTab)
  valStr = Replace(valStr, "\" & q, q)
  valStr = Replace(valStr, "\\", "\")
  ' Corrección automtica de mojibake por si acaso
  valStr = FixMojibake(valStr)
  JsonGetString = valStr
End Function

' Decodifica secuencias de escape Unicode en formato \uXXXX (ej: \u00e1 -> , \u00f1 -> ñ)
Public Function UnescapeUnicode(ByVal sText As String) As String

  Dim Pos     As Long

  Dim hexCode As String

  Dim charVal As Long

  Dim res     As String

  res = sText
  Pos = InStr(1, res, "\u", vbBinaryCompare)

  Do While Pos > 0 And (Pos + 5) <= Len(res)
    hexCode = Mid$(res, Pos + 2, 4)

    On Error Resume Next

    charVal = CLng("&H" & hexCode)

    If Err.Number = 0 And charVal > 0 Then
      res = Left$(res, Pos - 1) & ChrW$(charVal) & Mid$(res, Pos + 6)
      Pos = InStr(Pos + 1, res, "\u", vbBinaryCompare)
    Else
      Err.Clear
      Pos = InStr(Pos + 2, res, "\u", vbBinaryCompare)
    End If

    On Error GoTo 0

  Loop

  UnescapeUnicode = res
End Function

' Extrae un valor booleano de un JSON
Public Function JsonGetBool(ByVal json As String, ByVal Key As String) As Boolean

  Dim searchKey As String

  Dim posKey    As Long

  Dim posColon  As Long

  Dim subStr    As String

  Dim q         As String

  q = Chr$(34)
  JsonGetBool = False
  searchKey = q & Key & q
  posKey = InStr(1, json, searchKey, vbTextCompare)

  If posKey = 0 Then Exit Function
  posColon = InStr(posKey + Len(searchKey), json, ":")

  If posColon = 0 Then Exit Function
  subStr = LCase$(Trim$(Mid$(json, posColon + 1, 15)))

  If Left$(subStr, 4) = "true" Then
    JsonGetBool = True
  End If

End Function

' Extrae una coleccion de cadenas de un array JSON de strings: ["item1", "item2"]
Public Function JsonGetArrayStrings(ByVal json As String, _
                                    ByVal arrayKey As String) As Collection

  Dim col             As New Collection

  Dim searchKey       As String

  Dim posKey          As Long

  Dim posBracketOpen  As Long

  Dim posBracketClose As Long

  Dim arrayContent    As String

  Dim posStart        As Long, posEnd As Long

  Dim itemStr         As String

  Dim q               As String

  q = Chr$(34)
  Set JsonGetArrayStrings = col
  searchKey = q & arrayKey & q
  posKey = InStr(1, json, searchKey, vbTextCompare)

  If posKey = 0 Then Exit Function
  posBracketOpen = InStr(posKey + Len(searchKey), json, "[")

  If posBracketOpen = 0 Then Exit Function
  posBracketClose = InStr(posBracketOpen + 1, json, "]")

  If posBracketClose = 0 Then Exit Function
  arrayContent = Mid$(json, posBracketOpen + 1, posBracketClose - posBracketOpen - 1)
  posStart = InStr(1, arrayContent, q)

  Do While posStart > 0
    posEnd = InStr(posStart + 1, arrayContent, q)

    If posEnd = 0 Then Exit Do
    itemStr = Mid$(arrayContent, posStart + 1, posEnd - posStart - 1)

    If Len(Trim$(itemStr)) > 0 Then
      col.Add Trim$(itemStr)
    End If

    posStart = InStr(posEnd + 1, arrayContent, q)
  Loop

  Set JsonGetArrayStrings = col
End Function
