Attribute VB_Name = "modHttpClient"
Option Explicit

' ==============================================================================
' VB6 AI Assistant - Cliente HTTP Win32 con Decodificacion UTF-8 Nativa
' ==============================================================================
Private Const CP_UTF8 As Long = 65001

Private Const CP_ACP  As Long = 0

Private Declare Function MultiByteToWideChar _
                Lib "kernel32" (ByVal CodePage As Long, _
                                ByVal dwFlags As Long, _
                                ByVal lpMultiByteStr As Long, _
                                ByVal cchMultiByte As Long, _
                                ByVal lpWideCharStr As Long, _
                                ByVal cchWideChar As Long) As Long

Private Declare Function WideCharToMultiByte _
                Lib "kernel32" (ByVal CodePage As Long, _
                                ByVal dwFlags As Long, _
                                ByVal lpWideCharStr As Long, _
                                ByVal cchWideChar As Long, _
                                ByVal lpMultiByteStr As Long, _
                                ByVal cchMultiByte As Long, _
                                ByVal lpDefaultChar As Long, _
                                ByVal lpUsedDefaultChar As Long) As Long

' Convierte bytes UTF-8 a cadena String Unicode nativa de VB6 sin corrupcion
Public Function Utf8BytesToString(ByRef RawBytes As Variant) As String

  On Error GoTo Fallback

  Dim byteArr() As Byte

  Dim lSize     As Long

  Dim lChars    As Long

  Dim sResult   As String

  byteArr = RawBytes
  lSize = UBound(byteArr) - LBound(byteArr) + 1

  If lSize <= 0 Then Exit Function
  lChars = MultiByteToWideChar(CP_UTF8, 0, VarPtr(byteArr(LBound(byteArr))), lSize, 0, 0)

  If lChars > 0 Then
    sResult = String$(lChars, vbNullChar)
    MultiByteToWideChar CP_UTF8, 0, VarPtr(byteArr(LBound(byteArr))), lSize, StrPtr(sResult), lChars
    Utf8BytesToString = sResult

    Exit Function

  End If

Fallback:

  On Error Resume Next

  Dim objStream As Object

  Set objStream = CreateObject("ADODB.Stream")

  If Not objStream Is Nothing Then
    objStream.Type = 1 ' Binary
    objStream.Open
    objStream.Write RawBytes
    objStream.Position = 0
    objStream.Type = 2 ' Text
    objStream.Charset = "utf-8"
    Utf8BytesToString = objStream.ReadText
    objStream.Close
    Set objStream = Nothing

    If Len(Utf8BytesToString) > 0 Then Exit Function
  End If

  Utf8BytesToString = StrConv(RawBytes, vbUnicode)
End Function

' Convierte una cadena String de VB6 a un array de bytes en formato UTF-8 estricto
Public Function StringToUtf8Bytes(ByVal sText As String) As Byte()

  Dim lSize     As Long

  Dim byteArr() As Byte

  If Len(sText) = 0 Then
    StringToUtf8Bytes = byteArr

    Exit Function

  End If

  lSize = WideCharToMultiByte(CP_UTF8, 0, StrPtr(sText), Len(sText), 0, 0, 0, 0)

  If lSize > 0 Then
    ReDim byteArr(0 To lSize - 1)
    WideCharToMultiByte CP_UTF8, 0, StrPtr(sText), Len(sText), VarPtr(byteArr(0)), lSize, 0, 0
    StringToUtf8Bytes = byteArr
  End If

End Function

' Corrige cadenas que hayan sufrido doble codificacion o interpretacion ANSI (Mojibake)
Public Function FixMojibake(ByVal sText As String) As String

  If Len(sText) = 0 Then Exit Function

  ' Detectar si contiene secuencias tipicas de bytes UTF-8 leidos como ANSI Windows-1252
  If InStr(sText, "Ã") = 0 And InStr(sText, "â") = 0 And InStr(sText, "Â") = 0 And InStr(sText, "ð") = 0 Then
    FixMojibake = sText

    Exit Function

  End If

  On Error GoTo CatchErr

  Dim byteArr() As Byte

  Dim lSize     As Long

  Dim lChars    As Long

  Dim sResult   As String

  ' 1. Convertir la cadena ANSI a sus bytes crudos originales (CP 1252)
  lSize = WideCharToMultiByte(1252, 0, StrPtr(sText), Len(sText), 0, 0, 0, 0)

  If lSize > 0 Then
    ReDim byteArr(0 To lSize - 1)
    WideCharToMultiByte 1252, 0, StrPtr(sText), Len(sText), VarPtr(byteArr(0)), lSize, 0, 0
    ' 2. Re-decodificar esos bytes usando UTF-8 nativo
    lChars = MultiByteToWideChar(CP_UTF8, 0, VarPtr(byteArr(0)), lSize, 0, 0)

    If lChars > 0 Then
      sResult = String$(lChars, vbNullChar)
      MultiByteToWideChar CP_UTF8, 0, VarPtr(byteArr(0)), lSize, StrPtr(sResult), lChars
      FixMojibake = sResult

      Exit Function

    End If
  End If

