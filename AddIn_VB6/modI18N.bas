Attribute VB_Name = "modI18N"
Option Explicit

' ==============================================================================
' VB6 AI Assistant - Modulo de Internacionalizacion y Deteccion de Idioma (i18n)
' Soporta Deteccion Automatica Win32, Espanol e Ingles.
' ==============================================================================

Private Declare Function GetUserDefaultUILanguage Lib "kernel32" () As Integer
Private Declare Function GetSystemDefaultLCID Lib "kernel32" () As Long

Public g_CurrentLanguage As String ' "es" o "en"
Public g_LanguageMode    As String ' "auto", "es", "en"

' Constantes de idiomas soportados
Public Const LANG_AUTO   As String = "auto"
Public Const LANG_ES     As String = "es"
Public Const LANG_EN     As String = "en"

' Detecta el idioma primario del sistema operativo mediante API Win32
Public Function DetectSystemLanguage() As String
    On Error Resume Next
    Dim LangID As Long
    ' El ID de idioma primario son los primeros 10 bits del LANGID
    LangID = GetUserDefaultUILanguage() And &H3FF
    
    ' &H0A = 10 = LANG_SPANISH
    If LangID = &HA Then
        DetectSystemLanguage = LANG_ES
    Else
        ' Fallback internacional por defecto: Ingles (&H09 y cualquier otro idioma)
        DetectSystemLanguage = LANG_EN
    End If
    If Err.Number <> 0 Then
        DetectSystemLanguage = LANG_ES
    End If
End Function

' Inicializa el sistema de internacionalizacion leyendo la configuracion guardada
Public Sub InitI18N()
    On Error Resume Next
    Dim savedMode As String
    savedMode = LCase$(Trim$(GetSetting("VB6AIAssistant", "Settings", "LanguageMode", LANG_AUTO)))
    
    If savedMode = LANG_ES Or savedMode = LANG_EN Then
        g_LanguageMode = savedMode
        g_CurrentLanguage = savedMode
    Else
        g_LanguageMode = LANG_AUTO
        g_CurrentLanguage = DetectSystemLanguage()
    End If
End Sub

' Cambia el idioma actual y guarda la preferencia en el registro
Public Sub SetLanguage(ByVal mode As String)
    On Error Resume Next
    g_LanguageMode = LCase$(Trim$(mode))
    
    If g_LanguageMode = LANG_ES Or g_LanguageMode = LANG_EN Then
        g_CurrentLanguage = g_LanguageMode
    Else
        g_LanguageMode = LANG_AUTO
        g_CurrentLanguage = DetectSystemLanguage()
    End If
    
    SaveSetting "VB6AIAssistant", "Settings", "LanguageMode", g_LanguageMode
End Sub

' Obtiene el codigo de idioma actual ("es" o "en")
Public Function GetLanguage() As String
    If g_CurrentLanguage = "" Then
        InitI18N
    End If
    GetLanguage = g_CurrentLanguage
End Function

