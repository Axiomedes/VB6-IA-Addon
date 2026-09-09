VB6-AI Assistant (VB6 Addon)

# GUÍA DE CONFIGURACIÓN Y PUESTA EN MARCHA — VB6 AI ASSISTANT

Esta guía explica en detalle qué es el Add-In **VB6 AI Assistant**, qué funciones ofrece al desarrollador de **Microsoft Visual Basic 6.0**, cómo utilizar sus herramientas y cómo configurarlo paso a paso utilizando **Inteligencia Artificial Local (100% gratuita y privada con Ollama)** o **APIs en la Nube (OpenRouter, Google Gemini, Groq, OpenAI, Claude)**.

---

## 🤖 ¿QUÉ ES VB6 AI ASSISTANT?

**VB6 AI Assistant** es un complemento nativo (*Add-In COM / DLL*) desarrollado específicamente para el entorno de desarrollo **Microsoft Visual Basic 6.0 (SP6)**. Se integra de manera transparente dentro del IDE para actuar como un copiloto de programación asistido por Inteligencia Artificial moderna, adaptado rigurosamente a la sintaxis, particularidades, limitaciones y mejores prácticas de VB6 clásico (evitando sugerencias incompatibles de .NET).

El Add-In se comunica con un servicio ligero local en segundo plano (*Python FastAPI*), lo que le permite conectar tanto con modelos de IA locales (sin conexión a internet, 100% privados y gratuitos mediante Ollama) como con los modelos más avanzados disponibles en la nube.

---

## 💡 ¿QUÉ PUEDE HACER? (CAPACIDADES Y CASOS DE USO)

El asistente está diseñado para resolver las necesidades cotidianas del programador de VB6:

1. **Análisis y Depuración de Código en Vivo**:
   - Detecta errores lógicos, fugas de memoria por objetos o handles Win32 sin liberar (`Set obj = Nothing`, `DeleteObject`, `CloseHandle`).
   - Identifica desbordamientos de tipos comunes (ej. `Integer` vs `Long` al superar 32,767) y fallos de sintaxis.
   - Diagnostica problemas con llamadas a la API de Windows (`Declare Function ... Lib "user32"`).

2. **Comprensión y Documentación de Código Legacy**:
   - Explica rutinas antiguas, complejas o indocumentadas paso a paso en lenguaje claro.
   - Genera comentarios estructurados y documentación técnica de funciones o módulos completos.

3. **Refactorización y Optimización Estricta para VB6**:
   - Mejora la velocidad de bucles, optimiza el manejo de cadenas (`Mid$`, `InStr`, arrays de bytes) y consultas de bases de datos (ADO / DAO).
   - Garantiza que el código generado sea 100% compatible con Visual Basic 6.0 (evita constructores inexistentes, `Try...Catch` o tipos de datos modernos).

4. **Generación de Nuevas Funciones y Componentes**:
   - Crea subrutinas, funciones de validación, wrappers para APIs Win32 complejas, algoritmos de cálculo y módulos de clase (`.cls`).

5. **Comparación Visual de Cambios (Diff Engine) y Aplicación Segura**:
   - Muestra una ventana de comparación lado a lado (*Original* vs. *Propuesto por IA*).
   - Permite aplicar el código optimizado directamente al editor de VB6 con un solo clic o rechazarlo de manera segura.

6. **Copias de Seguridad y Deshacer (Rollback)**:
   - Antes de modificar cualquier línea en el IDE, el Add-In crea automáticamente un punto de restauración en una base de datos local SQLite (`VB6AI.db`), permitiendo auditar o revertir cambios.

---

## 🖥️ DESCRIPCIÓN DE INTERFACES Y PROPIEDADES (UI)

El Add-In cuenta con tres formularios principales diseñados bajo la estética clásica y funcional de Win32 / VB6:

### 1. Ventana Principal del Asistente (`frmAIAssistant`)
- **Chat con RichTextBox Avanzado**: usando el RichtextBox de Krool, este visualiza las respuestas con colores sintácticos (títulos en negrita, código en verde, alertas en naranja y errores en rojo), soporte total de caracteres y acentos en español (ANSI/CP1252) y sin parpadeo de pantalla (*flicker-free*).
- **Selector Inteligente de Contexto**:
  - `Código Seleccionado`: Captura automáticamente las líneas marcadas con el ratón en el editor.
  - `Módulo Actual`: Envía todo el código del formulario o módulo `.bas`/`.frm` activo.
  - `Función / Subrutina Automática`: Si en el chat escribes *"analiza la función CalcularTotales"*, el Add-In busca automáticamente la subrutina dentro del módulo activo y la envía como contexto.
  - `Sin Contexto`: Para preguntas generales de programación o dudas teóricas.
- **Selector Dinámico de Proveedor y Modelo**: Lista los modelos activos (locales o en la nube) y permite alternar entre ellos sin reiniciar el IDE.
- **Botón "Analizar Código"**: Ejecuta un prompt predefinido de auditoría de calidad y optimización sobre el contexto actual.
- **Botón "Aplicar Cambios"**: Abre la ventana de revisión de diferencias con el código propuesto.
- **Botón "Cfg" (Configuración)**: Acceso directo al gestor de proveedores y credenciales.
- **Ejecución Asíncrona (No Bloqueante)**: Permite seguir navegando o escribiendo en el IDE mientras la IA genera su respuesta, con opción de cancelación en cualquier momento.

### 2. Visor y Aplicador de Cambios (`frmChanges`)
- **Vista Comparativa**: Presenta el bloque de código original y el código generado por la IA para su inspección antes de tocar el proyecto.
- **Botón "Aplicar al Código"**: Reemplaza el texto en la ventana de código activa del IDE y registra el respaldo de seguridad.
- **Botón "Cerrar" / "Descartar"**: Cancela la operación sin alterar el código fuente.

### 3. Gestor de Configuración (`frmConfig`)
- **Selector de Idioma / Language**: Detecta automáticamente el idioma de Windows (`Auto`), permitiendo también forzar `Español` o `English` con traducción en caliente de toda la interfaz y de las respuestas de la IA.
- **Selector de Proveedores**: Soporta Ollama (Local), OpenRouter, Google Gemini, Groq, OpenAI y Claude.
- **Gestión de Credenciales**: Permite ingresar o editar claves API (con modo seguro de ocultación de caracteres) y URLs de hosts locales.
- **Prueba de Conexión en Vivo (`[Probar]` / `[Test]`): Valida la conectividad con el proveedor en tiempo real antes de guardar cambios.
- **Sincronización Inmediata**: Al pulsar "Guardar", actualiza instantáneamente la lista de modelos e idioma en la ventana principal.

---



## 📋 REQUISITOS PREVIOS



1. **Sistema Operativo**: Windows 7, 8, 10 u 11 (32 o 64 bits).

2. **Entorno de Desarrollo**: Microsoft Visual Basic 6.0 (SP6 recomendado).

3. **Runtime del Servicio Local**: Python 3.10 o superior instalado en el equipo.



---



## 🏗️ ARQUITECTURA GENERAL



El sistema opera mediante dos componentes locales comunicados por HTTP en su propio equipo:



```text

┌───────────────────────────────┐               ┌───────────────────────────────┐

│     VISUAL BASIC 6.0 IDE      │   HTTP/JSON   │        SERVICIO LOCAL         │

│         (Add-In DLL)          ├──────────────►│     (Python FastAPI Bridge)   │

│  - Captura código en memoria  │ 127.0.0.1:8765│  - Adapta prompts a VB6 (SP6) │

│  - Muestra chat y diferencias │               │  - Conecta con Ollama/Cloud   │

└───────────────────────────────┘               └───────────────┬───────────────┘

                                                                │

                                              ┌─────────────────┴─────────────────┐

                                              ▼                                   ▼

                                      IA LOCAL (Ollama)                   IA NUBE (OpenRouter /

                                      (127.0.0.1:11434)                   Gemini / Groq / OpenAI)

```