CatchErr:
  FixMojibake = sText
End Function

Public Function HttpGet(ByVal Url As String, _
                        ByRef OutResponse As String, _
                        ByRef OutStatusCode As Long) As Boolean

  On Error GoTo ErrorHandler

  Dim http As Object

  OutResponse = ""
  OutStatusCode = 0
  HttpGet = False

  On Error Resume Next

  Set http = CreateObject("WinHttp.WinHttpRequest.5.1")

  If http Is Nothing Then
    Set http = CreateObject("MSXML2.ServerXMLHTTP.6.0")
  End If

  If http Is Nothing Then
    Set http = CreateObject("MSXML2.ServerXMLHTTP")
  End If

  On Error GoTo ErrorHandler

  If http Is Nothing Then
    OutResponse = "No se pudo instanciar el cliente HTTP COM en Win32."

    Exit Function

  End If

  http.Open "GET", Url, False
  http.setRequestHeader "Accept", "application/json; charset=utf-8"

  On Error Resume Next

  http.SetTimeouts 3000, 3000, 5000, 5000

  On Error GoTo ErrorHandler

  http.Send
  OutStatusCode = http.status

  ' Obtener respuesta decodificando UTF-8 directamente de los bytes crudos (ResponseBody)
  On Error Resume Next

  OutResponse = Utf8BytesToString(http.ResponseBody)

  If Len(OutResponse) = 0 Then
    OutResponse = http.ResponseText
  End If

  OutResponse = FixMojibake(OutResponse)

  On Error GoTo ErrorHandler

  HttpGet = (OutStatusCode >= 200 And OutStatusCode < 300)
  Set http = Nothing

  Exit Function

ErrorHandler:
  OutResponse = "Error HTTP GET: " & Err.Description
  OutStatusCode = -1
  HttpGet = False
  Set http = Nothing
End Function

Public Function HttpPost(ByVal Url As String, _
                         ByVal JsonBody As String, _
                         ByRef OutResponse As String, _
                         ByRef OutStatusCode As Long) As Boolean

  On Error GoTo ErrorHandler

  Dim http        As Object

  Dim postBytes() As Byte

  OutResponse = ""
  OutStatusCode = 0
  HttpPost = False

  On Error Resume Next

  Set http = CreateObject("WinHttp.WinHttpRequest.5.1")

  If http Is Nothing Then
    Set http = CreateObject("MSXML2.ServerXMLHTTP.6.0")
  End If

  If http Is Nothing Then
    Set http = CreateObject("MSXML2.ServerXMLHTTP")
  End If

  On Error GoTo ErrorHandler

  If http Is Nothing Then
    OutResponse = "No se pudo instanciar el cliente HTTP COM en Win32."

    Exit Function

  End If

  http.Open "POST", Url, False
  http.setRequestHeader "Content-Type", "application/json; charset=utf-8"
  http.setRequestHeader "Accept", "application/json; charset=utf-8"

  On Error Resume Next

  http.SetTimeouts 3000, 3000, 10000, 10000

  On Error GoTo ErrorHandler

  ' Enviar los datos serializados en bytes UTF-8 reales
  postBytes = StringToUtf8Bytes(JsonBody)

  On Error Resume Next

  If (UBound(postBytes) - LBound(postBytes) + 1) > 0 Then
    http.Send postBytes
  Else
    http.Send JsonBody
  End If

  On Error GoTo ErrorHandler

  OutStatusCode = http.status

  ' Obtener respuesta decodificando UTF-8 directamente de los bytes crudos (ResponseBody)
  On Error Resume Next

  OutResponse = Utf8BytesToString(http.ResponseBody)

  If Len(OutResponse) = 0 Then
    OutResponse = http.ResponseText
  End If

  OutResponse = FixMojibake(OutResponse)

  On Error GoTo ErrorHandler

  HttpPost = (OutStatusCode >= 200 And OutStatusCode < 300)
  Set http = Nothing

  Exit Function

ErrorHandler:
  OutResponse = "Error HTTP POST: " & Err.Description
  OutStatusCode = -1
  HttpPost = False
  Set http = Nothing
End Function