' Obtiene la traduccion segun la clave solicitada para el idioma activo
Public Function T(ByVal key As String, Optional ByVal defaultVal As String = "") As String
    Dim isEn As Boolean
    isEn = (GetLanguage() = LANG_EN)
    
    Select Case UCase$(Trim$(key))
        ' --- Titulos de Ventanas ---
        Case "APP_TITLE"
            T = "VB6 AI Assistant"
        Case "TITLE_CONFIG"
            If isEn Then T = "AI Provider Configuration" Else T = "Configuración de Proveedores de IA"
        Case "TITLE_CHANGES"
            If isEn Then T = "Review Code Changes - VB6 AI Assistant" Else T = "Revisión de Cambios de Código por VB6 AI Assistant"
        Case "TITLE_ABOUT"
            If isEn Then T = "About..." Else T = "Acerca de..."
            
        ' --- Menus y Tooltips ---
        Case "MENU_MAIN"
            T = "&VB6 AI Assistant..."
        Case "MENU_TOOLTIP"
            If isEn Then T = "Artificial Intelligence Assistant for Visual Basic 6.0" Else T = "Asistente de Inteligencia Artificial para Visual Basic 6.0"
            
        ' --- Botones Comunes ---
        Case "BTN_SEND"
            If isEn Then T = "Send" Else T = "Enviar"
        Case "BTN_ANALYZE"
            If isEn Then T = "Analyze Code" Else T = "Analizar Código"
        Case "BTN_APPLY"
            If isEn Then T = "Apply Changes" Else T = "Aplicar Cambios"
        Case "BTN_APPLY_EDITOR"
            If isEn Then T = "Apply to Editor" Else T = "Aplicar al Código"
        Case "BTN_CANCEL"
            If isEn Then T = "Cancel" Else T = "Cancelar"
        Case "BTN_CLEAR"
            If isEn Then T = "Clear" Else T = "Limpiar"
        Case "BTN_CLOSE"
            If isEn Then T = "Close" Else T = "Cerrar"
        Case "BTN_DISCARD"
            If isEn Then T = "Discard" Else T = "Descartar"
        Case "BTN_SAVE"
            If isEn Then T = "Save Configuration" Else T = "Guardar Configuración"
        Case "BTN_TEST"
            If isEn Then T = "Test Connection" Else T = "Probar Conexión"
        Case "BTN_FETCH_MODELS"
            If isEn Then T = "Get Models" Else T = "Obtener Modelos"
        Case "BTN_COPY"
            If isEn Then T = "Copy Proposal" Else T = "Copiar Propuesta"
        Case "BTN_UNIFIED_VIEW"
            If isEn Then T = "Unified View" Else T = "Vista Unificada"
        Case "BTN_CFG"
            T = "Cfg"
        ' --- Etiquetas Generales ---
        Case "LBL_PROVIDER"
            If isEn Then T = "AI Provider:" Else T = "Proveedor de IA:"
        Case "LBL_PROVIDER_FRAME"
            If isEn Then T = "Select Artificial Intelligence Provider" Else T = "Seleccionar Proveedor de Inteligencia Artificial"
        Case "LBL_CONFIG_DETAILS"
            If isEn Then T = "Connection & Authentication Parameters" Else T = "Parámetros de Conexión y Autenticación"
        Case "LBL_MODEL"
            If isEn Then T = "Default / Custom Model:" Else T = "Modelo por Defecto / Personalizado:"
        Case "LBL_LANGUAGE"
            If isEn Then T = "Interface Language / Idioma:" Else T = "Idioma de Interfaz / Language:"
        Case "LBL_OLLAMA_HOST"
            If isEn Then T = "Ollama Server URL (Local):" Else T = "URL del Servidor Ollama (Local):"
        Case "LBL_API_KEY"
            If isEn Then T = "API Key (Provider Key):" Else T = "Clave API (API Key del Proveedor):"
        Case "LBL_SHOW_KEY"
            If isEn Then T = "Show" Else T = "Mostrar"
        Case "LBL_STATUS"
            If isEn Then T = "Status:" Else T = "Estado:"
        Case "LBL_CONTEXT"
            If isEn Then T = "Context:" Else T = "Contexto:"
        Case "LBL_DIFF_INFO"
            If isEn Then T = "Proposal Information" Else T = "Información de la Propuesta"
        Case "LBL_DIFF_ORIG"
            If isEn Then T = "Original Code:" Else T = "Código Original:"
        Case "LBL_DIFF_PROP"
            If isEn Then T = "Proposed Code (AI):" Else T = "Código Propuesto (IA):"
        Case "LBL_ABOUT_SUPPORT"
            If isEn Then T = "supported by" Else T = "con apoyo"
            
        ' --- Opciones de Contexto ---
        Case "CTX_SELECTED"
            If isEn Then T = "Selected Code" Else T = "Código Seleccionado"
        Case "CTX_MODULE"
            If isEn Then T = "Entire Module" Else T = "Módulo Actual"
        Case "CTX_NONE"
            If isEn Then T = "No Context" Else T = "Sin Contexto"
        Case "CTX_AUTO"
            If isEn Then T = "Auto-Detect Function/Sub" Else T = "Función / Subrutina Automática"
            
        ' --- Mensajes de Estado ---
        Case "STATUS_CONNECTED"
            If isEn Then T = "Service Connected" Else T = "Servicio Conectado"
        Case "STATUS_DISCONNECTED"
            If isEn Then T = "Local Service not detected at " Else T = "No se detectó el Servicio Local en "
        Case "STATUS_QUERYING"
            If isEn Then T = "Querying AI in background..." Else T = "Conectando con IA en background..."
        Case "STATUS_STREAMING"
            If isEn Then T = "Generating response..." Else T = "Generando respuesta..."
        Case "STATUS_COMPLETED"
            If isEn Then T = "Completed" Else T = "Completado"
        Case "STATUS_CANCELLED"
            If isEn Then T = "Cancelled by user" Else T = "Cancelado por el usuario"
        Case "STATUS_ERROR"
            If isEn Then T = "Error in query" Else T = "Error en la consulta"
        Case "STATUS_READY"
            If isEn Then T = "Ready" Else T = "Listo"
            
        ' --- Prompts y Mensajes de Dialogo ---
        Case "PROMPT_ANALYZE_DEFAULT"
            If isEn Then
                T = "Please analyze this Visual Basic 6.0 code, explain how it works, identify potential bugs or memory leaks, and propose an optimized version:"
            Else
                T = "Analiza el siguiente código de VB6, explica su funcionamiento, posibles bugs y sugiere optimizaciones:"
            End If
            
        Case "PROMPT_AUTO_CTX_FOUND"
            If isEn Then T = "CONTEXT DETECTED" Else T = "CONTEXTO DETECTADO"
            
        Case "MSG_CONFIRM_CLEAR"
            If isEn Then T = "Do you want to clear the chat history?" Else T = "¿Deseas limpiar el historial del chat?"
            
        Case "MSG_NO_CODE_TO_APPLY"
            If isEn Then T = "There is no code generated by the AI in the chat to review." Else T = "No hay código generado por la IA en el chat para revisar."
            
        Case "MSG_APPLIED_SUCCESS"
            If isEn Then T = "Code was successfully applied to the VB6 editor." Else T = "El código ha sido aplicado exitosamente al editor de VB6."
            
        Case "MSG_NO_CHANGES_DETECTED"
            If isEn Then T = "No differences were detected between the codes." Else T = "No se detectaron diferencias entre los códigos."
            
        Case "MSG_TEST_OK"
            If isEn Then T = "[OK] Connection successful" Else T = "[OK] Conexión exitosa"
            
        Case "MSG_TEST_FAIL"
            If isEn Then T = "[X] Connection failed" Else T = "[X] Error de conexión"
            
        Case "MSG_CONFIG_SAVED"
            If isEn Then T = "Configuration saved and reloaded successfully." Else T = "Configuración guardada y recargada exitosamente."
            
        Case "MSG_WRITE_REQUEST"
            If isEn Then T = "Please write a request." Else T = "Por favor escriba una solicitud."
            
        Case "MSG_REQUEST_IN_PROGRESS"
            If isEn Then T = "A request is already in progress. Press 'Cancel' if you want to abort it." Else T = "Ya hay una solicitud en curso. Presione 'Cancelar' si desea interrumpirla."
            
        ' --- Opciones del Combo Idioma ---
        Case "LANG_OPT_AUTO"
            If isEn Then T = "Auto (Detect System)" Else T = "Auto (Detectar Sistema)"
        Case "LANG_OPT_ES"
            T = "Español"
        Case "LANG_OPT_EN"
            T = "English"
            
        Case Else
            If defaultVal <> "" Then
                T = defaultVal
            Else
                T = key
            End If
    End Select
End Function