---



## 🚀 GUÍA RÁPIDA DE PUESTA EN MARCHA (4 PASOS)



---



### PASO 1: Iniciar el Servicio Local (`VB6AIService`)



1. Navega a la carpeta:

   ```text

   ...\Service_Python\

   ```

2. Haz doble clic en el archivo:

   ```cmd

   run_service.bat

   ```

3. Se abrirá una ventana de consola indicando:

   ```text

   Uvicorn running on http://127.0.0.1:8765

   ```

   *(Mantén esta ventana abierta mientras utilices el asistente en VB6).*

4. Puedes verificar que está funcionando abriendo en tu navegador:

   `http://127.0.0.1:8765/api/v1/health`



---



### PASO 2: Elegir tu Proveedor de IA



Puedes utilizar **IA Local** (sin internet ni claves) o **APIs Cloud Gratuitas**:



---



#### 🌟 OPCIÓN A: IA Local 100% Gratuita con Ollama (Recomendada para Privacidad)

*Ideal para trabajar offline, con privacidad total y sin límites de cuotas ni registrar tarjetas de crédito.*



1. Descarga e instala **Ollama** para Windows desde su sitio oficial:

   👉 **[https://ollama.com/download](https://ollama.com/download)**

2. Una vez instalado, abre una consola de comandos (`cmd.exe` o PowerShell) y descarga el modelo de código que prefieras:

   * **CodeLlama (Especializado en programación)**:

     ```cmd

     ollama run codellama

     ```

   * **Llama 3 (Equilibrado y rápido)**:

     ```cmd

     ollama run llama3

     ```

   * **Qwen 2.5 Coder (Excelente para código)**:

     ```cmd

     ollama run qwen2.5-coder:7b

     ```

3. Verifica que Ollama esté activo abriendo en el navegador:

   `http://127.0.0.1:11434/api/tags`

4. ¡Listo! El Add-In detectará automáticamente los modelos descargados.



---



#### ☁️ OPCIÓN B: Modelos Gratuitos en la Nube con OpenRouter (`:free`)

*Permite usar modelos muy potentes como DeepSeek R1, Llama 3.3 70B o Qwen 2.5 Coder 32B gratis.*



1. Regístrate gratis en: 👉 **[https://openrouter.ai](https://openrouter.ai)**

2. Ve a la sección de API Keys y crea una clave gratuita: 👉 **[https://openrouter.ai/keys](https://openrouter.ai/keys)**

3. Abre con el Bloc de Notas el archivo de configuración:

   `Service_Python\.env`

4. Pega tu clave en la variable `OPENROUTER_API_KEY`:

   ```ini

   OPENROUTER_API_KEY=sk-or-v1-tu-clave-aquíi

   ```

5. Reinicia `run_service.bat` para aplicar los cambios.

6. En el Add-In de VB6, selecciona Proveedor: **OpenRouter** y Modelo: `deepseek/deepseek-r1:free` o `meta-llama/llama-3.3-70b-instruct:free`.



---



#### ⚡ OPCIÓN C: Google Gemini (Tier Gratuito Oficial)

*Ultra-rápido y con amplia ventana de contexto.*



1. Obtén tu clave gratuita en Google AI Studio: 👉 **[https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)**

2. Abre el archivo `Service_Python\.env` y pega tu clave:

   ```ini

   GEMINI_API_KEY=AIzaSy-tu-clave-aquíi

   ```

3. Reinicia `run_service.bat`.

4. En el Add-In de VB6, selecciona Proveedor: **Google Gemini** y Modelo: `gemini-2.0-flash`.



---



#### 🚀 OPCIÓN D: Groq (Inferencia de Ultra Alta Velocidad)

*Respuestas casi instantáneas en modelos Llama y DeepSeek.*



1. Crea tu cuenta y obtén tu clave gratis en: 👉 **[https://console.groq.com/keys](https://console.groq.com/keys)**

2. Abre `Service_Python\.env` y pega tu clave:

   ```ini

   GROQ_API_KEY=gsk_tu-clave-aquíi

   ```

3. Reinicia `run_service.bat`.

4. En el Add-In de VB6, selecciona Proveedor: **Groq** y Modelo: `llama-3.3-70b-versatile`.



---



### PASO 3: Compilar y Registrar el Add-In en VB6



1. Inicia **Microsoft Visual Basic 6.0**.

2. Abre el proyecto:

   `...\AddIn_VB6\VB6AIAssistant.vbp`

3. En el menú superior de VB6, haz clic en:

   **File -> Make VB6AIAssistant.dll...**

4. Guarda el archivo DLL en la misma carpeta `AddIn_VB6\`.

5. *(Opcional)* Si deseas registrarlo globalmente en el sistema, ejecuta como Administrador:

   `AddIn_VB6\register_addin.bat`



---



### PASO 4: Probar el Asistente en el IDE de VB6



1. Abre cualquier proyecto en Visual Basic 6 (o crea un nuevo proyecto `Standard EXE`).

2. En la barra de menús principal de VB6, ve a:

   **Add-Ins (Complementos) -> &VB6 AI Assistant...**

3. Se abrirá la ventana del asistente.

4. **Verifica la barra de estado inferior**:

   * Mostrará `Estado: Servicio Conectado` y listará los modelos disponibles.

5. **Prueba 1: Consulta directa**:

   * Escribe en el cuadro de texto: `¿Cómo crear un archivo de texto en VB6 usando FileSystemObject?` y pulsa **Enviar**.

6. **Prueba 2: Análisis de código seleccionado**:

   * Abre un módulo `.bas` o formulario `.frm` en el editor de VB6.

   * Selecciona varias líneas de código con el ratón.

   * En el asistente, pulsa el botón **Analizar Código**.

   * El asistente capturará el código seleccionado del IDE y generará una explicación y propuesta de optimización en tiempo real.



---



## 🛠️ RESOLUCIÓN DE PROBLEMAS FRECUENTES (FAQ)



### 1. El asistente dice "No se detectó el Servicio Local en http://127.0.0.1:8765"

* **Causa**: El servicio en Python no está iniciado.

* **Solución**: Ejecuta `Service_Python\run_service.bat`. Verifica que no haya un firewall o antivirus bloqueando el puerto local 8765.



### 2. Ollama está instalado pero el asistente no muestra modelos

* **Causa**: Ollama no está en ejecución o no has descargado ningún modelo.

* **Solución**: Abre una terminal y ejecuta `ollama run codellama`. Verifica que el icono de Ollama aparezca en la bandeja del sistema de Windows.



### 3. El menú "&VB6 AI Assistant..." no aparece en VB6

* **Causa**: El Add-In no está cargado en el administrador de complementos.

* **Solución**: En VB6 ve a **Add-Ins -> Add-In Manager...**, busca **VB6 AI Assistant**, marca **Loaded/Unloaded** y **Load on Startup**, y pulsa **OK**.



### 4. ¿El asistente congela el IDE de VB6 mientras la IA piensa?

* **No**: El Add-In utiliza un sistema de **Jobs Asíncronos con Timer no bloqueante (200 ms)**. Puedes seguir navegando por el código del IDE, editando o cancelando la consulta con el botón **Cancelar** en cualquier momento.



---



*Desarrollado por Axio.UK para la comunidad de desarrolladores de Microsoft Visual Basic 6.0.*

*Idea Original de @Ivo (Argentina) dentro del Grupo Whatsapp Lationamericano de Visual Basic 6.0*

